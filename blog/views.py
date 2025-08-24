from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied, NotFound
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .serializers import (PostSerializer, PostCreateSerializer, 
                         CommentSerializer, CommentCreateSerializer)
from .permissions import IsOwnerOrReadOnly

class PostList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.all()
        return Post.objects.filter(is_published=True)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class CommentList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise NotFound("Post not found")
        
        if not post.is_published and not self.request.user.is_authenticated:
            raise NotFound("Post not found")
            
        return Comment.objects.filter(post_id=post_id, is_approved=True)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        
        if not post.is_published and not self.request.user.is_authenticated:
            raise PermissionDenied("Cannot comment on unpublished post")
            
        serializer.save(author=self.request.user, post=post)