from django.db import models
import datetime
from django.core.validators import MinValueValidator
# Create your models here.


class Fixture(models.Model):
    pub_date = models.DateTimeField('date published', null=True)
    icon = models.ImageField(upload_to='static/icons',
                             verbose_name='image',)
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True, default='', null=True)
    rounds = models.IntegerField(default=0)

    start_date = models.DateField('Start date')
    matches_per_day = models.PositiveIntegerField(
        validators=[MinValueValidator(1)])

    @property
    def icon_url(self):
        if self.icon:
            return self.icon.url
        return '/static/img/icons/fixture.png'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        pub_date = datetime.datetime.utcnow()
        super(Fixture, self).save(*args, **kwargs)


class Player(models.Model):
    class Meta:
        unique_together = (('rank', 'fixture'))
    rank = models.IntegerField()
    fixture = models.ForeignKey(Fixture, related_name="players")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Match(models.Model):
    class Meta:
        verbose_name_plural = "Matches"

    @property
    def description(self):
        return repr(self)

    @property
    def name(self):
        if self.match_number:
            return "{} - Match {}".format(self.fixture.name, self.match_number)
        else:
            return "{}".format(self.fixture.name)

    MATCH_STATUS = [
        ("BYE", 'BYE'),
        ("Not Scheduled", 'Not Scheduled'),
        ("Scheduled", "Scheduled"),
        ('Finished', 'Finished')
    ]
    date = models.DateField('Match Date', null=True, blank=True)
    match_number = models.IntegerField(blank=True, null=True)
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

    player_1_score = models.PositiveIntegerField(null=True, blank=True)
    player_2_score = models.PositiveIntegerField(null=True, blank=True)

    winner = models.ForeignKey(
        Player, blank=True, null=True, related_name="matches_won")

    def __str__(self):
        return "{}: {}".format(self.name, self.description)

    def __repr__(self):
        if self.status == 'Finished':
            return "{} {} vs {} {}".format(self.player_1, self.player_1_score, self.player_2, self.player_2_score)

        _right = "BYE"
        _left = "BYE"
        if self.player_1:
            _left = "{}".format(self.player_1)
        elif self.left_previous:
            _left = "Winners (Match {})".format(self.left_previous.match_number)

        if self.player_2:
            _right = "{}".format(self.player_2)
        elif self.right_previous:
            _right = "Winners (Match {})".format(self.right_previous.match_number)

        if _right == "BYE" and _left == "BYE":
            _right = "TBD"
            _left = "TBD"

        return "{} vs {}".format(_left, _right)

    def save(self, *args, **kwargs):
        self.status = "Not Scheduled"
        self.winner = None

        if self.player_1 and self.player_2:
            self.status = 'Scheduled'
            self.player_1_score = self.player_1_score or 0
            self.player_2_score = self.player_2_score or 0

            if self.player_1_score == self.player_2_score:
                self.player_1_score = None
                self.player_2_score = None
                self.winner=None
            elif self.player_1_score > self.player_2_score:
                self.winner = self.player_1
                self.status = "Finished"
            else:
                self.winner = self.player_2
                self.status = "Finished"


        elif self.player_1 or self.player_2:
            self.player_1_score = None
            self.player_2_score = None
            if not (self.player_1 or self.left_previous):
                self.status = 'BYE'
                self.winner = self.player_2
            elif not (self.player_2 or self.right_previous):
                self.status = 'BYE'
                self.winner = self.player_1

        super(Match, self).save(*args, **kwargs)

        if self.winner:
            try:
                _next_left = self.left_next_match
                if _next_left:
                    _next_left.player_1 = self.winner
                    _next_left.save()
            except:
                pass
            try:
                _next_right = self.right_next_match
                if _next_right:
                    _next_right.player_2 = self.winner
                    _next_right.save()
            except:
                pass

    def is_bye(self):
        return self.status == 'BYE', self.player_1 or self.player_2
