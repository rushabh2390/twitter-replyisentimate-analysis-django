# twitter-replyisentimate-analysis-django
## Generate Twitter developer app tokens.
---
1. Activate your twitter account to developer twitter account one.
2. Make Elevated project to get reply. 
> If essential project is there you are not allowed to get reply of tweet
3. please generate the consumer key , secret key access token access secret token for app. Make twitterconfig.py inside the tweetreplyanalysis directory and add value as given below
```
consumer_key = 'xxxxxx'
consumer_secret = 'xxxxxx'
access_token = 'xxxxxx'
access_token_secret = 'xxxxxx'
```
## Run Locally  
1. clone this repo.
2. Go to Project Directory twittersentimateanalysis/ in terminal. 
3. Activate virtual environment  by typing below function.
```
pipenv shell
```
4. Install dependency list.
```
pip install -r requiremenets.txt
```
Here we are using celery, redis celery-beat for eunning reply nalysis task asynchronously.
5. create a superuser
```
python manage.py createsuperuser
```
6. How to install and run redis please refere: [celery-redis-django](https://www.codingforentrepreneurs.com/blog/celery-redis-django)

7. After install  and run redis please type following 2 command in 2 seperate terminal.
```
celery -A twittersentimateanalysis worker -l info -P gevent

celery -A twittersentimateanalysis beat -l info
```
> if you gevent is   not installed please installed it with ``` pip install gevent ```

8. Now run this project with.
```
python manage.py runservere
```
Please create a new user and from going [register](http://localhost:8000/register)  and [login](http://localhost:8000/login)

9. On [Index](http://localhost:8000/index) page you will have one form whihc take twitter URL for which replies you want sentiment analysis. 

## Run in Docker
---
1. clone this repo.
2. Go to Project Directory in terminal.
3. Run following command.
```
docker-compose up -d
```