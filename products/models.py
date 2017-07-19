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
    price = models.IntegerField()
    game_type = models.PositiveSmallIntegerField(choices=GAME_TYPES)
    is_accepted = models.BooleanField(default=False)

    def accept(self):
        self.is_accepted = True

    def __str__(self):
        return 'Game of user "{}"'.format(self.author, )


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
        return 'User "{}" on game "{}"'.format(self.user, self.game.title)


    class Meta:
        ordering = ['created']


class LoginPassword(models.Model):
    game = models.ForeignKey(Game, related_name='login_password_to_game', null=True)
    owner = models.ForeignKey(User, related_name='login_password_of_user', null=True)

    login = models.CharField(max_length=250)
    password = models.CharField(max_length=250)

    def __str__(self):
        return 'Game "{}" of user "{}"'.format(self.game.title, self.owner)



class Photo(models.Model):
    game = models.ForeignKey(Game, related_name='photos_to_game', null=True)
    file = models.ImageField()
    description = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Photo of game "{}"'.format(self.game.title, )


    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'