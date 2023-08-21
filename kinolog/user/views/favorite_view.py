from django.http import Http404
from films.models import Films
from rest_framework.response import Response
from rest_framework.views import APIView
from user.serializers import FilmsSerializer, UpdateFavoritesSerializer, UserCustom, UserSerializer


class FavoritesFilmsAPIView(APIView):
    def get_user(self, user_id):
        try:
            return UserCustom.objects.get(id=user_id)
        except UserCustom.DoesNotExist:
            raise Http404("User does not exist")

    def get(self, request, user_id, *args, **kwargs):
        user = self.get_user(user_id)
        favorite_films = user.favorite.all()
        serializer = FilmsSerializer(favorite_films, many=True)
        return Response({"favorite_films": serializer.data})

    def post(self, request, user_id, *args, **kwargs):
        serializer = UpdateFavoritesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.get_user(user_id)
        update_user = serializer.update(user, serializer.validated_data)

        return Response({"user": UserSerializer(update_user).data})

    def delete(self, request, user_id, films_id, *args, **kwargs):
        user = self.get_user(user_id)

        try:
            film = Films.objects.get()
        except Films.DoesNotExist:
            return Response({"error": f"Film with ID {films_id} does not exist."}, status=404)

        if film in user.favorite.all():
            user.favorite.remove(film)

        return Response({"message": "Film has been removed from favorites."})
