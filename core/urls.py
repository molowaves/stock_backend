from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify_reg/', views.verify_registration, name='verify_reg'),
]