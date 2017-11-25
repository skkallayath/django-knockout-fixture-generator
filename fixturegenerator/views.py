from django.http import HttpResponse
from django.template import loader

from fixture.models import Fixture, Match


def index(request):
    fixture_list = Fixture.objects.order_by('-pub_date')
    match_list = []
    for fixture in fixture_list:
        matches = {}
        matches['fixture'] = fixture
        matches['matches'] = Match.objects.filter(fixture=fixture, status ="Scheduled").order_by('-date').all()
        match_list.append(matches)
    template = loader.get_template('fixture/index.html')
    context = {
        'fixture_list': fixture_list,
        'match_list': match_list,
    }
    return HttpResponse(template.render(context, request))