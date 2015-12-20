from __future__ import unicode_literals

from django.db import models


class Notification(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    actor = models.CharField(max_length=100, blank=True, default='')
    verb = models.CharField(max_length=100, blank=True, default='')
    object = models.CharField(max_length=100, blank=True, default='')
    text = models.CharField(max_length=250, blank=True, default='')

    class Meta:
        ordering = ('created',)