from django.db import models
from django.contrib.auth.models import User
class Laywer(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    law_firm = models.CharField(max_length=20, null=True)
# Create your models here.
