from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly,IsAdminUser
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

class MessagePublieViewSet(viewsets.ModelViewSet):
    queryset = MessagePublie.objects.all()
    serializer_class = MessagePublieSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['poster', 'date_creation']
    permission_classes = [IsAuthenticatedOrReadOnly]

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['gagnant', 'abonne']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # On retourne uniquement les abonnements de l'utilisateur connecté
        return Follow.objects.filter(follower=self.request.user)
    

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer