from django.shortcuts import redirect, render

from .models import User
from .forms import UsersForm, LoginForm

# Create your views here.
def signup_view(request):
    context ={}
    error_message = None
    success_message = None
    if request.method == 'POST':
        form = UsersForm(request.POST)
        if form.is_valid():
            email = form["userEmail"].value()
            user =User.get_user(email)
            if user:
                error_message ="Email is already exist"
            else:
                form.save()
                success_message = "Registration is Sucessfully"
    else:
        form = UsersForm(None)
    
    context['form'] = form
    context["errors"] = error_message
    context["success"] = success_message
    return render(request, "users/signup.html",context)

def login_request(request):
    context ={}
    form = LoginForm(request.POST or None)
    error_message =None
    if form.is_valid():
        email = form["userEmail"].value()
        password = form["userPwd"].value()
        user = User.get_user_for_login(email,password)
        if user:
            request.session['user_id'] = user.userID
            request.session['user_email'] = user.userEmail
            request.session['user_name'] = user.userFirstName+ " " + user.userLastName
            return redirect("index")
        else:
            error_message ="Email or password is incorrect"
        
    
    context['form'] = form
    context["error"] = error_message
    return render(request, "users/login.html",context)

def logout_request(request):
    if request.session.get('user_id', False):
        del request.session["user_id"]
        del request.session["user_email"]
        return redirect("login")