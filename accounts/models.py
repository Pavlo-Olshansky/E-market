from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

import stripe


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    file = models.ImageField(upload_to='profile_image/', blank=True, default='profile_image/no_profile.jpg')

    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['username', 'email']

    def __str__(self):
    	return self.user.username

    def charge(self, request, email, fee):
        # Set your secret key: remember to change this to your live secret key
        # in production. See your keys here https://manage.stripe.com/account
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Get the credit card details submitted by the form
        token = request.POST['stripeToken']

        # Create a Customer
        stripe_customer = stripe.Customer.create(
            card=token,
            description=email
        )

        # Save the Stripe ID to the customer's profile
        self.stripe_id = stripe_customer.id
        self.save()

        # Charge the Customer instead of the card
        stripe.Charge.create(
            amount=fee, # in cents
            currency="usd",
            customer=stripe_customer.id
        )

        return stripe_customer


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile, created = UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
    instance.userprofile.save()
