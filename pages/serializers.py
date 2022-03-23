from .models import Like, Page, PagePost, CommentPost
from rest_framework import serializers
from rest_framework.response import Response
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

class PageSerializer(serializers.ModelSerializer):
    # page_post = 'PagePostSerializer(many=True, read_only=True)'
    page_admin = serializers.PrimaryKeyRelatedField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Page
        fields = ['id','page_admin', 'page_profile', 'page_title', 'about', 
        'field', 'description', 'your_role', 'website', 'whatsapp', 
        'linkdin_profile_link', 'facebook', 'instagram', 'email', 'updated', 'created']

    def validate(self, data):
            data['page_admin'] = self.context['request'].user
            return data 


class PagePostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    admin_page = serializers.PrimaryKeyRelatedField(read_only=True)
    admin_user = serializers.PrimaryKeyRelatedField(read_only=True) 
    class Meta:
        model = PagePost
        fields = ['id', 'admin_page', 'admin_user', 'title', 'image', 'description']

    def create(self, validated_data):
        pk = self.context['page_id']
        page = Page.objects.get(pk=pk)
        req_user = self.context['user']
        if req_user == page.page_admin:
            return PagePost.objects.create(admin_page=page, admin_user=req_user, **validated_data)




class PagePostLikeSerializer(serializers.ModelSerializer):
    
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
        count = Like.objects.filter(post=self.context['pagepost_id']).count()
        return count
    
    def create(self, validated_data):
        pk = self.context['pagepost_id']
        post = PagePost.objects.get(pk=pk)

        try:
            post = Like.objects.get(post=post, user=self.context['user'])
            not_liked_post = False
        except MultipleObjectsReturned as e:
            not_liked_post = False
        except ObjectDoesNotExist:
            not_liked_post = True
        if not_liked_post:
            return Like.objects.create(post=post, user=self.context['user'], **validated_data)
        else:
            return [{'Error', 'Already Liked the Post'}]
            # return Like.objects.get(post__id=self.context['pagepost_id'], user=self.context['user'])







class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = CommentPost
        fields = ['id', 'post', 'user','comment_data' ,'created', 'updated']