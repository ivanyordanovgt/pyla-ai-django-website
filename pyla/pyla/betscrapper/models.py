from django.db import models


# Create your models here.

class BetMatch(models.Model):
    BOOKMAKER_MAX_LENGTH = 100
    SPORT_MAX_LENGTH = 100
    DATE_STRING_MAX_LENGTH = 20
    TIME_STRING_MAX_LENGTH = 20
    MATCH_ONE_MAX_LENGTH = 100
    MATCH_TWO_MAX_LENGTH = 100
    BET_TYPE_MAX_LENGTH = 100
    ODDS_MAX_LENGTH = 50
    LIGA_MAX_LENGTH = 100

    bookmaker = models.CharField(max_length=BOOKMAKER_MAX_LENGTH)
    sport = models.CharField(max_length=SPORT_MAX_LENGTH)
    date = models.CharField(max_length=DATE_STRING_MAX_LENGTH)
    time = models.CharField(max_length=TIME_STRING_MAX_LENGTH)
    match_one = models.CharField(max_length=MATCH_ONE_MAX_LENGTH)
    match_two = models.CharField(max_length=MATCH_TWO_MAX_LENGTH)
    bet_type = models.CharField(max_length=BET_TYPE_MAX_LENGTH)
    odds = models.FloatField()
    liga = models.CharField(max_length=LIGA_MAX_LENGTH)

    def __str__(self):
        return f"{self.match_one} vs {self.match_two}"