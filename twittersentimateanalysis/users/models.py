from django.db import models

# Create your models here.
class User(models.Model):
    userID = models.AutoField(primary_key=True)
    userFirstName = models.CharField(max_length = 200)
    userLastName = models.CharField(max_length = 200)
    userEmail = models.EmailField(max_length= 300)
    userPwd = models.CharField(max_length=200)

    @staticmethod
    def get_user_for_login(email,password):
        try:
            return User.objects.get(userEmail = email,userPwd = password)
        except:
            return False
    
    @staticmethod
    def get_user(email):
        try:
            return User.objects.get(userEmail = email)
        except:
            return False
            
    @staticmethod
    def is_duplicate(email):
        try:
            return User.objects.get(userEmail = email)
        except:
            return False