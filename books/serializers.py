from rest_framework import serializers
from .models import Book
from .models import Follow


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "description"]


class FollowSerializer(serializers.ModelSerializer):
    book_info = BookSerializer(read_only=True,source='Follow.all', many=True)

    class Meta:
        model = Follow
        fields = ["id", "user", "book","book_info"]
        read_only_fields = ["id", "user", "book","book_info "]


    