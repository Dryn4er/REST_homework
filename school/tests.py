from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Course, Subscription, Lesson
from users.models import User


class SubscriptionTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="password")
        self.course = Course.objects.create(title="Python")
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        Subscription.objects.all().delete()

        data = {
            "course": self.course.pk,
        }

        response = self.client.post("/subscriptions/create/", data=data)

        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Subscription.objects.count(), 1)
        self.assertEqual(Subscription.objects.first().course, self.course)

    def test_subscription_list(self):
        Subscription.objects.create(user=self.user, course=self.course)

        response = self.client.get("/subscriptions/")

        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        subscriptions = response.json()
        self.assertGreater(len(subscriptions), 0)


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@mail.ru")
        self.course = Course.objects.create(title="Python")
        self.lesson = Lesson.objects.create(
            title="drf", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_create(self):
        url = reverse("school:lessons_create")
        data = {"title": "drf", "course": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_retrieve(self):
        url = reverse("school:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_delete(self):
        url = reverse("school:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("school:lessons_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
