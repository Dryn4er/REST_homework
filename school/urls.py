from django.urls import path
from rest_framework.routers import SimpleRouter

from school.apps import SchoolConfig
from school.views import (CourseViewSet, LessonCreateApiView,
                          LessonDestroyApiView, LessonListApiView,
                          LessonRetrieveApiView, LessonUpdateApiView, SubscriptionCreateAPIView,
                          SubscriptionListAPIView, )

app_name = SchoolConfig.name

router = SimpleRouter()
router.register("courses", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListApiView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>/", LessonRetrieveApiView.as_view(), name="lessons_retrieve"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lessons_create"),
    path("lessons/<int:pk>/delete/", LessonDestroyApiView.as_view(), name="lessons_delete"),
    path("lessons/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lessons_update"),
    path('subscription/create/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
    path('subscription/', SubscriptionListAPIView.as_view(), name='subscription_list'),
]

# Добавляем маршруты из SimpleRouter
urlpatterns += router.urls