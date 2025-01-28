from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router =  DefaultRouter()
router.register(r'stores', views.StoreViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register, name='register'),
    path('verify_reg/', views.verify_registration, name='verify_reg'),
]