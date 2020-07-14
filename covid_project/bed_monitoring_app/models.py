from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfileInfo(models.Model):
    #relationship with user
    user = models.OneToOneField(User,on_delete=models.CASCADE,)
    #additonal parameters needed
    hospital_name = models.CharField(max_length=40)
    address = models.TextField(max_length=70)

    def __str__(self):
        return self.user.username

class HospitalBedDetails(models.Model):
    #link to user and hospital is user
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    #parameters needed for hospital details
    total_no_of_beds = models.IntegerField()
    total_govt_beds = models.IntegerField()
    total_hospital_beds = models.IntegerField()
    occupied_govt_beds = models.IntegerField(default=0)
    occupied_hospital_beds = models.IntegerField(default=0)
