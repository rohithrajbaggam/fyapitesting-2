from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.contrib.auth.models import User
from .models import UserProfile, Post, Message, Like, CommentPost, FollowUser
from rest_framework import serializers



class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['user','profile_pic', 'dob', 'full_name', 
        'Section', 'Branch', 'year_joined', 
        'Hosteler_or_DayScholar', 'Hostel_Room_No', 
        'bio', 'Native_Language', 'Languages_Known', 
        'Address', 'State', 'foreigners_can_enter_their_states_here', 
        'Country', 'whatsapp', 'instagram_username',
         'facebook', 'linkdin_profile_link', 'gmail']
    def validate(self, data):
            data['user'] = self.context['request'].user
            return data



class UserPostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = ['id','author' ,'title', 'image', 'description', 'created', 'updated']
    def validate(self, data):
            data['author'] = self.context['request'].user
            return data
    


class MessageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    req_user = serializers.PrimaryKeyRelatedField(read_only=True)
    other_user = serializers.PrimaryKeyRelatedField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Message
        fields = ['id', 'req_user','other_user', 'msg', 'created' ]
    
    def create(self, validated_data):
        user = User.objects.get(pk=self.context['userprofile_id'])
        return Message.objects.create(req_user=self.context['user'], other_user=user, **validated_data)



class LikeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    like_count = serializers.SerializerMethodField(method_name='like_count_method')

    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'like_count', 'created', 'updated']
    
    def like_count_method(self, like:Like):
        print(self.context['post_id'])
        count = Like.objects.filter(post=self.context['post_id']).count()
        return count
    
    def create(self, validated_data):
        pk = self.context['post_id']  
        post = Post.objects.get(pk=pk)

        try:
            post = Like.objects.get(post=post, user=self.context['user'])
            not_liked_post = False
            print('it"s a try block')
        except MultipleObjectsReturned as e:
            post = None
            print(e)   
            print('multiple object exists')
            not_liked_post = False
        except ObjectDoesNotExist:
            print('object does not exist')
            not_liked_post = True
        if not_liked_post:
            return Like.objects.create(post=post, user=self.context['user'], **validated_data)
        else:
            return Like.objects.get(post__id=self.context['post_id'],user=self.context['user'])
        


class FollowUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    follower = serializers.PrimaryKeyRelatedField(read_only=True)
    following = serializers.PrimaryKeyRelatedField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FollowUser
        fields = ['id', 'follower', 'following', 'created', 'updated']
    
    def create(self, validated_data):
        pk = self.context['userprofile_id']
        userprofile = UserProfile.objects.get(pk=pk)
        following = self.context['user']
        follower = userprofile.user
        try:
            follow_object = FollowUser.objects.get(follower=follower, following=following)
            allow_follow = False
        except MultipleObjectsReturned:
            allow_follow = False
        except ObjectDoesNotExist:
            allow_follow = True
        if allow_follow:
            return FollowUser.objects.create(follower=follower, following=following, **validated_data)
        else:
            return FollowUser.objects.get(follower=follower, following=following)




class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = CommentPost
        fields = ['id', 'post', 'user','comment_data' ,'created', 'updated']



    # def create(self, validated_data):
    #     post = Post.objects.get(pk=self.context['post_id'])
    #     return Like.objects.create(post=post, user=self.context['user'])

# user user-profile user posts messages
# page page-posts 


# like , comment , follow, change user data 