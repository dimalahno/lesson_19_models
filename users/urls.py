from django.urls import path
from users.views import home, register, login_view, send_message_view, activate, profile_view, request_account_delete, \
    confirm_account_delete

app_name = 'users'

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("send-message/", send_message_view, name="send_message"),
    path("activate/<uidb64>/<token>/", activate, name='activate'),
    path('profile/', profile_view, name='profile'),
    path('delete_account/', request_account_delete, name='request_account_delete'),
    path('confirm_delete/<uidb64>/<token>/', confirm_account_delete, name='confirm_account_delete'),
]