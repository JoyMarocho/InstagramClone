from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Image,Comment,Profile

class NewUserForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


    def save(self,commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class UpdateUserForm(forms.ModelForm):
        email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

        class Meta:
            model = User
            fields = ('username', 'email')

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget = forms.TextInput()
        self.fields['comment'].widget.attrs['placeholder'] = 'Add a comment...'

    class Meta:
        model = Comment
        fields = ('comment',)




class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['comments', 'likes', 'profile',]


class ProfileEditForm(forms.ModelForm):
    
        class Meta:
            model = Profile
            fields = ['name', 'location', 'profile_picture', 'bio']


class PostForm(forms.ModelForm):
    
        class Meta:
            model = Post
            fields = ('image', 'caption')