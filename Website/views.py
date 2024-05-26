from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import TapTag

# Create a dir named `templates` to add .html files
# Create your views here.


def home(request):
    # is user auth
    if request.user.is_authenticated:
        user_email = request.user.email
        # filter by tags by email association.
        tap_tags = TapTag.objects.filter(email_assigned_to=user_email)
    else:
        tap_tags = None
    
    return render(request, 'home.html', {'tap_tags': tap_tags})

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
            messages.success(request, "Error logging in, please try again.")
            return redirect('login')
        
    else:
        # Sending is_login_page to ensure correct navbar items appear
        return render(request, 'login.html', {'is_login_page': True})


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
        # !Update code to where register shows certain portions of code on nav bar - update colors for login & register.
        return render(request, 'register.html', {'form': form, 'is_register_page': True})
    return render(request, 'register.html', {'form': form, 'is_register_page': True})


# Need to create view for the listed tags for user & then display the junk & stuff

# Show individual taptag
def individual_tap_tag(request, primary_key):
    if request.user.is_authenticated:
        # Look up record
        tap_tag = TapTag.objects.get(id = primary_key)
        # ! UPDATE CODE HERE
        return render(request, 'record.html', {'tap_tag': tap_tag})
    else:
        messages.success(request, "Must be logged in!")
        return redirect('home')