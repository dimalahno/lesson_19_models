from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Message


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Введите действующий email")

    class Meta:
        model = CustomUser
        fields = ["username", "phone_number", "address", "email", "password1", "password2"]
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Этот адрес электронной почты уже зарегистрирован.")
        return email
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"}))

"""
Отправка сообщений
"""
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["name", "email", "text"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ваше имя"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Ваша почта"}),
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Введите сообщение"}),
        }

    def clean_text(self):
        text = self.cleaned_data.get("text")

        # Проверяем, что текст не пустой
        if not text.strip():
            raise forms.ValidationError("Сообщение не может быть пустым.")

        # Проверяем, что текст не превышает 500 символов
        if len(text) > 500:
            raise forms.ValidationError("Сообщение не должно превышать 500 символов.")

        return text
            