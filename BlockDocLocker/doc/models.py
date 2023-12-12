from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    uname= models.ForeignKey(User, on_delete=models.CASCADE)
    document= models.CharField(max_length=100)
    uid=models.CharField(max_length=100)
    date_posted=models.DateTimeField(default= timezone.now)


class DummyModel(models.Model):
    pass
