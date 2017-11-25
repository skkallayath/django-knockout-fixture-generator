from django.contrib import admin
from .models import Player, Fixture, Match
from .utils import genearte_random_string
import math
from datetime import timedelta
from django.contrib import messages

# Register your models here.
def generate_schedules(modeladmin, request, queryset):
    for fixture in queryset:
        fixture.matches.all().delete()
        fixture.save()
        create_schedules(fixture)
        messages.add_message(request, messages.SUCCESS, 'Fixture generated for {}.'.format(fixture))

def create_schedules(fixture):
    _player_list = list(fixture.players.order_by('rank'))
    _len = len(_player_list)
    if _len == 0:
        return
    fixture.rounds = int(math.ceil(math.log(_len, 2)))
    fixture.save()

    _number_of_players = int(math.pow(2, fixture.rounds))
    _players = _player_list + ([None]*(_number_of_players - _len))

    _date = fixture.start_date
    _matches = []
    _counter = 1
    _round = 1
    for i in range(_number_of_players//2):
        _match = Match()
        _match.fixture = fixture
        _match.match_round = _round
        if _players[i]:
            _match.player_1 = _players[i]
        if _players[-1-i]:
            _match.player_2 = _players[-1-i]

        if _match.player_1 and _match.player_2:
            _match.match_number = _counter
            _match.date = _date
            if _counter%fixture.matches_per_day ==0:
                print("date change",_counter)
                _date = _date + timedelta(days=1)
            print(_counter)
            _counter = _counter+1

        _match.save()

        _matches.append(_match)

    generate_next_rounds(fixture, _matches, _round+1, _counter, _date + timedelta(days=1))

def generate_next_rounds(fixture, matches, _round, counter, _date):
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
        _match.date = _date
        if counter%fixture.matches_per_day == 0:
            print("date change", counter)
            _date = _date + timedelta(days=1)
        print(counter)
        counter = counter+1

        _match.save()

        _matches.append(_match)
    
    generate_next_rounds(fixture, _matches, _round+1, counter, _date + timedelta(days=1))

generate_schedules.short_description = "Generate knockout fixture"

class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'rank', 'fixture']
    ordering = ['name']

class MatchAdmin(admin.ModelAdmin):
    readonly_fields = ('description', 'name', 'match_number','fixture','match_round', 'left_previous','right_previous','player_1', 'player_2', 'status','winner',)
    fields = ('date', 'name', 'description', 'fixture', 'match_number',  'player_1', 'player_2','match_round', 'status','winner', 'player_1_score', 'player_2_score', )
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        print(actions.items())
        return actions

class MatchInline(admin.TabularInline):
    model = Match
    ordering = ['match_number',]
    readonly_fields = ('description', 'match_number','fixture','match_round', 'left_previous','right_previous','player_1', 'player_2', 'status','winner',  )
    fields = ('date', 'description', 'match_number', 'player_1', 'player_2','match_round', 'status','winner','player_1_score', 'player_2_score', )
    can_delete = False
    def has_add_permission(self, request):
        return False

class PlayerInline(admin.TabularInline):
    model = Player
    ordering = ['rank']
    fields = ('name', 'rank', )

class FixtureAdmin(admin.ModelAdmin):
    readonly_fields = ('rounds',)
    fields = ('name', 'description', 'icon', 'start_date', 'matches_per_day', )
    inlines = [
        PlayerInline,
        MatchInline,
    ]
    actions = [generate_schedules]

admin.site.register(Player, PlayerAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Fixture, FixtureAdmin)