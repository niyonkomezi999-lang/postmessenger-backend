from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password =serializers.CharField(write_only=True) 
    
    def validate(self, data):
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        
        try:
            user = User.objects.get(username=username, email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Utilisateur incorrect")
        if not user.check_password(password):
            raise serializers.ValidationError("Mot de passe incorrect")
        if not user.is_active:
            raise serializers.ValidationError("utilisateur inactif")
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "username": user.username,
            "email": user.email
        }
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']
class MessagePublieSerializer(serializers.ModelSerializer):
    poster_username = serializers.CharField(source='poster.username', read_only=True)
    class Meta:
        model = MessagePublie
        fields = ['id', 'contenu', 'date_creation', 'poster', 'poster_username']

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'date_created']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'contenu', 'date_created']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        data['is_staff'] = self.user.is_staff
        return data