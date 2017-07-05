from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    HEARTHSTONE = 1
    WOW = 2
    HOTS = 3
    GAME_TYPES = (
        (HEARTHSTONE, 'Hearthstone'),
        (WOW, 'WOW'),
        (HOTS, 'HOTS'),
    )
    
    title = models.CharField(max_length=50)
    publication_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User)
    # author = models.CharField(max_length=30, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    pages = models.IntegerField(blank=True, null=True)
    game_type = models.PositiveSmallIntegerField(choices=GAME_TYPES)