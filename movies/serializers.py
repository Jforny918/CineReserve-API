from rest_framework import serializers
from .models import Movie, Room, Session


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'duration_minutes', 'genre', 'rating', 'poster_url', 'created_at']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'rows', 'cols']


class SessionSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    room_name = serializers.CharField(source='room.name', read_only=True)
    available_seats = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = ['id', 'movie', 'movie_title', 'room', 'room_name', 'datetime', 'language', 'format', 'available_seats']

    def get_available_seats(self, obj):
        return obj.seats.filter(status='available').count()