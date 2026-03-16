from rest_framework import serializers
from .models import Seat, Ticket


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'row', 'col', 'status']


class ReserveSeatSerializer(serializers.Serializer):
    seat_id = serializers.IntegerField()


class TicketSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='seat.session.movie.title', read_only=True)
    session_datetime = serializers.DateTimeField(source='seat.session.datetime', read_only=True)
    room_name = serializers.CharField(source='seat.session.room.name', read_only=True)
    seat_row = serializers.CharField(source='seat.row', read_only=True)
    seat_col = serializers.IntegerField(source='seat.col', read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'ticket_code', 'purchased_at', 'movie_title', 'session_datetime', 'room_name', 'seat_row', 'seat_col']