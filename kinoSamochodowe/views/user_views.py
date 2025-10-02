from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from kinoSamochodowe.forms import CustomUserCreationForm, CustomUserChangeForm, PasswordChangeCustomForm


# strona główna użytkownika(Bilety, Edytuj dane)
@login_required(login_url="login")
def dashboard(request):
    return render(request, "user/dashboard.html", {"user": request.user})


#LOGOWANIE
def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Nieprawidłowy login lub hasło.")
    else:
        form = AuthenticationForm()
    return render(request, "auth/login.html", {"form": form})


def logout_user(request): # Django ma metody login,logout i register dlatego należało dodać _user do kazdej z metod
    logout(request)
    return redirect("/")


def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = CustomUserCreationForm()
    return render(request, "auth/register.html", {"form": form})


@login_required
def edit_user(request): #problem z formularzami - czyszczone są wszystkie dane oznaczone jako disabled po kliknięciiu przycisku
    user = request.user

    if request.method == "POST":
        if "update_data" in request.POST:
            form = CustomUserChangeForm(request.POST, instance=user)
            password_form = PasswordChangeCustomForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Dane użytkownika zostały zmienione.", extra_tags="user")
                return redirect("user_edit")

        elif "update_password" in request.POST:
            password_form = PasswordChangeCustomForm(user, request.POST)
            form = CustomUserChangeForm(instance=user)
            if password_form.is_valid():
                user.set_password(password_form.cleaned_data["password1"])
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Hasło zostało zmienione.", extra_tags="password")
                return redirect("user_edit")

    else:
        form = CustomUserChangeForm(instance=user)
        password_form = PasswordChangeCustomForm()

    return render(request, "user/edit.html", {"form": form, "password_form": password_form})