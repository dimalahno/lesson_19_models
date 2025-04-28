from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import RegistrationForm, LoginForm, MessageForm
from .models import CustomUser


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
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Генерация токена для подтверждения email
            # Отправка письма
            current_site = get_current_site(request)
            mail_subject = 'Активация аккаунта на нашем сайте'
            message = render_to_string('users/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return render(request, "users/registration_success.html", {"username": user.username})
    else:
        form = RegistrationForm()

    return render(request, "users/register.html", {"form": form})


def activate(request, uidb64, token):
    """
    Активация пользователя
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('users:home')
    else:
        return render(request, 'users/activation_invalid.html')



def login_view(request):
    """
    Авторизация пользователя
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f"Пользователь {user.username} успешно авторизован!")
                    return redirect('users:home')
                else:
                    messages.error(request, 'Аккаунт не активирован. Пожалуйста, подтвердите почту.')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

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