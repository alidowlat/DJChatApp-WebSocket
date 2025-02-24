from django import forms
from django.contrib.auth import get_user_model

user = get_user_model()


class SignUpForm(forms.ModelForm):
    """
    A form for creating a new user account.
    It includes fields for username, email, and password.

    Fields:
        - username: The unique username for the user.
        - email: The email address of the user.
        - password: The password for the user, rendered as a password input.

    Methods:
        save(commit=True):
            - Hashes the password before saving the user to the database.
            - If commit=True, saves the user instance to the database.
    """
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = user
        fields = ["username", "email", "password"]

    def save(self, commit=True):
        """
        Save the user instance, with the password being hashed.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
