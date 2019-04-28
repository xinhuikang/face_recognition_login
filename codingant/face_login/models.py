from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Faces(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='姓名')
    face_img = models.ImageField(null=True)  # models.TextField()# models.BinaryField(max_length=128)
