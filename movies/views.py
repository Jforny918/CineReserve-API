from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Movie, Session
from .serializers import MovieSerializer, SessionSerializer


class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all().order_by('id')
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'genre']
    ordering_fields = ['title', 'created_at']


class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]


class SessionListView(generics.ListAPIView):
    serializer_class = SessionSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['language', 'format']
    ordering_fields = ['datetime']

    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        return Session.objects.filter(movie_id=movie_id).select_related('movie', 'room')


class SessionDetailView(generics.RetrieveAPIView):
    queryset = Session.objects.all().select_related('movie', 'room')
    serializer_class = SessionSerializer
    permission_classes = [permissions.AllowAny]