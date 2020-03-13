from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from .models import Article
from .serializer import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins


# Create your views here.
class generic_article_list_class(generics.GenericAPIView,mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def get(self,request):
        return self.list(request)

    def post(self,request):
        return self.create(request)


class article_list_class(APIView):

    def get(self,request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data,status = 201)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class article_detail_class(APIView):

    def get_object(self,id):
        try:
            return Article.objects.get(title=id)
        except Article.DoesNotExist:
            return None

    def get(self,request,pk):
        article = self.get_object(pk)
        if article == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def put(self,request,pk):
        article = self.get_object(pk)
        if article == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        article = self.get_object(pk)
        if article == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        #Not required as now we are using api_view decorator and directly use request.data
        #data = JSONParser().parse(request)
        serializer = ArticleSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            #return JsonResponse(serializer.data,status = 201)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

#@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def article_detail(request,pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response(status = status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data,status=status.HTTP_200_OK)

    elif request.method == 'PUT':
       #data = JSONParser().parse(request)
        serializer = ArticleSerializer(article, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)