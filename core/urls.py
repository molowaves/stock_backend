from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router =  DefaultRouter()
router.register(r'stores', views.StoreViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register, name='register'),
    path('verify_reg/', views.verify_registration, name='verify_reg'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]