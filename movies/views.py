from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from .serializers import (
    MovieDetailSerializer,
    MovieListSerializer,
    MovieCreateSerializer,
    CommentSerializer,
    TopSerializer,
)
from .models import Movie, Comment
from .services import get_movie_ranking_data


class MovieListCreateAPIView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovieCreateSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response("Movie ID does not exist in our database")

    def get(self, request, pk):
        movie = self.get_object(pk=pk)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        movie = self.get_object(pk=pk)
        serializer = MovieDetailSerializer(instance=movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = self.get_object(pk=pk)
        movie.delete()
        return Response(
            data="Movie succesfully deleted", status=status.HTTP_204_NO_CONTENT
        )


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("movie__id", "text")


class TopMoviesAPIView(APIView):
    """
    :return: a list with top movies with their ids, total comments and rank
    """

    def get(self, request):
        data = request.data
        try:
            if request.data["year_from"] and request.data["year_to"]:
                movies_rank = get_movie_ranking_data(
                    year_from=str(request.data["year_from"]),
                    year_to=str(request.data["year_to"]),
                )
                return Response(movies_rank)
        except KeyError:
            return Response(
                "Please specify 'year_from' and 'year_to' in your get request!"
            )
