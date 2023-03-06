from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from login import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string



def home(request):
    return render(request,"authentication/index.html")

def signup(request):
    if request.method == "POST":
        #username = request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request,"Username already exist! Please try another Username")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request,"Email already registered!")
            return redirect('home')
        
        if len(username)>10:
            messages.error(request,"Username must be under 10 characters ")
            
        if pass1 != pass2:
            messages.error(request,"Password didn't match")
        
        if not username.isalnum():
            messages.error(request,"Username must be in Alpha-Numeric!")
            return redirect('home')
            
    
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()

        messages.success(request,"Your Account has been Sucessfully Created. We have sent you a confirmation email, please confirm your email in order to activate your account!!")

       

        return redirect('signin')


    return render(request,"authentication/signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname':fname})
        
        else:
            messages.error(request,"Bad Credentials!")
            return redirect('home')

    return render(request,"authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"Logged Out Successfully")
    return redirect('home')

def workout(request):
    return render(request,"authentication/workout.html")



# Create your views here
