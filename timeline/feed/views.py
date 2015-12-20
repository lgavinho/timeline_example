from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from models import Notification
from serializers import NotificationSerializer
import stream


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def notification(request):
    """
    List all notification, or create a new.
    """
    if request.method == 'GET':
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = NotificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            # Initialize the client with your api key and secret
            client = stream.connect('bnk64gtyrsdw', 'bnk64gtyrsdw_SECRET')
            # For the feed group 'user' and user id 'eric' get the feed
            eric_feed = client.feed('user', serializer.actor)
            # Add the activity to the feed
            eric_feed.add_activity({'actor': serializer.actor, 'verb': serializer.verb, 'object': serializer.object,
                                    'tweet': serializer.text
                                    })

            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def notification_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        notification = Notification.objects.get(pk=pk)
    except Notification.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = NotificationSerializer(notification)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = NotificationSerializer(notification, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        notification.delete()
        return HttpResponse(status=204)
