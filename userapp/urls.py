from django.urls import path, include
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('userprofile', views.UserProfileViewSet)
router.register('posts', views.UserPostViewSet) # parent router
 # parent router


follow_user_router = routers.NestedDefaultRouter(router, 'userprofile', lookup='userprofile')
follow_user_router.register('follow', views.FollowViewSets, basename='follow')


message_router = routers.NestedDefaultRouter(router, 'userprofile', lookup="userprofile") 
message_router.register('message', views.MessgaeViewSet, basename='messages')


post_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
post_router.register('like', views.LikeView, basename='like-posts')
post_router.register('comment', views.CommentPostViewSets, basename='comment-posts')

 
# userposts = routers.NestedDefaultRouter(router, 'userposts', lookup='posts') likes comments all comes under child router
# userposts.register('posts', views.UserPostViewSet, basename='user-posts')

# like_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
# like_router.register('like', views.LikePostViewSet, basename='user-post-like')

 
urlpatterns = [ 
    path('post-list/', views.post_list_view),
] + router.urls + message_router.urls + post_router.urls + follow_user_router.urls


# http://127.0.0.1:8000/api/userapp/userprofile/<int:pk>/message/
# http://127.0.0.1:8000/api/userapp/userprofile/<int:pk>/message/<int:pk>
# http://127.0.0.1:8000/api/userapp/posts/<int:pk>/like/<int:pk>/
# http://127.0.0.1:8000/api/userapp/posts/<int:pk>/comment/<int:pk>/