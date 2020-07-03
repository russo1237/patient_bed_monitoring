from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfileInfo(models.Model):
    #relationship with user
    user = models.OneToOneField(User,on_delete=models.CASCADE,)
    #additonal parameters needed
    hospital_name = models.CharField(max_length=40)
    address = models.CharField(max_length=70)

    def __str__(self):
        return self.user.username
