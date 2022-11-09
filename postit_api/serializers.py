from rest_framework import serializers
from .models import Post, Comment, CommentLike, PostLike


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_id', 'post', 'body', 'created']

class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    comments = serializers.StringRelatedField(many=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'user_id', 'title', 'body', 'comments', 'comments_count', 'created']

    def get_comments_count(self, obj):
        return Comment.objects.filter(post=obj).count()

    # {
    #     "id": 3,
    #     "user": "adminas",
    #     "user_id": 1,
    #     "title": "hey hey",
    #     "body": "Komentaras",
    #    "comments": []
    # }
    