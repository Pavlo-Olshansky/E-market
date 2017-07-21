from django.db import models
from django.contrib.auth.models import User

from shortuuidfield import ShortUUIDField

    
class Game(models.Model):
    HEARTHSTONE = 1
    WOW = 2
    HOTS = 3
    GAME_TYPES = (
        (HEARTHSTONE, 'Hearthstone'),
        (WOW, 'WOW'),
        (HOTS, 'HOTS'),
    )
    
    uuid = ShortUUIDField(unique=True)
    title = models.CharField(max_length=50)
    publication_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User)
    buyer = models.ForeignKey(User, related_name='game_buyer', null=True)
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



from paypal.standard.ipn.signals import payment_was_successful, valid_ipn_received
from accounts.tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site             


def Paypal_comfirm(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == "Completed":

        game_id = ipn_obj.invoice
        game = get_object_or_404(Game, pk=game_id)

        # Update a game list without this game
        game.accept()
        game.save() 
        user_author = game.author
        current_user = game.buyer
        user_author.userprofile.money += game.price

        # Send message to seller(request a login and pass)
        current_site = get_current_site(request)
        subject = 'Your account wont to buy!'
        message = render_to_string('products/login_password/login_pass_request_EMAIL.html', {
            'user_author': user_author,
            'current_user': current_user,
            'game': game,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(current_user.pk)),
            'token': account_activation_token.make_token(current_user),
        })
        user_author.email_user(subject, message)

payment_was_successful.connect(Paypal_comfirm)
 
valid_ipn_received.connect(Paypal_comfirm)
