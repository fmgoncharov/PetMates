from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from petmates import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', auth_views.LoginView.as_view(), name="login"),
    path('logout', auth_views.LogoutView.as_view(), name="logout"),
    path('registration/', views.registration, name="registration"),
    path('accounts/profile/', views.ban, name="accounts/profile"),
    path('admin/', admin.site.urls),
    path('preferences', views.preferences, name="preferences"),
    path('adverts/<str:breed>', views.adverts, name="adverts"),
]
