from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    USER_PROFILE_CHOICES = [
        ('User', 'User'),
        ('Agent', 'Agent'),
    ]
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    image=models.ImageField(default='defalut.jpg', upload_to='profile_pics')
    profile_type = models.CharField(max_length=6, choices=USER_PROFILE_CHOICES)
    def __str__(self):
        return f'{self.user.username} Profile'
