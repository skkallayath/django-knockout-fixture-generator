from django.template import loader
from django.http import HttpResponse
from .models import Fixture
from django.db.models import Q

# Create your views here.


def index(request, fixture_id):
    fixture = Fixture.objects.filter(id=fixture_id).prefetch_related(
        "matches").prefetch_related("players").get()
    fixture.match_list = fixture.matches.filter(
        ~Q(status="BYE")).order_by("id")
    fixture.player_list = fixture.players.order_by("rank")
    template = loader.get_template('fixture/fixture.html')
    context = {
        'fixture': fixture,
    }
    return HttpResponse(template.render(context, request))


def json(request, fixtureId):
    fixture = Fixture.objects.filter(id=fixtureId).get()
    if not fixture:
        return None
