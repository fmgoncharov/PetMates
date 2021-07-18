from django.db import models
from django.contrib.auth.models import User


class UserPreferences(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    cat_pref = models.TextField()
    num_pref = models.TextField()
