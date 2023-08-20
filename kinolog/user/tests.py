from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from user.models import UserCustom
from films.models import Films


class UserAPIListTestCase(APITestCase):
    def setUp(self):
        self.usercustom = UserCustom.objects.create(first_name="John",
                                                    last_name="Doe",
                                                    phone="1234567890",
                                                    email="johndoe@example.com")
        self.user = User.objects.create_user(username='testuser',
                                             email='test@gmail.com',
                                             password='password')
        self.client.login(username='testuser', password='password')

    def test_get_user_list(self):
        url = reverse("user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_create_user(self):
    #     user_data = {
    #         "first_name": "Jane",
    #         "last_name": "Smith",
    #         "phone": "9876543210",
    #         "email": "janesmith@example.com",
    #         "favorite": []
    #     }
    #
    #     url = reverse("user-list")
    #     response = self.client.post(url, user_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(UserCustom.objects.count(), 2)
    #
    # def test_get_user_detail(self):
    #     url = reverse("user-detail", args=[str(self.usercustom.id)])
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_update_user_detail(self):
    #     url = reverse("user-detail", args=[str(self.usercustom.id)])
    #
    #     updated_data = {
    #         "first_name": "Updated First Name",
    #         "last_name": "Updated Last Name",
    #         "phone": "9876543210",
    #         "email": "updated@example.com",
    #         "favorite": []
    #     }
    #
    #     response = self.client.put(url, updated_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(UserCustom.objects.get(id=self.usercustom.id).first_name, "Updated First Name")
    #
    # def test_delete_user(self):
    #     url = reverse("user-detail", args=[str(self.usercustom.id)])
    #
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(UserCustom.objects.count(), 1)


class FavoritesFilmsAPITestCase(APITestCase):
    def setUp(self):
        self.usercustom = UserCustom.objects.create(first_name="John",
                                                    last_name="Doe",
                                                    phone="1234567890",
                                                    email="johndoe@example.com")
        self.user = User.objects.create_user(username='testuser',
                                             email='test@gmail.com',
                                             password='password')
        self.client.force_authenticate(user=self.user)

        self.film = Films.objects.create(name="Test Film",
                                         time_release='2020-01-01',
                                         description="Test description",)
        self.film_id = str(self.film.id)

    def test_get_favorite_films(self):
        url = reverse("user-favorite", args=[str(self.usercustom.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_favorite_film(self):
        url = reverse("user-favorite-film", args=[str(self.usercustom.id), self.film_id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
