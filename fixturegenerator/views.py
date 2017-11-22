from django.http import HttpResponse
from django.template import loader

from fixture.models import Fixture


def index(request):
    latest_fixture_list = Fixture.objects.order_by('-pub_date')[:5]
    template = loader.get_template('fixture/index.html')
    context = {
        'latest_fixture_list': latest_fixture_list,
    }
    return HttpResponse(template.render(context, request))