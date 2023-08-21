from django.urls import path

from .views.favorite_view import FavoritesFilmsAPIView
from .views.user_view import UserAPIView, UserListView

urlpatterns = [
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<uuid:id>/", UserAPIView.as_view(), name="user-detail"),
    path(
        "users/<uuid:user_id>/favorite/",
        FavoritesFilmsAPIView.as_view(),
        name="user-favorite",
    ),
    path(
        "users/<uuid:user_id>/favorite/<uuid:films_id>/",
        FavoritesFilmsAPIView.as_view(),
        name="user-favorite-film",
    ),
]
