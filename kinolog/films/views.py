from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Films
from .serializers import FilmsSerializer
from .service import FilmsFilter, FilmsPagination


class FilmsListView(generics.ListCreateAPIView):
    queryset = Films.objects.all()
    serializer_class = FilmsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FilmsFilter
    ordering_fields = ["category_id", "time_release"]
    pagination_class = FilmsPagination
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = FilmsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        film = serializer.save()

        return Response({"film": FilmsSerializer(film).data}, status=status.HTTP_201_CREATED)


class FilmsAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,) Для демонстрации, доступ по Session будет закрыт
    # Доступ только по токену

    def get(self, request, id=None, *args, **kwargs):
        if id is not None:
            film = get_object_or_404(Films, id=id)
            serializer = FilmsSerializer(film)
            return Response(serializer.data)

        queryset = Films.objects.all()
        serializer = FilmsSerializer(queryset, many=True)
        return Response({"films": serializer.data})

    def put(self, request, id=None, *args, **kwargs):
        film = get_object_or_404(Films, id=id)
        serializer = FilmsSerializer(data=request.data, instance=film)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"film": FilmsSerializer(film).data})

    def delete(self, request, id=None, *args, **kwargs):
        film = get_object_or_404(Films, id=id)
        film.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


# class FilmsAPIView(generics.ListAPIView):
#     queryset = Films.objects.all()
#     serializer_class = FilmsSerializer
