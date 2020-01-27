from rest_framework import serializers
from .models import StatusLog
from django.contrib.auth.models import User


class LogsSerializer(serializers.ModelSerializer):  # create class to serializer model

    class Meta:
        model = StatusLog
        fields = ('msg', 'create_datetime')