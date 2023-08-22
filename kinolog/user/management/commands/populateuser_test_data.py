import uuid
from django.core.management.base import BaseCommand
from films.models import Films
from user.models import UserCustom


class Command(BaseCommand):
    help = "Populate test data for UserCustom model"

    def handle(self, *args, **kwargs):
        films = Films.objects.all()

        users = [
            {
                "first_name": "User 1",
                "last_name": "Last Name 1",
                "phone": "1234567890",
                "email": "user1@example.com",
                "favorite": films[:2],
            },
            {
                "first_name": "User 2",
                "last_name": "Last Name 2",
                "phone": "9876543210",
                "email": "user2@example.com",
                "favorite": films[2:],
            },
        ]

        for user_data in users:
            favorite_films = user_data.pop("favorite")
            user = UserCustom.objects.create(**user_data)
            user.favorite.set(favorite_films)

        self.stdout.write(self.style.SUCCESS("Test data for UserCustom model populated successfully"))
