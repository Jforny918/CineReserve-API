from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from drf_spectacular.utils import extend_schema
import uuid

from movies.models import Session
from .models import Seat, Ticket
from .serializers import SeatSerializer, ReserveSeatSerializer, TicketSerializer


def generate_seats_for_session(session):
    if session.seats.exists():
        return
    room = session.room
    rows = [chr(65 + i) for i in range(room.rows)]
    seats = [
        Seat(session=session, row=row, col=col, status=Seat.Status.AVAILABLE)
        for row in rows
        for col in range(1, room.cols + 1)
    ]
    Seat.objects.bulk_create(seats)


class SeatMapView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, session_id):
        session = get_object_or_404(Session, id=session_id)
        generate_seats_for_session(session)
        seats = session.seats.all().order_by('row', 'col')
        serializer = SeatSerializer(seats, many=True)
        return Response({
            'session_id': session.id,
            'movie': session.movie.title,
            'datetime': session.datetime,
            'room': session.room.name,
            'seats': serializer.data
        })


@extend_schema(request=ReserveSeatSerializer)
class ReserveSeatView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, session_id):
        serializer = ReserveSeatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        seat_id = serializer.validated_data['seat_id']
        seat = get_object_or_404(Seat, id=seat_id, session_id=session_id)

        expiry = timezone.now() - timedelta(minutes=10)
        if seat.status == Seat.Status.RESERVED:
            if seat.reserved_at and seat.reserved_at < expiry:
                seat.status = Seat.Status.AVAILABLE
                seat.reserved_by = None
                seat.reserved_at = None
                seat.save()

        if seat.status != Seat.Status.AVAILABLE:
            return Response(
                {'error': 'Assento não disponível.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        seat.status = Seat.Status.RESERVED
        seat.reserved_by = request.user
        seat.reserved_at = timezone.now()
        seat.save()

        return Response({
            'message': 'Assento reservado por 10 minutos.',
            'seat': SeatSerializer(seat).data,
            'expires_at': seat.reserved_at + timedelta(minutes=10)
        })


@extend_schema(request=ReserveSeatSerializer)
class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, session_id):
        serializer = ReserveSeatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        seat_id = serializer.validated_data['seat_id']
        seat = get_object_or_404(Seat, id=seat_id, session_id=session_id)

        if seat.status != Seat.Status.RESERVED or seat.reserved_by != request.user:
            return Response(
                {'error': 'Assento não está reservado para você.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        expiry = timezone.now() - timedelta(minutes=10)
        if seat.reserved_at < expiry:
            seat.status = Seat.Status.AVAILABLE
            seat.reserved_by = None
            seat.reserved_at = None
            seat.save()
            return Response(
                {'error': 'Reserva expirada. Selecione o assento novamente.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        seat.status = Seat.Status.PURCHASED
        seat.save()

        ticket = Ticket.objects.create(
            user=request.user,
            seat=seat,
            ticket_code=f'CNP-{uuid.uuid4().hex[:8].upper()}'
        )

        return Response({
            'message': 'Ticket gerado com sucesso!',
            'ticket': TicketSerializer(ticket).data
        }, status=status.HTTP_201_CREATED)


class MyTicketsView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(
            user=self.request.user
        ).select_related(
            'seat__session__movie',
            'seat__session__room'
        ).order_by('-purchased_at')