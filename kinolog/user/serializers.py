from rest_framework import serializers
from films.models import Films
from .models import UserCustom


class FilmsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    time_release = serializers.TimeField(read_only=True)
    description = serializers.CharField()


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=25)
    last_name = serializers.CharField(max_length=125)
    phone = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    favorite = FilmsSerializer(many=True, read_only=True)

    def create(self, validated_data):
        favorites_data = validated_data.pop('favorites')
        user = UserCustom.objects.create(**validated_data)

        for favorite_data in favorites_data:
            film, _ = Films.objects.get_or_create(**favorite_data)
            user.favorite.add(film)

        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.phone = validated_data.get('phone')
        instance.email = validated_data.get('email')
        instance.save()
        return instance


class UpdateFavoritesSerializer(serializers.Serializer):
    films_id = serializers.UUIDField()

    def update(self, instance, validated_data):
        films_id = validated_data['films_id']
        try:
            film = Films.objects.get(pk=films_id)
        except Films.DoesNotExist:
            raise serializers.ValidationError("Film with the provided ID does not exist.")

        if film in instance.favorite.all():
            instance.favorite.remove(film)
        else:
            instance.favorite.add(film)

        return instance
