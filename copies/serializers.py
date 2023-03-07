from rest_framework import serializers
from .models import Copy
from .models import Lending
import datetime


class CopySerializer(serializers.ModelSerializer):
    class Meta:
        model = Copy
        fields = ["id", "is_lending", "book"]
        read_only_fields = ["id", "book"]

    def create(self, validated_data: dict):
        return Copy.objects.create(**validated_data)


class LendingSerializer(serializers.ModelSerializer):
    return_date = serializers.SerializerMethodField()

    class Meta:
        model = Lending
        fields = ["id", "is_date", "return_date", "user", "copy"]
        read_only_fields = ["id", "user", "copy"]

    def create(self, validated_data: dict):
        return Lending.objects.create(**validated_data)

    def get_return_date(self, obj):
        obj.return_date = obj.return_date + datetime.timedelta(days=2)

        if obj.return_date.weekday() == 1:
            obj.return_date = obj.return_date + datetime.timedelta(days=1)

        if obj.return_date.weekday() == 7:
            obj.return_date = obj.return_date + datetime.timedelta(days=2)

        return obj.return_date
