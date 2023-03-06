from rest_framework import serializers
from .models import Book
from .models import Follow


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "description"]


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "is_follow" "user", "book"]
        read_only_fields = ["id", "user", "book"]
