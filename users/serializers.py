from .models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from books.serializers import FollowSerializer


class UserSerializer(serializers.ModelSerializer):
    is_follow = FollowSerializer(read_only=True,many=True)
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_colaborator",
            "is_blocked",
            "is_follow",
        ]
        read_only_fields = ["id", "is_follow"]
        extra_kwargs = {
            "username": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="A user with that username already exists.",
                    )
                ]
            },
            "email": {
                "required": True,
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="A user with that email already exists.",
                    )
                ],
            },
            "password": {"write_only": True},
        }


    def create(self, validated_data: dict) -> User:
        if validated_data["is_colaborator"]:
            return User.objects.create_superuser(**validated_data)
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.set_password(validated_data.get("password"))
        instance.save()
        return instance
