from django.urls import path
from .views import *
from matrimonial_app import views


urlpatterns=[

    path('',views.home),
    path('register/',views.register),
    path('login/',login,name='company_login'),
    path('verify/<auth_token>',views.verify),
    path('error/',views.error),
    path('tockensend/',views.tokensend),
    path('success/',views.success),
    path('company_profile/',views.user_profile),
    path('edit_profile/<str:auth_token>/<str:username>',views.profile_edit),

]