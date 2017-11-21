from django.db import models
from django.http import HttpResponseRedirect

# Create your models here.


class Player(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Fixture(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1024, blank=True, default='', null=True)
    players = models.ManyToManyField(Player)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        super(Fixture, self).save(*args, **kwargs)

        return HttpResponseRedirect("/admin/fixture/fixture/%d/change/" % (self.pk))


class Match(models.Model):
    class Meta:
        verbose_name_plural = "Matches"

    MATCH_STATUS = [
        ("BYE", 'BYE'),
        ("Not Scheduled", 'Not Scheduled'),
        ("Scheduled", "Scheduled"),
        ('Finished', 'Finished')
    ]
    MATCH_WINNERS = [
        ("Player 1", "Player 1"),
        ("Player 2", "Player 2")
    ]
    match_number = models.IntegerField(blank=True, default=0)
    fixture = models.ForeignKey(Fixture, related_name="matches")
    match_round = models.IntegerField()
    left_previous = models.OneToOneField(
        'self', blank=True, null=True, related_name="left_next_match")
    right_previous = models.OneToOneField(
        'self', blank=True, null=True, related_name="right_next_match")

    player_1 = models.ForeignKey(
        Player, blank=True, null=True, related_name="left_matches")
    player_2 = models.ForeignKey(
        Player, blank=True, null=True, related_name="right_matches")

    status = models.CharField(
        max_length=20, choices=MATCH_STATUS, default='Not Scheduled')

    winner = models.CharField(max_length=20, choices=MATCH_WINNERS, blank=True)

    winning_palyer = models.ForeignKey(
        Player, blank=True, null=True, related_name="matches_won")

    def __str__(self):
        _right = "BYE"
        _left = "BYE"
        if self.player_1:
            _left = "{}".format(self.player_1)
        elif self.left_previous:
            _left = "Winners ({})".format(self.left_previous)
        
        if self.player_2:
            _right = "{}".format(self.player_2)
        elif self.right_previous:
            _right = "Winners ({})".format(self.right_previous)
        
        if _right == "BYE" and _left == "BYE":
            _right = "TBD"
            _left = "TBD"

        return "Round {}: {} vs {}".format(self.match_round, _left, _right)

    def save(self, *args, **kwargs):
        self.status = "Not Scheduled"
        self.winning_palyer = None

        if self.player_1 and self.player_2:
            self.status = 'Scheduled'
            if self.winner == 'Player 1':
                self.winning_palyer = self.player_1
                self.status = "Finished"
            elif self.winner == 'Player 2':
                self.winning_palyer = self.player_2
                self.status = "Finished"
        elif self.player_1 or self.player_2:
            if not (self.player_1 or self.left_previous):
                self.status = 'BYE'
                self.winner = 'Player 2'
                self.winning_palyer = self.player_2
            elif not (self.player_2 or self.right_previous):
                self.status = 'BYE'
                self.winner = 'Player 1'
                self.winning_palyer = self.player_1
        
        super(Match, self).save(*args, **kwargs)

        if self.winning_palyer:
            try:
                _next_left = self.left_next_match
                if _next_left:
                    _next_left.player_1 = self.winning_palyer
                    _next_left.save()
            except:
                pass
            try:
                _next_right = self.right_next_match
                if _next_right:
                    _next_right.player_2 = self.winning_palyer
                    _next_right.save()
            except:
                pass

    def is_bye(self):
        return self.status == 'BYE', self.player_1 or self.player_2

