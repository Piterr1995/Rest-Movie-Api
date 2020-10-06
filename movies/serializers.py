from rest_framework import serializers
from rest_framework.response import Response
from .models import Movie, Comment
from .services import fetch_movie_data


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("id", "Title")


class MovieCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"

    def validate(self, data):
        if len(data) == 1 and data["Title"]:
            title = data["Title"]
            movie_data, title_exists = fetch_movie_data(title)
            breakpoint()
            if title_exists:
                return movie_data
            else:
                raise serializers.ValidationError(
                    "Movie not found in OMDB database. Please choose another title."
                )
        raise serializers.ValidationError(
            "Please use 'Title': '<value>' as the only key in your post request"
        )


class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    movie_title = serializers.SerializerMethodField()

    def get_movie_title(self, instance):
        return instance.movie.Title

    class Meta:
        model = Comment
        fields = "__all__"