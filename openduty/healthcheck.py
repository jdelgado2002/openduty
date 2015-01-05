__author__ = 'deathowl'

from time import sleep
import datetime
from openduty.serializers import NoneSerializer
from openduty.models import Incident
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .celery import add
from random import randint



class HealthCheckViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = NoneSerializer

    def list(self, request):
        try:
           firstincident = Incident.objects.first()
        except Exception:
            return Response("FAILED", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response("OK", status=status.HTTP_200_OK)

class CeleryHealthCheckViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = NoneSerializer

    def list(self, request):
        try:
            random1 = randint(1, 100)
            random2 = randint(101, 200)
            result = add.apply_async(args=[random1, random2],
                                     expires=datetime.datetime.now() + datetime.timedelta(seconds=3), connect_timeout=3)
            now = datetime.datetime.now()
            while (now + datetime.timedelta(seconds=5)) > datetime.datetime.now():
                if result.result == random1 + random2:
                    return Response("OK", status=status.HTTP_200_OK)
                sleep(0.5)
        except IOError:
            pass
        return Response("FAILED", status=status.HTTP_500_INTERNAL_SERVER_ERROR)