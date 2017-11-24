from django.template import loader
from django.http import HttpResponse
from .models import Fixture
from django.db.models import Q
import json

# Create your views here.


def index(request, fixture_id):
    fixture = Fixture.objects.filter(id=fixture_id).prefetch_related(
        "matches").prefetch_related("players").get()
    fixture.match_list = fixture.matches.filter(
        ~Q(status="BYE")).order_by("id")
    fixture.player_list = fixture.players.order_by("rank")
    teams, results = get_bracket_info(fixture)
    template = loader.get_template('fixture/fixture.html')
    context = {
        'fixture': fixture,
        'teams':json.dumps(teams),
        'results': json.dumps(results)
    }
    return HttpResponse(template.render(context, request))

def get_bracket_info(fixture):
    results = []
    teams = list(map(lambda x: x.get_player_names(), fixture.matches.filter(match_round=1).order_by('id')))

    for r in range(1, fixture.rounds+1):
        results.append(list(map(lambda x: x.get_result_values(), fixture.matches.filter(match_round=r).order_by('id'))))
    
    return teams, results