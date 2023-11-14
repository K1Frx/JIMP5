from django.urls import path
from .apiviews import MovieAPIView, CategoryAPIView, TopMovieAPIView

urlpatterns = [
    path("api/movies/", MovieAPIView.as_view(), name="movie_list"),
    path("api/movies/<int:pk>/", MovieAPIView.as_view(), name="movie_list"),
    path("api/top-movies/", TopMovieAPIView.as_view(), name="top_movies_list"),
    path("api/categories/", CategoryAPIView.as_view(), name="category_list"),
    path("api/categories/<int:pk>/", CategoryAPIView.as_view(), name="category_list"),
]