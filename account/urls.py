from django.urls import path
from . import views

urlpatterns = [
    # URL for the sign-in page. Redirects to the signin_view function in views.py
    path('signin/', views.signin_view, name='signin_page'),

    # URL for the sign-up page. Redirects to the signup_view function in views.py
    path('signup/', views.signup_view, name='signup_page'),

    # URL for signing out the user. Redirects to the signout_view function in views.py
    path('signout/', views.signout_view, name='signout_page'),
]
