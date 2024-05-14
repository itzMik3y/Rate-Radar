from django.urls import path
# from .views import *
from . import views
from .views import MyTokenObtainPairView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenRefreshView
)
from django.conf import settings
# from .views import UserAPICallCountView



urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('pulse/', views.pulse, name='pulse'),
]