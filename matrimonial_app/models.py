from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class regmodel(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    name=models.CharField(max_length=50,default='')
    phone = models.IntegerField()
    dob=models.DateField()
    gender=models.CharField(max_length=20)
    bio=models.CharField(max_length=1000)
    occupation=models.CharField(max_length=100)
    looking_for=models.CharField(max_length=20)
    image=models.ImageField(upload_to='matrimonial_app/static')

    def __str__(self):
        return self.user.username