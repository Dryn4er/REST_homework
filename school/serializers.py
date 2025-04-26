from rest_framework import serializers

from school.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "description", "picture", "course", "video_url"]


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