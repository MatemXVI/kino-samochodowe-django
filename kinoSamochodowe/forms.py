from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
import re


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Adres e-mail", required=True,error_messages={"required": "E-mail jest wymagany!", "invalid": "E-mail jest niepoprawny!"})
    username = forms.CharField(label="Nazwa użytkownika", required=True,min_length=3,max_length=20,
                               error_messages={ "required": "Login jest wymagany!", "min_length": "Login musi mieć minimum 3 znaki!", "max_length": "Login może mieć maksymalnie 20 znaków!"})
    first_name = forms.CharField(label="Imię",required=True)
    last_name = forms.CharField(label="Nazwisko", required=True)

    age = forms.IntegerField(label="Wiek", required=True, min_value=1, max_value=150,
                             error_messages={"invalid": "Wiek jest niepoprawny!", "min_value": "Wiek nie może być mniejszy niż 1!", "max_value": "Wiek nie może być większy niż 150!"})

    phone_number = forms.CharField(label="Telefon", required=False, error_messages={"invalid": "Numer telefonu jest niepoprawny!"})

    terms = forms.BooleanField(label="Akceptuję regulamin",required=True, error_messages={"required": "Zaakceptuj regulamin!"})

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username","email","first_name","last_name","age","phone_number","terms","password1","password2")

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not re.match(r"^[\w-]+$", username):  # alpha_dash
            raise ValidationError("Login może zawierać tylko litery, cyfry, myślniki i podkreślenia!")
        return username

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if phone and not re.match(r"^(?:\d{9}|\d{3}\s\d{3}\s\d{3})$", phone):
            raise ValidationError("Numer telefonu jest niepoprawny!")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        first = cleaned_data.get("first_name")
        last = cleaned_data.get("last_name")
        if not first or not last:
            raise ValidationError("Brak imienia i nazwiska!")
        return cleaned_data


class CustomUserChangeForm(forms.ModelForm):
    email = forms.EmailField(label="Adres e-mail", required=True,error_messages={"required": "E-mail jest wymagany!", "invalid": "E-mail jest niepoprawny!"})
    username = forms.CharField(label="Nazwa użytkownika", required=True,min_length=3,max_length=20,
                               error_messages={ "required": "Login jest wymagany!", "min_length": "Login musi mieć minimum 3 znaki!", "max_length": "Login może mieć maksymalnie 20 znaków!"})
    first_name = forms.CharField(label="Imię",required=True)
    last_name = forms.CharField(label="Nazwisko", required=True)

    age = forms.IntegerField(label="Wiek", required=True, min_value=1, max_value=150,
                             error_messages={"invalid": "Wiek jest niepoprawny!", "min_value": "Wiek nie może być mniejszy niż 1!", "max_value": "Wiek nie może być większy niż 150!"})

    phone_number = forms.CharField(label="Telefon", required=False, error_messages={"invalid": "Numer telefonu jest niepoprawny!"})

    class Meta:
        model = CustomUser
        fields = ["username", "email", "first_name", "last_name", "age", "phone_number"]

    def clean(self):
        cleaned_data = super().clean()
        if self.instance and self.instance.pk:
            has_changes = False
            for field, value in cleaned_data.items():
                if value != getattr(self.instance, field):
                    has_changes = True
                    break
            if not has_changes:
                raise ValidationError("Nie wprowadzono żadnych zmian!")
        return cleaned_data

class PasswordChangeCustomForm(forms.Form):
    old_password = forms.CharField(label="Stare hasło", widget=forms.PasswordInput, required=True,
        error_messages={"required": "Musisz podać swoje obecne hasło!"},
    )

    password1 = forms.CharField(label="Nowe hasło", widget=forms.PasswordInput, required=True, min_length=5, max_length=255,
        error_messages={
            "required": "Hasło jest wymagane!",
            "min_length": "Hasło musi mieć minimum 5 znaków!",
            "max_length": "Hasło może mieć maksymalnie 255 znaków!",
        },
    )
    password2 = forms.CharField(label="Powtórz hasło", widget=forms.PasswordInput, required=True, error_messages={"required": "Potwierdzenie hasła jest wymagane!"})

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not self.user.check_password(old_password):
            raise ValidationError("Stare hasło jest nieprawidłowe!")
        return old_password


    def clean(self):
        cleaned_data = super().clean()
        old_password = self.cleaned_data.get("old_password")
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise ValidationError("Hasła się nie zgadzają!")
        if old_password and p1 and self.user.check_password(p1):
            raise ValidationError("Nowe hasło nie może być takie samo jak stare!")
        return cleaned_data



