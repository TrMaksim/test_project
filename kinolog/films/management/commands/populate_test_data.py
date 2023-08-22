import uuid

from django.core.management.base import BaseCommand
from films.models import Category, Directors, Films


class Command(BaseCommand):
    help = "Populate test data"

    def handle(self, *args, **kwargs):
        categories = [
            {"id": uuid.uuid4(), "name": "Category 1"},
            {"id": uuid.uuid4(), "name": "Category 2"},
        ]

        directors = [
            {"name": "Director 1", "description": "Description 1"},
            {"name": "Director 2", "description": "Description 2"},
        ]

        films = [
            {
                "name": "Film 1",
                "time_release": "2022-01-01",
                "description": "Description for Film 1",
                "category": categories[0]["id"],
                "directors": [directors[0]["name"]],
            },
            {
                "name": "Film 2",
                "time_release": "2022-02-01",
                "description": "Description for Film 2",
                "category": categories[1]["id"],
                "directors": [directors[1]["name"]],
            },
        ]

        for category_data in categories:
            category = Category.objects.create(**category_data)
            self.stdout.write(self.style.SUCCESS(f"Created category: {category.name}"))

        for director_data in directors:
            director = Directors.objects.create(**director_data)
            self.stdout.write(self.style.SUCCESS(f"Created director: {director.name}"))

        for film_data in films:
            category_id = film_data.pop("category")
            directors_names = film_data.pop("directors")

            category = Category.objects.get(id=category_id)
            directors_list = Directors.objects.filter(name__in=directors_names)

            film, created = Films.objects.get_or_create(category=category, **film_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created film: {film.name}"))

            film.directors.set(directors_list)
            self.stdout.write(self.style.SUCCESS(f"Assigned directors to film: {film.name}"))
