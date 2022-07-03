from django import forms
from django.forms import fields
from .models import TwitterData

class TweetUrlForm(forms.ModelForm):

    class Meta:
        model = TwitterData
        fields = ["twitter_url"]
        widgets = {
            'tweetUrl': forms.URLField(),
        },
        labels ={
            'tweetUrl': 'Twitter Url',
        }