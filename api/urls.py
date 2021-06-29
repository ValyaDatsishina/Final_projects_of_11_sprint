from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views
from .routers import router

# from .views import CommentList
# from .views import CommentViewSet, FollowViewSet

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/email/', views.send_code),
    path('auth/token/', views.take_token),
    path('users/me/', views.UserMeViewSet.as_view({'get': 'list',
                                                   'patch': 'update_me'})),
    path('', include(router.urls)),
]
