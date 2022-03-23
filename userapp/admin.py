from django.contrib import admin
from .models import UserProfile, Post, Message, Like, CommentPost, FollowUser

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Message)
admin.site.register(Like)
admin.site.register(CommentPost)
admin.site.register(FollowUser)