from rest_framework import serializers 

from .models import Category, Post, Comment, PostMeta, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = "__all__"
        depth = 2


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post 
        fields = [
            "id", "author", "title", 
            "meta_title", "tags", 
            "categories", "slug", 
            "summary","content", "meta",
            "published", "created_at", 
            "updated_at", "published_at"]