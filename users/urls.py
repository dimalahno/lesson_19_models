from django.urls import path
from users.views import home, register, login_view, send_message_view, activate

app_name = 'users'

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("send-message/", send_message_view, name="send_message"),
    path("activate/<uidb64>/<token>/", activate, name='activate'),
]