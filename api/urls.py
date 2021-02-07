from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import views
from .views import GroupViewSet, PostViewSet, UserViewSet

router = DefaultRouter()
router.register(r'v1/posts', PostViewSet, basename='posts')
router.register(r'v1/users', UserViewSet, basename='users')
router.register(r'v1/groups', GroupViewSet, basename='groups')



urlpatterns = [
    path('', include(router.urls)),
]
