from django.shortcuts import render, redirect
from numpy import negative
from requests import session
from .forms import TweetUrlForm
from .models import TwitterData
from users.models import User
from .tasks import tweetanalysis
import json

# Create your views here.

def dashboard(request):
    if request.session.get('user_id', False):
        context ={}
        error_message = None
        success_message = None
        user = User.get_user(request.session['user_email'])
        if request.method == 'POST':
            form = TweetUrlForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj = form.save(commit=False)
              
                obj.request_user_id = user
                obj.save()
                success_message = "Url added Sucessfully"
            else:
                error_message ="please enter valid Url"
        else:
            form = TweetUrlForm(None)
        
        data = TwitterData.get_user_tweet_data(user.userID)
        if data:
            context["tweet_data"] = data
        else:
            context["message"] = "No tweet Url for analysis yet"
        context['form'] = form
        context["errors"] = error_message
        context["success"] = success_message
        return render(request, "tweetsreplyanalysis/index.html",context)
    return redirect("login")
    
def summary(request):
    if request.session.get('user_id', False):
        context ={}
        tweet_id = request.GET.get("tweet_id",None)
        if tweet_id:
            print(tweet_id)
            data = TwitterData.get_tweet_data_from_id(tweet_id)
        if data:
                summary_data_list = json.loads((data.twitter_replies_texts_classification.replace("'",'"')))
                summary_data_list = sorted(summary_data_list, key=lambda d: d['sentiment']) 
                positive_summary = []
                negative_summary = []
                neutral_summary = []
                for reply_summary in summary_data_list :
                    if reply_summary["sentiment"] == "Positive":
                        positive_summary.append(reply_summary["text"])
                    elif reply_summary["sentiment"] == "Negative":
                        negative_summary.append(reply_summary["text"])
                    elif reply_summary["sentiment"] == "Neutral":
                        neutral_summary.append(reply_summary["text"])
                
                context["tweet_data"] = data
                context["positive_data"] = positive_summary
                context["negative_data"] = negative_summary
                context["neutral_data"] = neutral_summary
                return render(request, "tweetsreplyanalysis/analysis_details.html",context)
        else:
            return redirect("index")
            
    return redirect("login")