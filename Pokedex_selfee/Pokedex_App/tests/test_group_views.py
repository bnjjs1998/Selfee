from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APIClient


class GroupRemoveTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.group = Group.objects.create(name='grass')
        self.client = APIClient()

    def test_remove_group_success(self):
        # add user to group then remove
        self.user.groups.add(self.group)
        self.client.force_authenticate(user=self.user)
        resp = self.client.delete(f'/api/group/{self.group.name}/remove/')
        self.assertEqual(resp.status_code, 200)
        # reload user groups
        self.user.refresh_from_db()
        self.assertFalse(self.user.groups.filter(name__iexact=self.group.name).exists())

    def test_remove_group_not_member(self):
        # user not in group
        self.client.force_authenticate(user=self.user)
        resp = self.client.delete(f'/api/group/{self.group.name}/remove/')
        self.assertEqual(resp.status_code, 400)
