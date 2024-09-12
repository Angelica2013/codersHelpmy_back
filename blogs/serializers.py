from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth.models import User


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content', 'created_at', 'parent', 'replies']

    def get_replies(self, obj):
        if obj.parent is None:
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'comments']

    def get_comments(self, obj):
        # Solo obtiene comentarios principales (sin 'parent')
        comments = Comment.objects.filter(post=obj, parent__isnull=True)
        return CommentSerializer(comments, many=True).data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

