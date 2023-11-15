from django.shortcuts import render
from rest_framework.views import APIView, Response, status

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

class PaginatorAPIView(APIView):
    def paginate(self, queryset, page=None, per_page=None):
        if page is None:
            page = 1
        if per_page is None:
            per_page=100
            
        if per_page < 1:
            per_page = 1
        elif per_page > 500:
            per_page = 500

        total = len(queryset)
        num_pages = int(total / per_page)
        if total % per_page != 0:
            num_pages += 1

        if page < 1:
            page = 1
        elif page > num_pages:
            page = num_pages
            if page == 0:
                page = 1

        index_start = (page - 1) * per_page
        index_finish = index_start + per_page
        if index_finish > total:
            index_finish = total

        return {
            "page": page,
            "total": total,
            "per_page": per_page,
            "num_pages": num_pages,
            "offset": index_start,
            "items": queryset[index_start:index_finish]
        }

class GenericCRUDAPIView(PaginatorAPIView):
    def get(self, request):
        try:
            serializer = self.request_serializer_get(data=request.query_params)
            if serializer.is_valid():
                filters = serializer.validated_data
                
                page = filters.pop('page', None)
                per_page = filters.pop('per_page', None)
                
                data = self.model.objects.filter(**filters)
                paginated_data = self.paginate(data, page, per_page)
                response = self.response_serializer_get(paginated_data)
                return Response(response.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
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
    
    
class TopMovieAPIView(PaginatorAPIView):
    response_serializer_get = TopMoviesGetResponseSerializer
    
    def get(self, request):
        try:
            movies = Movie.objects.all().order_by('-rating')[:5]
            movies = self.paginate(movies)
            response = self.response_serializer_get(movies)
            return Response(response.data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            