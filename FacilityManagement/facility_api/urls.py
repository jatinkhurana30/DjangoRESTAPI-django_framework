from django.urls import path
from .views import article_list,article_detail,article_list_class,article_detail_class,generic_article_list_class

urlpatterns = [
    path('articles' ,article_list),
    path('article',article_list_class.as_view()),
    path('articles/<int:pk>' ,article_detail),
    path('article/<str:pk>',article_detail_class.as_view()),
    path('generic/article/',generic_article_list_class.as_view())
]