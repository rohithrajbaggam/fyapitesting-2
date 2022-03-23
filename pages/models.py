from hashlib import blake2b
import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Page(models.Model):
    page_admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pages')
    page_profile = models.ImageField(upload_to='page_profile', default='page_profile_default.jpeg')
    page_title = models.CharField(max_length=100, unique=True)
    about = models.TextField()
    field = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    your_role = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    # social media 
    whatsapp = models.CharField(max_length=10, blank=True)
    linkdin_profile_link = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.page_title} by {self.page_admin}' 


class PagePost(models.Model):
    admin_page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='page_post')
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='page_user')
    title = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='page_posts', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title[0:20]} by {self.admin_page}'


class Like(models.Model):
    post = models.ForeignKey(PagePost,on_delete= models.CASCADE, related_name='page_post_like')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='page_post_user_like')

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.post.title} liked by {self.user}'

class CommentPost(models.Model):
    post = models.ForeignKey(PagePost, on_delete=models.CASCADE, related_name='comment_page_post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_page_post_user')
    comment_data = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.post.title} by {self.user}'