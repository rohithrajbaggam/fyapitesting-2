from rest_framework.response import Response
from rest_framework.decorators import api_view, action, APIView, permission_classes, parser_classes
from rest_framework.mixins import  RetrieveModelMixin, UpdateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .serializers import PagePostSerializer, PageSerializer, PagePostLikeSerializer, CommentSerializer
from .models import Page, PagePost, Like, CommentPost
from .permissions import IsPageAdminOrReadOnly, IsPagePostAdminOrReadOnly
from userapp.permissions import IsUserProfileorReadOnly




# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    routes = [ 
        # url patterns to navigate user 
        # 
        'http://127.0.0.1:8000/auth/users/', # user registration 
        'http://127.0.0.1:8000/auth/jwt/create', # login a user to get access and refresh token 
        'http://127.0.0.1:8000/auth/jwt/refresh', # to get access token from refresh token
        
        'http://127.0.0.1:8000/api/userapp/userprofile/me/', # request user profile, GET,POST, PUT, request
        'http://127.0.0.1:8000/api/userapp/userprofile/', # user profile

        'http://127.0.0.1:8000/api/userapp/userprofile/<int:pk>/message/',
        'http://127.0.0.1:8000/api/userapp/userprofile/<int:pk>/message/<int:pk>',

        'http://127.0.0.1:8000/api/userapp/userprofile/5/follow/', # following a user
        'http://127.0.0.1:8000/api/userapp/userprofile/5/follow/<int:pk>/', # follow detail page to perform modification like PUT and DELETE methods

        'http://127.0.0.1:8000/api/userapp/posts/', # post create page
        'http://127.0.0.1:8000/api/userapp/posts/<int:pk>/', # post detail page put and delete options are allowed for post authors only 
        'http://127.0.0.1:8000/api/userapp/post-list/', # user post list

        'http://127.0.0.1:8000/api/userapp/posts/<int:pk>/like/', # like post page
        'http://127.0.0.1:8000/api/userapp/posts/<int:pk>/like/<int:pk>/', # like post detail page for modfication operation like PUT and DELETE

        'http://127.0.0.1:8000/api/userapp/posts/<int:pk>/comment/', # comment post page
        'http://127.0.0.1:8000/api/userapp/posts/<int:pk>/comment/<int:pk>/', # comment post detail page for modification operation like PUT and DELETE
    
        'http://127.0.0.1:8000/api/page-list/', # Page List
        'http://127.0.0.1:8000/api/pages/', # Page Create 
        'http://127.0.0.1:8000/api/pages/<int:pk>/pageposts/<int:pk>/', # Page Detail 

        'http://127.0.0.1:8000/api/pages/<int:pk>/pageposts/<int:pk>/like/',# like post page
        'http://127.0.0.1:8000/api/pages/<int:pk>/pageposts/<int:pk>/like/<int:pk>/', # like post detail page for modfication operation like PUT and DELETE
        
        'http://127.0.0.1:8000/api/pages/<int:pk>/pageposts/<int:pk>/comment/',# comment post page
        'http://127.0.0.1:8000/api/pages/<int:pk>/pageposts/<int:pk>/comment/<int:pk>/'# comment post detail page for modification operation like PUT and DELETE


    ]
    return Response(routes) 


class PageViewSet(ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [IsPageAdminOrReadOnly, IsAuthenticated]



    # def get_serializer_context(self):
    #     return {'request', self.request}
    

class PagePostViewSet(ModelViewSet):
    serializer_class = PagePostSerializer
    permission_classes = [IsAuthenticated, IsPagePostAdminOrReadOnly]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        else:
            return [IsPagePostAdminOrReadOnly()]

    def get_queryset(self):
        page = Page.objects.get(pk=self.kwargs['page_pk'] )
        return PagePost.objects.filter(admin_page=page, admin_user=page.page_admin)

    def get_serializer_context(self):
        return {'page_id': self.kwargs['page_pk'], 'user' : self.request.user}


    # def get_serializer_context(self, pk):
    #     return {pk: pk}


class PageViewList(ListModelMixin, GenericViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer 



class PagePostListView(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = PagePost.objects.all()
    serializer_class = PagePostSerializer(queryset)







class PagePostLikeViewSet(ModelViewSet):
    serializer_class = PagePostLikeSerializer
    permission_classes  = [IsUserProfileorReadOnly]

    def get_queryset(self):
        print(self.kwargs['pagepost_pk'])
        return Like.objects.filter(post=self.kwargs['pagepost_pk'])

    def get_serializer_context(self):
        # return {'post_id':self.kwargs['post_pk'], 'user':self.request.user}
        return {'pagepost_id':self.kwargs['pagepost_pk'], 'user':self.request.user}
    
    # def create(self, request, *args, **kwargs):
    #     pk = self.kwargs['pagepost_pk']
    #     post = PagePost.objects.get(pk=pk)
    #     user = self.request.user
    #     serializer = PagePostLikeSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(post=post, user=user)

    #     try:
    #         already_liked = Like.objects.get(post=post, user=user)
    #     except ObjectDoesNotExist:
    #         already_liked = None
    #     if already_liked is not None:
    #         return Response('No')
    #     else:
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)



class CommentPostViewSets(ModelViewSet):
    queryset = CommentPost.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsUserProfileorReadOnly]


    def get_queryset(self):
        return CommentPost.objects.filter(post=self.kwargs['pagepost_pk'])

    def perform_create(self, serializer):
        post = PagePost.objects.get(pk=self.kwargs['pagepost_pk'])
        serializer.save(post=post, user=self.request.user)





# @api_view(['POST'])
# @parser_classes((FileUploadParser, ))
# def page_post_create_view(request, pk):
#     page = Page.objects.get(pk=pk)
#     if request.method == 'GET':
#         queryset = PagePost.objects.filter(admin_page=page)
#         serializer = PagePostSerializer(queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         if request.user == page.page_admin:
#             # queryset = PagePost.objects.all()
#             serializer = PagePostSerializer(data=request.data, files=request.FILES)
#             serializer.is_valid(raise_exception=True)
#             serializer.save(admin_page=page, admin_user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response("Only Admins are allowed to Post", status=status.HTTP_401_UNAUTHORIZED)




#class PagePostViewSets(APIView):
#     # permission_classes = [IsPagePostAdminOrReadOnly]
#     def get(self, request, pk, format=None):
#         page = Page.objects.get(pk=pk)
#         queryset = PagePost.objects.filter(admin_page=page)
#         serializer = PagePostSerializer(queryset, many=True)
#         return Response(serializer.data)

#     # @permission_classes((IsPagePostAdminOrReadOnly, ))
#     @parser_classes([FileUploadParser])
#     def post(self, request, pk, format=None):
#         page = Page.objects.get(pk=pk)
#         serializer = PagePostSerializer(data={**request.data,**request.FILES})
#         if request.user == page.page_admin:
#             if serializer.is_valid():
#                 serializer.save(admin_page=page, admin_user=page.page_admin)
#                 # serializer.save(
#                 #     selection=Selection.objects.get(code=request.data.get('selection')),
#                 #     photo=request.data.get('photo')
#                 # )
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         return Response("Only Page Admin's are allowed to this operation", status=status.HTTP_405_METHOD_NOT_ALLOWED)



        










