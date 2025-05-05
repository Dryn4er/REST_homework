from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from school.models import Course, Lesson, Subscription
from school.validators import VideoLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "description", "picture", "course", "video_url"]
        validators = [VideoLinkValidator(field='video_link')]


class CourseSerializer(serializers.ModelSerializer):
    count_of_lessons = serializers.SerializerMethodField()
    info_lessons = LessonSerializer(source='lesson_set', many=True)

    def get_count_of_lessons(self, obj):
        return obj.lesson_set.count()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "description",
            "preview",
            "count_of_lessons",
            "info_lessons",
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class CourseDetailSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()

    def get_count_lessons(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_subscription(self, course):
        user = self.context.get('request').user
        course = self.context.get('view').kwargs.get('pk')
        subscription = Subscription.objects.filter(user=user, course=course)
        if subscription.exists():
            return True
        else:
            return False

    class Meta:
        model = Course
        fields = ('title', 'description', 'count_lessons')


class LessonDetailSerializer(serializers.ModelSerializer):
    count_lesson_with_same_course = SerializerMethodField()