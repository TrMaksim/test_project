from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from films.models import Films, Category, Directors


class FilmsAPIViewTestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.director = Directors.objects.create(name='Test Director', description='Test Description')

        self.film_data = {
            "name": "Test Film",
            "time_release": "2023-01-01",
            "description": "Test description",
            "category_id": str(self.category.id),
        }

        self.user = User.objects.create_user(username='testuser@example.com',
                                             email='testuser@example.com',
                                             password='testpassword')
        self.client.login(username='testuser@example.com', password='testpassword')

        self.film = Films.objects.create(**self.film_data)
        self.film.directors.set([self.director])

    def test_get_single_film(self):
        url = reverse("films-detail", args=[str(self.film.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_film(self):
        url = reverse("films-detail", args=[str(self.film.id)])

        updated_data = {
            "name": "Updated Film Name",
            "time_release": "2023-02-01",
            "description": "Updated description",
            "category_id": str(self.category.id),
            "directors": [{"name": "Update Test Director"}]

        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Films.objects.get(id=self.film.id).name, "Updated Film Name")

    def test_delete_film(self):
        url = reverse("films-detail", args=[str(self.film.id)])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Films.objects.count(), 0)


class FilmsListViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser@example.com',
                                             email='testuser@example.com',
                                             password='testpassword')
        self.client.login(username='testuser@example.com', password='testpassword')

    def test_get_films_list(self):
        url = reverse("films-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_film(self):
        self.category = Category.objects.create(name='Test Category')
        self.director = Directors.objects.create(name='Test Director')

        film_data = {
            "name": "Test Film",
            "time_release": "2023-01-01",
            "description": "Test description",
            "category_id": str(self.category.id),
            "directors": [{"name": self.director.name}],
        }

        url = reverse("films-list")
        response = self.client.post(url, film_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Films.objects.count(), 1)

