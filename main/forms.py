from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Article, Comment

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length = 100)
    last_name = forms.CharField(max_length = 100)

    class Meta:
        model = User
        fields = ["username", "email",  'first_name' , 'last_name',  "password1", "password2"]

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['author', 'title', 'text', 'tags']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

# class TagForm(forms.ModelForm):
#     class Meta:
#         model = Tag
#         fields = ['tag_name']
