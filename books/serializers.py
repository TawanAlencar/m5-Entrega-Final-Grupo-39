from .models import Book
from .models import Follow
from rest_framework import serializers
from users.serializers import UserSerializer
from rest_framework.validators import UniqueValidator


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "description", "followers"]
        depth=1
        extra_kwargs = {
            "title": {
                "validators": [
                    UniqueValidator(
                        queryset=Book.objects.all(),
                        message="A book with that title already exists.",
                    )
                ]
            }
        }


class FollowSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ["id", "user", "book"]
        read_only_fields = ["id", "user", "book"]
