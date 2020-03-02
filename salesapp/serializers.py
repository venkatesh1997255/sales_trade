# Python imports

# Third party Imports

# DRF Imports
from rest_framework import serializers

# Django imports

# Local Imports
from salesapp.models import Sales


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = ['date', 'open', 'high', 'low', 'close', 'shares_traded', 'turnover']


class BulkUploadSerializer(serializers.Serializer):
    source = serializers.URLField()


class DateStampSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
