from rest_framework import serializers
from .models import Copy
from .models import Lending
from books.models import Book
import datetime
from django.shortcuts import get_object_or_404


class CopySerializer(serializers.ModelSerializer):
    class Meta:
        model = Copy
        fields = ["id", "is_lending", "book"]
        read_only_fields = ["id", "book"]

    def create(self, validated_data: dict):
        return Copy.objects.create(**validated_data)


class LendingSerializer(serializers.ModelSerializer):
    return_date = serializers.SerializerMethodField()
    copy = CopySerializer(read_only=True)

    class Meta:
        model = Lending
        fields = ["id", "is_date", "return_date", "user", "copy"]
        read_only_fields = ["id", "user", "copy"]

    def create(self, validated_data: dict):
        copy = get_object_or_404(Copy, id=validated_data["copy_id"])

        if copy.is_lending == True:
            raise serializers.ValidationError("message: This copy has been lending")

        copy.is_lending = True
        copy.save()
        lending = Lending.objects.create(**validated_data)
        return lending

    def get_return_date(self, obj):
        obj.return_date = obj.return_date + datetime.timedelta(days=4)
        obj.save()

        if obj.return_date.weekday() == 6:
            obj.return_date = obj.return_date + datetime.timedelta(days=1)
            obj.save()

        if obj.return_date.weekday() == 5:
            obj.return_date = obj.return_date + datetime.timedelta(days=2)
            obj.save()

        return obj.return_date
