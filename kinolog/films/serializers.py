from rest_framework import serializers

from .models import Directors, Films


class DirectorsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)


class FilmsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    time_release = serializers.DateField()
    description = serializers.CharField()
    category_id = serializers.UUIDField()
    directors = DirectorsSerializer(many=True)

    def create(self, validated_data):
        directors_data = validated_data.pop("directors")
        film = Films.objects.create(**validated_data)

        for director_data in directors_data:
            director, _ = Directors.objects.get_or_create(name=director_data["name"])
            film.directors.add(director)

        return film

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name")
        instance.time_release = validated_data.get("time_release")
        instance.description = validated_data.get("description")
        instance.category_id = validated_data.get("category_id")

        directors_data = validated_data.get("directors")
        if directors_data is not None:
            instance.directors.clear()
            for director_data in directors_data:
                director, created = Directors.objects.get_or_create(name=director_data["name"])
                instance.directors.add(director)
            instance.save()
            return instance


# def pk(pk):
#     w1 = Films.objects.get(id=uuid.UUID(pk))
#     print(w1)
