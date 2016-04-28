from redis_admin.compat import url as redis_admin_url, get_library


Library = get_library()
register = Library()


@register.tag
def url(parser, token):
    return redis_admin_url(parser, token)
