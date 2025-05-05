from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Course, Subscription, Lesson
from users.models import User


class SubscriptionTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@mail.ru")
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


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@mail.ru")
        self.course = Course.objects.create(title="Python")
        self.lesson = Lesson.objects.create(title="drf", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)


    def test_lesson_create(self):
        url = reverse("school:lessons_create")
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


    def test_lesson_retrieve(self):
        url = reverse("school:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("title"), self.lesson.name
        )

    def test_lesson_update(self):
        url = reverse("school:lessons_update", args=(self.lesson.pk,))
        data = {
            "title": "drf",
            'course': self.course.pk
        }
        response = self.client.get(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("title"), "drf"
        )

    def test_lesson_delete(self):
        url = reverse("school:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse('school:lessons_list')
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
