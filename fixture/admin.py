from django.contrib import admin
from .models import Player, Fixture, Match
from .utils import genearte_random_string
from django.http import HttpResponseRedirect
import math

# Register your models here.

def create_fixture(modeladmin, request, queryset):
    fixture = Fixture(name=genearte_random_string())
    fixture.save()
    for player in queryset:
        fixture.players.add(player)
    fixture.save()
    create_schedules(fixture)
    return HttpResponseRedirect("/admin/fixture/fixture/%d/change/" % (fixture.pk))

def create_schedules(fixture):
    _player_list = list(fixture.players.all())
    _len = len(_player_list)
    _rounds = int(math.ceil(math.log(_len, 2)))
    _number_of_players = int(math.pow(_rounds, 2))
    print(_len, _number_of_players, _rounds)
    _players = _player_list + ([None]*(_number_of_players - _len))

    print(_players)
    _matches = []
    _counter = 1
    _round = 1
    for i in range(_number_of_players//2):
        _match = Match()
        _match.fixture = fixture
        _match.match_round = _round
        _match.player_1 = _players[i]
        _match.player_2 = _players[-1-i]

        if _match.player_1 and _match.player_2:
            _match.match_number = _counter
            _counter = _counter+1

        _match.save()

        _matches.append(_match)
    
    generate_next_rounds(fixture, _matches, _round+1, _counter)

def generate_next_rounds(fixture, matches, _round, counter):
    _matches = []
    _len = len(matches)
    if _len <=1:
        return
    for i in range(_len//2):
        _match = Match()
        _match.fixture = fixture
        _match.match_round = _round
        _match.left_previous = matches[i]
        _match.right_previous = matches[-1-i]

        _left_bye, _left_winner = _match.left_previous.is_bye()
        if _left_bye:
            _match.player_1 = _left_winner
        _right_bye, _right_winner = _match.right_previous.is_bye()
        if _right_bye:
            _match.player_2 = _right_winner

        _match.match_number = counter
        counter = counter+1

        _match.save()

        _matches.append(_match)
    
    generate_next_rounds(fixture, _matches, _round+1, counter)

create_fixture.short_description = "Create knockout fixture"

class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']
    actions = [create_fixture]

class MatchAdmin(admin.ModelAdmin):
    readonly_fields = ('match_number','fixture','match_round', 'left_previous','right_previous','player_1', 'player_2', 'status','winning_palyer',  )
    fields = ('match_number',  'player_1', 'player_2','match_round', 'status','winner', 'winning_palyer', )
    def has_add_permission(self, request):
        return False

    can_delete = False

class MatchInline(admin.TabularInline):
    model = Match
    ordering = ['match_number']
    readonly_fields = ('match_number','fixture','match_round', 'left_previous','right_previous','player_1', 'player_2', 'status','winning_palyer',  )
    fields = ('match_number',  'player_1', 'player_2','match_round', 'status','winner', 'winning_palyer', )
    can_delete = False
    def has_add_permission(self, request):
        return False

class FixtureAdmin(admin.ModelAdmin):
    readonly_fields = ('players',)
    fields = ('name', 'description', 'players', )
    inlines = [
        MatchInline,
    ]
    def has_add_permission(self, request):
        return False

admin.site.register(Player, PlayerAdmin)
admin.site.register(Match, MatchAdmin)

admin.site.register(Fixture, FixtureAdmin)