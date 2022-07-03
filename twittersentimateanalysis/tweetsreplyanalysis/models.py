from operator import truediv
from django.db import models
from users.models import User

# Create your models here.
class TwitterData(models.Model):
    twitterID = models.BigAutoField(primary_key=True)
    twitter_url = models.URLField()
    twitter_id = models.TextField(null=True,blank=True)
    twitter_replies_number = models.IntegerField(default=0)
    twitter_positive_percentage = models.DecimalField(decimal_places=2,max_digits=4,default=0.0)
    twitter_negative_percentage = models.DecimalField(decimal_places=2,max_digits=4,default=0.0)
    twitter_neutral_percentage = models.DecimalField(decimal_places=2,max_digits=4,default=0.0)
    twitter_replies_texts_classification = models.TextField(blank=True,null=True)
    request_user_id = models.ForeignKey(User,on_delete=models.CASCADE, blank=True,null=True)
    analysis_status = models.TextField(default="Submitted")
    analysis_created_at = models.DateTimeField(auto_now_add = True)
    analysis_updated_at = models.DateTimeField(auto_now = True)

    @staticmethod
    def get_user_tweet_data(user_id):
        try:
            return TwitterData.objects.filter(request_user_id = user_id).values()
        except:
            return False
    @staticmethod
    def get_tweet_data_from_id(sid):
        try:
            return TwitterData.objects.get(twitter_id=sid)
        except:
            return False
        
    @staticmethod
    def get_submitted_url():
        try:
            return TwitterData.objects.filter(analysis_status="Submitted")  
        except:
            return False