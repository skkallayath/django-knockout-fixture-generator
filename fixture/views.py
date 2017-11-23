from django.template import loader
from django.http import HttpResponse
from .models import Fixture
# Create your views here.

def index(request, fixture_id):
    fixture = Fixture.objects.filter(id=fixture_id).get()
    template = loader.get_template('fixture/fixture.html')
    context = {
        'fixture': fixture,
    }
    return HttpResponse(template.render(context, request))

    

def json(request, fixtureId):
    fixture = Fixture.objects.filter(id=fixtureId).get()
    if not fixture:
        return None

    

