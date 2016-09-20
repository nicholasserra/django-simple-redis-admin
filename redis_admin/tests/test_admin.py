from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase


class RedisAdminSanityTests(TestCase):
    urls = 'redis_admin.tests.test_urls' # Deprecated in Django 1.10.

    def setUp(self):
        self.user = User.objects.create_superuser('test', 'test@test.com', 'password')
        self.client.login(username=self.user.username, password='password')
        self.ROOT_URLCONF = getattr(settings, 'ROOT_URLCONF', None)
        setattr(settings, 'ROOT_URLCONF', 'redis_admin.tests.test_urls')

    def test_admin_accessible(self):
        response = self.client.get('/admin/')
        self.assertEqual(200, response.status_code)

    def tearDown(self):
        setattr(settings, 'ROOT_URLCONF', self.ROOT_URLCONF)


class RedisAdminViewsTests(TestCase):
    urls = 'redis_admin.tests.test_urls' # Deprecated in Django 1.10.

    def setUp(self):
        self.user = User.objects.create_superuser('test', 'test@test.com', 'password')
        self.client.login(username=self.user.username, password='password')
        self.ROOT_URLCONF = getattr(settings, 'ROOT_URLCONF', None)
        setattr(settings, 'ROOT_URLCONF', 'redis_admin.tests.test_urls')

        cache.master_client.set('test-redis-admin', 'test')

    def test_index(self):
        response = self.client.get('/admin/redis_admin/manage/')
        self.assertEqual(200, response.status_code)

    def test_key(self):
        response = self.client.get('/admin/redis_admin/manage/test-redis-admin/')
        self.assertEqual(200, response.status_code)

    def test_delete_key_confirmation(self):
        response = self.client.get('/admin/redis_admin/manage/test-redis-admin/delete/')
        self.assertEqual(200, response.status_code)

    def test_delete_key_action(self):
        response = self.client.post('/admin/redis_admin/manage/test-redis-admin/delete/', {'post': 'yes'})
        self.assertEqual(302, response.status_code)

    def tearDown(self):
        cache.master_client.delete('test-redis-admin')
        setattr(settings, 'ROOT_URLCONF', self.ROOT_URLCONF)
