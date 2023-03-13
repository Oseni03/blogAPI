from django.db import models
from django.contrib.auth.models import AbstractUser
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField

# Create your models here.
class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=50, null=True)
    mobile = models.CharField(max_length=15, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    intro = models.TextField()
    profile = models.TextField()
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return str(self.username)


class Category(MPTTModel):
    title = models.CharField(max_length=20)
    meta_title = models.CharField(max_length=100)
    slug = models.SlugField(null=True)
    content = models.TextField()
    parent = TreeForeignKey("self", on_delete=models.PROTECT, related_name="children")
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return str(self.title)


class Comment(MPTTModel):
    title = models.CharField(max_length=20)
    content = models.TextField()
    parent = TreeForeignKey("self", on_delete=models.PROTECT, related_name="children")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.title)
    

class Post(MPTTModel):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="posts")
    parent = TreeForeignKey("self", on_delete=models.PROTECT, related_name="children")
    title = models.CharField(max_length=70)
    meta_title = models.CharField(max_length=100)
    tags = models.ManyToManyField(
        "Tag", related_name="posts", 
        through="PostTag")
    categories = TreeManyToManyField(
        Category, related_name="posts")
    slug = models.SlugField(null=True)
    summary = models.TextField()
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    
    def __str__(self):
        return str(self.title)


class Tag(models.Model):
    title = models.CharField(max_length=20)
    meta_title = models.CharField(max_length=100)
    slug = models.SlugField(null=True)
    content = models.TextField()
    
    def __str__(self):
        return str(self.title)


class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = (("post", "tag"),)


class PostMeta(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="meta")
    key = models.CharField(max_length=20)
    content = models.TextField()
    
    def __str__(self):
        return str(self.key)