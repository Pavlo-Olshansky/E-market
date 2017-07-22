from django.db import models

class Contact_us(models.Model):
    user = models.CharField(max_length=250)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'User "{}" on "{}"'.format(self.user, self.created)

class Support(models.Model):
	PROBLEMS= (
		(1, "I can't log in"),
		(2, "I can't sign up"),
		(3, "I can't pay for account"),
		(4, 'Another (I will write it)'),
	)
	problem = models.PositiveSmallIntegerField(choices=PROBLEMS)

	user = models.CharField(max_length=250)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return 'Support from user "{}" on "{}"'.format(self.user, self.created)

