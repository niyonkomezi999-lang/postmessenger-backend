from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly,AllowAny
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

def frontend(request):
    return render(request, "index.html")
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes =[IsAuthenticatedOrReadOnly] #[IsAdminUser]
#pour les users que je suis    
class FollowingMessagesView(ListAPIView):
    serializer_class = MessagePublieSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        following_users = Follow.objects.filter(abonne=user).values_list("gagnant", flat=True)
        return MessagePublie.objects.filter(poster__in=following_users).order_by("-date_creation")

class MyMessagesView(ListAPIView):
    serializer_class = MessagePublieSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return MessagePublie.objects.filter(poster=user).order_by("-date_creation")

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
    permission_classes =[IsAuthenticated]

    #def get_queryset(self):
        # On retourne uniquement les abonnements de l'utilisateur connecté
    #     return Follow.objects.filter(abonne=self.request.user)
    

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

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer