from django.urls import path, include
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .apps import UsersConfig
from .views import PaymentViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)
from users.views import UserCreateAPIView

urlpatterns = [
    path('', include(router.urls)),
    path('register/',UserCreateAPIView.as_view(), name= 'register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
]
urlpatterns += router.urls