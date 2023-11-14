from django.shortcuts import render
from rest_framework.views import APIView, Response, status
#from django.middleware import cors

from .models import Movie, Category
from .serializers import (
    MovieGetResponseSerializer, 
    MovieGetRequestSerializer, 
    MoviePostRequestSerializer, 
    MoviePostResponseSerializer, 
    MoviePatchRequestSerializer, 
    MoviePatchResponseSerializer, 
    CategoryGetRequestSerializer, 
    CategoryGetResponseSerializer,
    CategoryPostRequestSerializer, 
    CategoryPostResponseSerializer,
    CategoryPatchRequestSerializer, 
    CategoryPatchResponseSerializer,
    TopMoviesGetResponseSerializer
)

class GenericCRUDAPIView(APIView):
    #@cors.middleware(enforce_resource_types=['application/json'])
    def get(self, request):
        try:
            serializer = self.request_serializer_get(data=request.query_params)
            if serializer.is_valid():
                filters = serializer.validated_data
                data = self.model.objects.filter(**filters)
                response = self.response_serializer_get(data, many=True)
                return Response(response.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
    #@cors.middleware(enforce_resource_types=['application/json'])    
    def post(self, request):
        try:
            serializer = self.request_serializer_post(data=request.data)
            if serializer.is_valid():
                serializer.save()
                movie = self.model.objects.get(pk=serializer.data['id'])
                response = self.response_serializer_post(movie)
                return Response(response.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
    #@cors.middleware(enforce_resource_types=['application/json'])    
    def patch(self, request, pk):
        try:
            movie = self.model.objects.get(pk=pk)
        except:
            return Response(f"{self.model.__class__.__name__} not found", status=status.HTTP_404_NOT_FOUND)
        
        try:
            serializer = self.request_serializer_patch(movie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                movie = self.model.objects.get(pk=pk)
                response = self.response_serializer_patch(movie)
                return Response(response.data, status=status.HTTP_202_ACCEPTED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
    #@cors.middleware(enforce_resource_types=['application/json'])    
    def delete(self, request, pk):
        try:
            movie = self.model.objects.get(pk=pk)
        except:
            return Response(f"{self.model.__class__.__name__} not found", status=status.HTTP_404_NOT_FOUND)

        try:
            movie.delete()
            return Response(f"{self.model.__class__.__name__} deleted succesfully", status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
    class Meta:
        abstract = True

class MovieAPIView(GenericCRUDAPIView):
    model = Movie
    
    request_serializer_get = MovieGetRequestSerializer
    response_serializer_get = MovieGetResponseSerializer
    
    request_serializer_post = MoviePostRequestSerializer
    response_serializer_post = MoviePostResponseSerializer
    
    request_serializer_patch = MoviePatchRequestSerializer
    response_serializer_patch = MoviePatchResponseSerializer
    
class CategoryAPIView(GenericCRUDAPIView):
    model = Category
    
    request_serializer_get = CategoryGetRequestSerializer
    response_serializer_get = CategoryGetResponseSerializer
    
    request_serializer_post = CategoryPostRequestSerializer
    response_serializer_post = CategoryPostResponseSerializer
    
    request_serializer_patch = CategoryPatchRequestSerializer
    response_serializer_patch = CategoryPatchResponseSerializer
    
    
class TopMovieAPIView(GenericCRUDAPIView):
    response_serializer_get = TopMoviesGetResponseSerializer
    
    def get(self, request):
        try:
            movies = Movie.objects.all().order_by('-rating')[:5]
            response = self.response_serializer_get(movies, many=True)
            return Response(response.data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            