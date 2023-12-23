from django.urls import re_path, path
from authentification import views
from django.contrib.auth import views as auth_views


app_name = 'authentification'

urlpatterns = [
   
    #url(r'^authentification', views.index, name="authentification"),

    path('resend-confirmation-email/', views.resend_confirmation, name='resend-confirmation-email'),
    path('register/', views.registerpage, name='register'),
    path('login/', views.loginpage, name='login'),
    path('activate/(?P<uidb64>[^/]+)/(?P<token>[^/]+)/', views.activate, name='activate'),
    path('logout/', views.logoutuser, name='logout'),
    path('profile/', views.profileuser, name="profile"),


    
]



