from re import search
from api.permissions import IsOwnerOrReadOnly
from django.shortcuts import render
from posts.models import Post, Group, User
from rest_framework import viewsets
from .serializers import GroupSerializers, PostSerializers, UserSerializer
from rest_framework.permissions import AllowAny
from .permissions import IsOwnerOrReadOnly
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
# Create your views here.


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    filter_backends = [SearchFilter]
    search_fields = ['group__title',]
    permission_classes = [IsOwnerOrReadOnly, AllowAny]
    pagination_class = PageNumberPagination
    ordering_fields = ['pub_date']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['username',]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['title',]



    

    
