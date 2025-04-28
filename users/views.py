from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm, LoginForm, MessageForm

def home(request):
    """
    Домашняя страница
    """
    return render(request, "users/home.html")

def register(request):
    """
    Регистрация пользователя
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, "users/registration_success.html", {"username": user.username})

    else:
        form = RegistrationForm()

    return render(request, "users/register.html", {"form": form})

def login_view(request):
    """
    Авторизация пользователя
    """
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Пользователь {user.username} успешно авторизован!")
            return redirect("users:home")
        else:
            messages.error(request, "Неверный логин или пароль. Попробуйте снова.")
    else:
        form = LoginForm()

    return render(request, "users/login.html", {"form": form})

def send_message_view(request):
    """
    Отправка сообщений
    """
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваше сообщение успешно отправлено!")
            return render(request, "users/send_message.html", {"form": form})
    else:
        form = MessageForm()

    return render(request, "users/send_message.html", {"form": form})