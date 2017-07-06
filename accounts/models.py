from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    file = models.ImageField(upload_to='profile_image/', blank=True, default='profile_image/no_profile.jpg')

    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['username', 'email']

    def __str__(self):
    	return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    user_profile, created = UserProfile.objects.get_or_create(user=instance)

    # if kwargs['created']:
    #     user_profile.set_password(user_profile.password)
        # user_profile = UserProfile.objects.create(user=kwargs['instance'])
    # if created:
    #     user_profile = UserProfile.objects.create(user=instance)

# post_save.connect(create_user_profile, sender=User)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

# post_save.connect(save_user_profile, sender=User)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
    instance.userprofile.save()
# post_save.connect(update_user_profile, sender=User)

