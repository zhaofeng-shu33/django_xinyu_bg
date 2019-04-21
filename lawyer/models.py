from django.db import models
from django.contrib.auth.models import User
class Lawyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    law_firm = models.CharField(max_length=20, null=True)
    def __str__(self):
        return self.user.__str__()
