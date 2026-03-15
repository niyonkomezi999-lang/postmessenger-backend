from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'Users', UserViewSet)
router.register(r'MessagePublies', MessagePublieViewSet)
router.register(r'Follows', FollowViewSet)
router.register(r'likes', LikeViewSet, basename='like')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', frontend),
    path('api/', include(router.urls)),
    path('api/login/', LoginView.as_view(), name= 'login'),
    path('api/feed/', FollowingMessagesView.as_view()),
    path('api/my_messages/', MyMessagesView.as_view()),
    path('auth/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),  # facultatif
]
