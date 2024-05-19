from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm


# Create your views here.
def home(request):
    return render(request, 'home.html', {})

# Login
def login_user(request):

    if request.method == 'POST':
        username = request.POST['username'] # These are the html field names on the home.html file
        password = request.POST['password']

        #Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in")
            return redirect('home')
        else:
            messages.success(request, "Username is case sensitive! Please try again.")
            return redirect('login')
        
    else:
        return render(request, 'login.html', {})


# Logout user
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

# Register User
def register_user(request):
    # Check to see if it is the post metod
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate & login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered!")
            return redirect('home')
    else:
        # Not POSTing yet but load form
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


# Need to create view for the listed tags for user & then display the junk & stuff