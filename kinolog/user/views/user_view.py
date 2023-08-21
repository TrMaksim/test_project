from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import UserCustom
from user.serializers import UserSerializer
from user.service import UserFilter, UserPagination


class UserListView(generics.ListCreateAPIView):
    queryset = UserCustom.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = UserFilter
    ordering_fields = ["first_name", "phone"]
    pagination_class = UserPagination
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        film = serializer.save()

        return Response({"film": UserSerializer(film).data}, status=status.HTTP_201_CREATED)


class UserAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,) Для демонстрации можно использовать, но доступ по Session
    # будет только по токену

    def get(self, request, id=None, *args, **kwargs):
        if id is not None:
            user = get_object_or_404(UserCustom, id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data)

        queryset = UserCustom.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response({"users": serializer.data})

    def put(self, request, id=None, *args, **kwargs):
        user = get_object_or_404(UserCustom, id=id)
        serializer = UserSerializer(data=request.data, instance=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"user": UserSerializer(user).data})

    def delete(self, request, id=None, *args, **kwargs):
        user = get_object_or_404(UserCustom, id=id)
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
