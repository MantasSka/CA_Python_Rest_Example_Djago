from django.shortcuts import render
from rest_framework import generics, permissions, status
from sqlalchemy import null 
from .models import Post, PostLike, Comment, CommentLike
from .serializers import PostSerializer, CommentSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse

# a very simple example of how serialization works

def book_list(request):
    posts = Post.objects.all()
    posts_list = list(posts.values())
    return JsonResponse(
        {
            'posts': posts_list
        }
    )


# a very simple view function for get and post functions, no user added here for simplicity
@api_view(['GET', 'POST'])
def book_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer_class = PostSerializer(posts, many=True)
        return Response(serializer_class.data)

    if request.method == 'POST':
        serializer_class = PostSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save(user=request.user)
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

# this is GET/POST implemeted using class view, notice how much less code here we have
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('Negalima trinti svetimų pranešimų!')

    def put(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if post.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError('Negalima koreguoti svetimų pranešimų!')

class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if 'pk' in self.kwargs:
            print('hey')
            post = Post.objects.get(pk=self.kwargs['pk'])
            return Comment.objects.filter(post=post)
        else:
            return Comment.objects.all()

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, post=post)

    # def get_queryset(self):
    #     post = Post.objects.get(pk=self.kwargs['pk'])
    #     return Comment.objects.filter(post=post)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        comment = Comment.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if comment.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('Negalima trinti svetimų komentarų!')

    def put(self, request, *args, **kwargs):
        comment = Comment.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if comment.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError('Negalima koreguoti svetimų komentarų!')