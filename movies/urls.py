from django.urls import path
from . import views

urlpatterns = [
    path("movies/", views.MovieListCreateAPIView.as_view(), name="movies"),
    path(
        "movies/<int:pk>/",
        views.MovieDetailAPIView.as_view(),
        name="movie_details",
    ),
    path("comments/", views.CommentListCreateAPIView.as_view(), name="comments"),
]
