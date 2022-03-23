from django.urls import path
from . import views
from rest_framework_nested import routers


router = routers.DefaultRouter()
# router.register('pageprofile', views.PageViewSet)
router.register('pages', views.PageViewSet)

page_posts_router = routers.NestedDefaultRouter(router, 'pages', lookup="page")
page_posts_router.register('pageposts', views.PagePostViewSet, basename='page-posts')


page_post_router = routers.NestedDefaultRouter(page_posts_router, 'pageposts', lookup='pagepost')
page_post_router.register('like', views.PagePostLikeViewSet, basename='like-posts')
page_post_router.register('comment',views.CommentPostViewSets, basename='comment-posts')


urlpatterns = [ 
    path('', views.getRoutes),
    path('page-list/', views.PageViewList.as_view({'get': 'list'}), name='page-list'),
] + router.urls + page_posts_router.urls + page_post_router.urls


