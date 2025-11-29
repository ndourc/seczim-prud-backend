from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, UserProfileViewSet, AuthViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'user-profiles', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', AuthViewSet.as_view({'post': 'login'}), name='login'),
    path('logout/', AuthViewSet.as_view({'post': 'logout'}), name='logout'),
    path('register/', AuthViewSet.as_view({'post': 'register'}), name='register'),
    path('change-password/', AuthViewSet.as_view({'post': 'change_password'}), name='change_password'),
    path('reset-password/', AuthViewSet.as_view({'post': 'reset_password'}), name='reset_password'),
    path('me/', AuthViewSet.as_view({'get': 'me'}), name='me'),
    path('dashboard/', AuthViewSet.as_view({'get': 'dashboard'}), name='dashboard'),
]
