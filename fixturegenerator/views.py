from django.http import HttpResponse
from django.template import loader

from fixture.models import Fixture


def index(request):
    fixture_list = Fixture.objects.order_by('-pub_date')
    template = loader.get_template('fixture/index.html')
    context = {
        'fixture_list': fixture_list,
    }
    return HttpResponse(template.render(context, request))