from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
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
        return render(request, 'home.html', {'tap_tags': tap_tags, 'username': request.user.username})
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
            email = request.user.email
            print(email + "This is the users email from request")
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
        # Testing purposes
        form = SignUpForm(request.POST)
        if form.is_valid():

            # Check email for duplicates
            email_error = form.check_email()
            if email_error is None:
                form.save()
                # Authenticate & login
                # todo - check username if already selected
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, "You have successfully registered!")
                return redirect('home')
            else:
                # Inform the email taken
                form.add_error(None, "A user with that email already exists. ")

    else:
        # Not POSTing yet but load form
        form = SignUpForm()
    return render(request, 'register.html', {'form': form, 'is_register_page': True})


# Need to create view for the listed tags for user & then display the junk & stuff

def users_tags(request):
    if request.user.is_authenticated:
        user_email = request.user.email
        # filter by tags by email association.
        tap_tags = TapTag.objects.filter(email_assigned_to=user_email)
    else:
        tap_tags = None
    
    return render(request, 'taptags.html', {'tap_tags': tap_tags})


# Show individual taptag
def individual_tap_tag(request, primary_key):
    # Using the gaurdian value to show the tag
    # todo - edit a 404 page
    # tap_tag = get_object_or_404(TapTag, gaurdian = primary_key) # Catch non-existent tags
    # todo - turn off debug to see proper 404
    try:
        tap_tag = TapTag.objects.get(gaurdian = primary_key)
    except:
        messages.success(request, 'This tag does not exist!')
        return redirect('home')

    # todo - show disabled tags
    if request.user.is_authenticated:
        # Logged in
        if tap_tag.initialized == 'True':
            #Logged in - Tag initialialized
            if request.user.email == tap_tag.email_assigned_to:
                # Logged in - Tag initialized - Owner of tag (Editable)
                return render(request, 'tag.html', {'tap_tag': tap_tag, 'tagtag_initialized': True, 'owners_tag' : True})
            
            else:
                # Logged in - Tag initialized - Not Owner (View only)
                return render(request, 'tag.html', {'tap_tag': tap_tag , 'tagtag_initialized': True, 'owners_tag' : False})

        else:
            # Logged in - Tag not intialized - Claimable
            return render(request, 'tag.html', {'tap_tag': tap_tag, 'tagtag_initialized': False})

    else:
        # Not logged in
        if tap_tag.initialized == 'True':
            # Not logged in - Tag initialized (Login to claim)
            return render(request, 'tag.html', {'tap_tag': tap_tag , 'tagtag_initialized': True})
        
        else:
            # Not logged in - Tag not initialized (View only)
            return render(request, 'tag.html', {'tap_tag': tap_tag , 'tagtag_initialized': False})
    
        
def claim_tag(request, primary_key):
    tap_tag = get_object_or_404(TapTag, gaurdian = primary_key)
    # logged in?
    if request.user.is_authenticated:
        # Assign values as claiming
        tap_tag.initialized = 'True'
        tap_tag.tag_name = 'New Tag!'
        tap_tag.tag_location = '123 Bleep Bloop St'
        tap_tag.email_assigned_to = request.user.email
        user_email = request.user.email
        if not user_email:
            messages.success(request, "No email associated with this user.")
            return redirect('home')  # Redirect to an error page or handle the error appropriately
        tap_tag.save() # Save to db
        messages.success(request, "Tag Saved! Update it whenever you want!")
        return redirect('taptags')
    else:
        messages.success(request, "Must login to claim this tag!")
        return redirect('login')
    
        
        