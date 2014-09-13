from django.db import models

# Create your models here.
from users.models import User


class Event(models.Model):
    url = models.URLField()
    user = models.ForeignKey(User, related_name='user')

    def __unicode__(self):
        return "{} inputted this link: {}".format(self.url, self.user.username)