from rest_framework import serializers
from posts.models import Post, Group, User


class PostSerializers(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field = 'username',
        read_only = True
    )
    group = serializers.SlugRelatedField(
        slug_field = 'title',
        read_only = True
    )

    class Meta:
        model = Post
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        fields = ("first_name", "last_name", "username",)
        model = User

class GroupSerializers(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'