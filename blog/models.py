from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    DOB = models.DateField()
    address = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    profile_pic = models.ImageField(upload_to='profileimg',null=True)


class UserBlog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Topic = models.CharField(max_length=100)
    caption = models.CharField(max_length=100)
    image = models.ImageField(upload_to='blogimg')
    blog_data = models.CharField(max_length=800)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(null=True)



# my model data
# my name is darsana Sandeep
# hello world