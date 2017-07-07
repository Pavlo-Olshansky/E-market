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
    price = models.DecimalField(max_digits=7, decimal_places=1)
    game_type = models.PositiveSmallIntegerField(choices=GAME_TYPES)
    is_accepted = models.BooleanField(default=False)

    def accept(self):
        self.is_accepted = True

    class Meta:
        ordering = ['publication_date']

class Comment(models.Model):
    game = models.ForeignKey(Game, related_name='comments')
    user = models.CharField(max_length=250)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def approved(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.user