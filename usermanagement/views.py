from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('main:index')
        else:
            # Return an 'invalid login' error message.
            messages.success(request,"There was an error logging in, please try again.")
            return redirect('usermanagement:login')
    else:
        return render(request, 'authentication/login.html')

def logout_user(request):
        print('User logged out')
        logout(request)
        print('User logged out')
        messages.success(request,"Logout successful!")
        return redirect('usermanagement:login')