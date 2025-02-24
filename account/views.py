from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.urls import reverse
from .forms import SignUpForm
from django.shortcuts import redirect


def signup_view(request):
    # Handle POST request for user registration
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user and hash the password
            login(request, user)  # Log the user in
            return redirect(reverse('index_page'))  # Redirect to homepage
    else:
        form = SignUpForm()  # Create an empty form for GET request

    context = {'form': form}
    return render(request, "account/signup.html", context)


def signin_view(request):
    # Handle POST request for user login
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Get the user object
            login(request, user)  # Log the user in
            return redirect(reverse('index_page'))  # Redirect to homepage
    else:
        form = AuthenticationForm()  # Create an empty form for GET request

    context = {'form': form}
    return render(request, "account/signin.html", context)


def signout_view(request):
    # Handle user logout
    logout(request)
    return redirect(reverse('signin_page'))  # Redirect to sign-in page after logout
