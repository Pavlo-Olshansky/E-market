from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    image = models.ImageField(upload_to='profile_image', blank=True, default='no_profile.jpg')

    def __str__(self):
    	return self.user.username


# @receiver(post_save, sender=User)
def create_user_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])
    # if created:
    #     user_profile = UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(save_user_profile, sender=User)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
    # instance.profile.save()
