from django.shortcuts import render
from .models import Fixture
# Create your views here.

def index(request):
    pass

def json(request, fixtureId):
    fixture = Fixture.objects.filter(id=fixtureId).get()
    if not fixture:
        return None

    

