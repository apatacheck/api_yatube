from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as auth_views

from .views import PostViewSet, GroupViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment'
)

urlpatterns = [ 
    path('api-token-auth/', auth_views.obtain_auth_token), #эндпоинт для получения токена аутентификации
    path('v1/', include(router.urls)), #все API-маршруты имеют префикс v1/
]