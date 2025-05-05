from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import User, Course, Subscription, Lesson


class SubscriptionTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(title="Python")
        self.lesson = Lesson.objects.create(title="drf", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)


    def test_create_subscription(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('subscription-list'), {'course': self.course.id})
        self.assertEqual(response.status_code, 201)

    def test_delete_subscription(self):
        subscription = Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('subscription-detail', args=[subscription.id]))
        self.assertEqual(response.status_code, 204)

    def test_lesson_create(self):
        url = reverse("materials:lesson_create")
        data = {
            "title": "drf",
            "course": self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2)