from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, MovieListView, MovieDetailView, SessionListView, SessionDetailView

router = DefaultRouter()
router.register(r'movies-admin', MovieViewSet)

urlpatterns = [
    path('', MovieListView.as_view()),
    path('<int:pk>/', MovieDetailView.as_view()),
    path('<int:movie_id>/sessions/', SessionListView.as_view()),
    path('sessions/<int:pk>/', SessionDetailView.as_view()),
    path('', include(router.urls)),
]