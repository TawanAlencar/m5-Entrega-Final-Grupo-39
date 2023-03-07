from rest_framework import serializers
from .models import Copy
from .models import Lending


class CopySerializer(serializers.ModelSerializer):
    class Meta:
        model = Copy
        fields = ["id", "is_lending", "book"]
        read_only_fields = ["id", "book"]


class LendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lending
        fields = ["id", "is_date", "return_date", "user", "copy"]
        read_only_fields = ["id", "user", "copy"]