from rest_framework import serializers
import re

class VideoLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if not re.match(r'^https?://(www\.)?youtube\.com/watch\?v=', value):
            raise serializers.ValidationError("Ссылки на сторонние ресурсы, кроме youtube.com, не допускаются.")