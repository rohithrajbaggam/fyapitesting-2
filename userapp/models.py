from .choices import Hosteler_or_DayScholar_Choices, Branch_Choice, year, state_choices
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, default='user_profile_default.png')
    dob = models.DateField(blank=True, null=True)
    full_name = models.CharField(max_length=55)
    Section     = models.CharField(max_length=100, blank=True)
    Branch     = models.CharField(max_length=100, choices=Branch_Choice, default='None') 
    year_joined = models.CharField(max_length=5, choices=year )
    Hosteler_or_DayScholar  = models.CharField(max_length=100, choices=Hosteler_or_DayScholar_Choices, default='None', blank=True)
    Hostel_Room_No   = models.PositiveIntegerField(default=None,blank=True, null=True)
    bio = models.TextField(blank=True)

    Native_Language = models.CharField(max_length=10)#mandatory # add languages functionality for next update
    Languages_Known = models.CharField(max_length=100)
# add languages functionality for next update
    Address     = models.TextField(default=None, blank=True, null=True)
    State = models.CharField(choices=state_choices,max_length=255, null=True, blank=True)
    foreigners_can_enter_their_states_here = models.CharField(max_length=100, blank=True)
    Country     = models.CharField(max_length=20, default='India')

    whatsapp = models.CharField(max_length=10, blank=True) 
    instagram_username = models.CharField(max_length=50 ,blank = True)
    facebook = models.URLField(blank = True)
    linkdin_profile_link = models.URLField(blank = True)
    gmail = models.EmailField(blank=True)
    
    def __str__(self):
        return self.full_name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="user_posts", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title[:10]} by {self.author}'


class Message(models.Model):
    req_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='msg_req_user') # me or login user
    other_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='msg_other_user') # frnd
    msg = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f'{self.req_user} to {self.other_user}'


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # like = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.post} Liked by {self.user}'


class CommentPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    comment_data = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.post.title} by {self.user}'

class FollowUser(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_user') # people who follows me 
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_user') # people I follow
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.follower} follows {self.following}'

    