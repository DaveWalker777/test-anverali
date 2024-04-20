from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login_user', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout'),
    path('register_user', views.register_user, name='register_user'),
    path('customer_profile', views.customer_profile, name='customer_profile'),
    path('contractor_profile', views.contractor_profile, name='contractor_profile'),
    path('customer_update', views.customer_profile_update, name='customer_update'),
    path('contractor_update', views.contractor_profile_update, name='contractor_update'),
    ]