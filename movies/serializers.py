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
        try:
            if len(data) == 1 and data["Title"]:
                title = data["Title"]
                movie_data, title_exists = fetch_movie_data(
                    title
                )  # find the movie data in omdb api if it exists (check services.py)
                if title_exists:
                    return movie_data
                else:
                    raise serializers.ValidationError(
                        "Movie not found in OMDB database. Please choose another title."
                    )
            raise serializers.ValidationError(
                "Please use 'Title': '<value>' as the only key in your post request"
            )
        except KeyError:
            raise serializers.ValidationError(
                "Title not found. Make sure to use Title instead of title"
            )


class MovieDetailSerializer(serializers.ModelSerializer):
    # the most simple model serializer. Returns all the data about the movie.
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


class TopSerializer(serializers.Serializer):
    # only these params are needed to get movies from database
    year_from = serializers.CharField(max_length=20)
    year_to = serializers.CharField(max_length=20)

    def validate(self, data):
        if data["year_from"] and data["year_to"] and len(data) == 2:
            return data
        elif len(data) > 2:
            raise serializers.ValidationError(
                "Entered to many parameters! Please specify 'year_from' and 'year_to' values! only!"
            )
        else:
            raise serializers.ValidationError(
                "Please specify 'year_from' and 'year_to' values in your get request!"
            )