from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile, Post, Message, Like, CommentPost, FollowUser
from .serializers import UserProfileSerializer, UserPostSerializer, MessageSerializer, LikeSerializer, CommentSerializer, FollowUserSerializer
from .permissions import IsAuthorOrReadOnly, IsUserProfileorReadOnly, IsFollowingUserOrReadOnly, IsMessageAuthorOrReadOnly
from itertools import chain

# Create your views here.
class UserProfileViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsUserProfileorReadOnly, IsAuthenticated]


    @action(detail=False, methods=['GET','POST', 'PUT'])
    def me(self, request):
        if request.method == 'GET':
            queryset = get_object_or_404(UserProfile, user=request.user)
            serializer = UserProfileSerializer(queryset)
            return Response(serializer.data)
        if request.method == 'POST':
            queryset = UserProfile.objects.create(user=request.user)
            serializer = UserProfileSerializer(queryset)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = UserProfileSerializer(UserProfile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)



class MessgaeViewSet(ModelViewSet):
    serializer_class = MessageSerializer 
    permission_classsees = [IsMessageAuthorOrReadOnly]

    def get_queryset(self):
        user = User.objects.get(pk=self.kwargs['userprofile_pk'])
        queryset1 = Message.objects.filter(req_user=self.request.user, other_user=user)
        queryset2 = Message.objects.filter(req_user=user, other_user=self.request.user)
        # message_order = sorted(chain(msgs, my_msgs), key=lambda msg : msg.sent, reverse=False)
        # queryset = sorted(chain(queryset1, queryset2), key=)
        queryset = sorted(chain(queryset1, queryset2), key=lambda msg:msg.created, reverse=False)
        # message_order = sorted(chain(msgs, my_msgs), key=lambda msg : msg.sent, reverse=False)
        return queryset
    
    

    # def list(self, request, *args, **kwargs):
    #     user = User.objects.get(pk=self.kwargs['userprofile_pk'])
    #     queryset = UserProfile.objects.get(user=user)
    #     serializer = UserProfileSerializer(queryset, many=False)
    #     return Response(serializer.data)
    
    def get_serializer_context(self):
        return {'userprofile_id': self.kwargs['userprofile_pk'], 'user' : self.request.user}


class MessageList(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class CommentPostViewSets(ModelViewSet):
    queryset = CommentPost.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsUserProfileorReadOnly]

    def get_queryset(self):
        return CommentPost.objects.filter(post=self.kwargs['post_pk'])

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['post_pk'])
        serializer.save(post=post, user=self.request.user)



#  serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LikeView(ModelViewSet):
    serializer_class = LikeSerializer
    permission_classes  = [IsUserProfileorReadOnly]

    def get_queryset(self):
        print(self.kwargs['post_pk'])
        return Like.objects.filter(post=self.kwargs['post_pk'])

    def get_serializer_context(self):
        return {'post_id':self.kwargs['post_pk'], 'user':self.request.user}


class FollowViewSets(ModelViewSet):
    serializer_class = FollowUserSerializer
    permission_classes  = [IsFollowingUserOrReadOnly]

    def get_queryset(self):
        userprofile = UserProfile.objects.get(pk=self.kwargs['userprofile_pk'])
        return FollowUser.objects.filter(follower=userprofile.user)

    def get_serializer_context(self):
        return {'userprofile_id':self.kwargs['userprofile_pk'], 'user':self.request.user}
    
    


    
    # def create(self, request, *args, **kwargs):
    #     try:
    #         already_liked = Like.objects.get(post=self.kwargs['post_pk'], user=self.request.user)
    #     except ObjectDoesNotExist:
    #         already_liked = None

    #     return super().create(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #     post = Post.objects.get(pk=self.kwargs['post_pk'])
    #     user = self.request.user
    #     serializer = LikeSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(post=post, user=user)

    #     try:
    #         already_liked = Like.objects.get(post=post, user=user)
    #         already_liked_user = True
    #     except MultipleObjectsReturned:
    #         already_liked_user = False 
    #     if already_liked_user:
    #         return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)
    #     else:
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            



    

@api_view(['GET'])
def post_list_view(request):
    queryset = Post.objects.all()
    serializers = UserPostSerializer(queryset, many=True)
    return Response(serializers.data)




# class UserPostViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
#     queryset = Post.objects.all()
#     serializer_class = UserPostSerializer

class UserPostViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = UserPostSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]

    
    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        queryset = Post.objects.all()
        if request.method == 'GET':
            serializer = UserPostSerializer(queryset)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = UserPostSerializer(Post, data=request.sata)
            return Response(serializer.data)
        elif request.user == queryset.author :
            if request.method == 'PUT':
                serializer = UserPostSerializer(Post, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data) 










# class LikeViewSets(ModelViewSet):
#     queryset = Like.objects.all()
#     serializer_class = LikeSerializer



# class LikePostViewSet(ModelViewSet):
#     queryset = Like.objects.all()
#     serializer_class = LikeSerializer

#     def get_serializer_context(self):
#         return {'post_id': self.kwargs['post_pk'], 'user' : self.request.user}

# /api/userapp/posts/<int:pk>/like
# @api_view(['GET'])
# def like_post(request, pk):



#  def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def perform_create(self, serializer):
#         serializer.save()

#     def get_success_headers(self, data):
#         try:
#             return {'Location': str(data[api_settings.URL_FIELD_NAME])}
#         except (TypeError, KeyError):
#             return {}

# def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     def perform_destroy(self, instance):
#         instance.delete()








