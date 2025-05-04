from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import User, Course, Subscription

class SubscriptionTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.course = Course.objects.create(title='Test Course')

    def test_create_subscription(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('subscription-list'), {'course': self.course.id})
        self.assertEqual(response.status_code, 201)

    def test_delete_subscription(self):
        subscription = Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('subscription-detail', args=[subscription.id]))
        self.assertEqual(response.status_code, 204)

