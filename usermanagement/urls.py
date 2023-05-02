from django.urls import path

from . import views

app_name = 'usermanagement'
urlpatterns = [
   path('login_user', views.login_user, name="login"),
    path('logout_user', views.login_user, name="logout"),
]