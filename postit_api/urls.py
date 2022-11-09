from django.urls import path, include
from .views import PostList, PostDetail, CommentList, CommentDetail
from .views import book_list

urlpatterns = [
    # path('posts', book_list), # galime naudoti ir view funkcijas # https://www.django-rest-framework.org/tutorial/1-serialization/ ir https://www.django-rest-framework.org/tutorial/2-requests-and-responses/
    path('posts', PostList.as_view()), # galime naudoti class viewsus https://www.django-rest-framework.org/tutorial/3-class-based-views/
    path('posts/<int:pk>', PostDetail.as_view()),
    path('comments', CommentList.as_view()),
    path('posts/<int:pk>/comments', CommentList.as_view()),
    path('comments/<int:pk>', CommentDetail.as_view()),
]