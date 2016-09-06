from django.contrib import admin
from django.db import models
from django.conf.urls import url
from django.core.cache import cache
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages


class RedisAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(RedisAdmin, self).get_urls()

        my_urls = [
            url(r'^$', self.index),
            url(r'^(?P<key>.+)/delete/$', self.delete),
            url(r'^(?P<key>.+)/$', self.key),
        ]
        return my_urls + urls

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def index(self, request):

        if request.method == 'POST' and request.POST.getlist('_selected_action') and \
            request.POST.get('action') == 'delete_selected' and \
            request.POST.get('post') == 'yes':

            if cache.master_client.delete(*request.POST.getlist('_selected_action')):
                messages.add_message(request, messages.SUCCESS,
                                    'Successfully deleted %d keys.' %
                                    len(request.POST.getlist('_selected_action')))
            else:
                messages.add_message(request, messages.ERROR,
                                    'Could not delete %d keys.' %
                                    len(request.POST.getlist('_selected_action')))

        elif request.method == 'POST' and request.POST.getlist('_selected_action') and \
            request.POST.get('action') == 'delete_selected':

            return render_to_response('redis_admin/delete_selected_confirmation.html',
                                     {'keys': request.POST.getlist('_selected_action')},
                                     context_instance=RequestContext(request))

        if request.GET.get('q'):
            keys_result = cache.master_client.keys('*%s*' % request.GET.get('q'))
        else:
            keys_result = cache.master_client.keys('*')

        paginator = Paginator(keys_result, 100)

        page = request.GET.get('p')

        try:
            keys = paginator.page(page)
        except PageNotAnInteger:
            keys = paginator.page(1)
        except EmptyPage:
            keys = paginator.page(paginator.num_pages)

        return render_to_response('redis_admin/index.html', {'keys': keys, 
                                  'count': paginator.count, 'page_range': paginator.page_range},
                                   context_instance=RequestContext(request))

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def key(self, request, key):

        key_type = cache.master_client.type(key)

        if key_type == 'none':
            raise Http404

        context = {'key': key, 'type': key_type}

        if key_type == 'string':
             context['value'] = cache.master_client.get(key)
        elif key_type == 'set':
            context['value'] = str(cache.master_client.smembers(key))

        return render_to_response('redis_admin/key.html', context,
                                   context_instance=RequestContext(request))

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def delete(self, request, key):
        if request.method == "POST" and request.POST.get('post') == 'yes':
            if cache.master_client.delete(key):
                messages.add_message(request, messages.SUCCESS, 'The key "%s" was deleted successfully.' % key)
            else:
                messages.add_message(request, messages.ERROR, 'The key "%s" was not deleted successfully.' % key)
            return HttpResponseRedirect('%sredis_admin/manage/' % reverse('admin:index'))
        return render_to_response('redis_admin/delete_confirmation.html',
                                 {'key': key}, context_instance=RequestContext(request))

class Meta:
    app_label = 'redis_admin'
    verbose_name = 'Manage'
    verbose_name_plural = "Manage"

admin.site.register(type('manage', (models.Model,), {'__module__': '', 'Meta': Meta}), RedisAdmin)
