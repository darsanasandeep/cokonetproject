from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from blog.models import Profile


class RegisterForm(UserCreationForm):
    class Meta():
        model = User
        fields = ('first_name','last_name','email','username','password1','password2')

class UploadForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ['profile_pic']


