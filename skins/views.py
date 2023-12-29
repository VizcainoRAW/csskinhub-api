from django.shortcuts import render
from rest_framework import viewsets
from skins.models import Case
from skins.serializer import CaseSerializer

class CaseView(viewsets.ModelViewSet):
    serializer_class = CaseSerializer
    queryset = Case.objects.all()