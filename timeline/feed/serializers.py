__author__ = 'lgavinho'

from rest_framework import serializers
from models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'actor', 'verb', 'object', 'text')
