from .models import Book
from .models import Follow
from rest_framework import serializers
from users.serializers import UserSerializer
from rest_framework.validators import UniqueValidator
from copies.serializers import CopySerializer
from django.shortcuts import get_object_or_404


class BookSerializer(serializers.ModelSerializer):
    is_avaliable = serializers.SerializerMethodField()
    copies = CopySerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "description",
            "followers",
            "is_avaliable",
            "copies",
        ]

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

    def get_is_avaliable(self, obj):
        copies = obj.copies.all()
        serializer = CopySerializer(copies, many=True)
        counter = 0

        for copy in serializer.data:
            if copy["is_lending"] == False:
                counter += 1

        if counter > 0:
            return True

        return False


class FollowSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ["id", "user", "book"]
        read_only_fields = ["id", "user", "book"]
