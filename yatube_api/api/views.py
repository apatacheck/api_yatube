from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from posts.models import Post, Group
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet): #управление постами
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user) 

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user: #проверка авторства
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super().perform_update(serializer) 

    def perform_destroy(self, instance):
        if instance.author != self.request.user: #проверка авторства
            raise PermissionDenied('Удаление чужого контента запрещено!')
        instance.delete() 


class GroupViewSet(viewsets.ReadOnlyModelViewSet): #Только GET-запросы
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_post(self):
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, id=post_id) #возвращает пост

    def get_queryset(self):
        post = self.get_post()
        return post.comments.all() #вовзращает все комментарии к посту

    def perform_create(self, serializer):
        post = self.get_post() #получает пост
        serializer.save(author=self.request.user, post=post) #автор определяется автоматически

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user: #проверка авторства
            raise PermissionDenied('Изменение чужого комментария запрещено!') 
        super().perform_update(serializer) #сохранение 

    def perform_destroy(self, instance):
        if instance.author != self.request.user: #проверка авторства
            raise PermissionDenied('Удаление чужого комментария запрещено!')
        instance.delete()
        