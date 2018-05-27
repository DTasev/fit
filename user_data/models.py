from django.contrib.auth.models import User
from django.db import models


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="details")
    weight = models.FloatField("Weight", null=True)
