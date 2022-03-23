from django.contrib import admin
from .models import Page, PagePost, Like, CommentPost
# Register your models here.

admin.site.register(Page)
admin.site.register(PagePost)
admin.site.register(Like)
admin.site.register(CommentPost)
