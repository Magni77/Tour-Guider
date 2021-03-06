from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from apps.places.tests.factories import PlaceFactory
from apps.trips.api.serializers import TripSerializer, TripDetailSerializer
from apps.trips.models import Trip
from apps.trips.tests.factories import TripFactory


class GetAllTripsTest(APITestCase):
    def setUp(self):
        places = (PlaceFactory(name=place) for place in range(2))
        TripFactory.create(places=places, name="Wycieczka po rynku")
        TripFactory.create(places=places, name="Wycieczka po rynku")
        TripFactory.create(places=places, name="Wycieczka po rynku")

    def test_get_all_places(self):
        response = self.client.get(reverse('api-trip:list'))
        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleTripTest(APITestCase):
    def setUp(self):
        places = (PlaceFactory(name=place) for place in range(2))
        self.trip = TripFactory.create(places=places, name="Wycieczka po rynku")

    def test_get_valid_single_trip(self):
        response = self.client.get(
            reverse('api-trip:detail', kwargs={'trip_pk': self.trip.id}))
        trip = Trip.objects.first()
        serializer = TripDetailSerializer(trip)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_trip(self):
        response = self.client.get(
            reverse('api-trip:detail', kwargs={'trip_pk': 100}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewTripTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="nerd")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.valid_payload = {
            'name': 'Muffin',
            'description': 'Best trip!'
        }
        self.invalid_payload = {
            'name': '',
            'description': 'Best trip!'
        }

    def test_create_valid_trip(self):
        response = self.client.post(
            reverse('api-trip:list'),
            data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['private'], True)

    def test_create_invalid_trip(self):
        response = self.client.post(
            reverse('api-trip:list'),
            data=self.invalid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_create_public_trip(self):
        self.valid_payload['private'] = False
        response = self.client.post(
            reverse('api-trip:list'),
            data=self.valid_payload
        )
        self.assertEqual(response.data['private'], True)

    def test_superuser_create_public_trip(self):
        self.valid_payload['private'] = False
        self.user.is_superuser = True
        response = self.client.post(
            reverse('api-trip:list'),
            data=self.valid_payload
        )
        self.assertEqual(response.data['private'], False)


class UpdateSingleTripTest(APITestCase):
    def setUp(self):
        user = User.objects.create(username="nerd")
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        TripFactory.create()
        TripFactory.create()
        self.valid_payload = {
            'name': 'Trip',
            'description': 'Better then Best trip!',
        }
        self.invalid_payload = {
            'name': 'WrongName',
            'description': '',
        }

    def test_valid_update_trip(self):
        response = self.client.put(
            reverse('api-trip:detail', kwargs={'trip_pk': 1}),
            data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_trip(self):
        response = self.client.put(
            reverse('api-trip:detail', kwargs={'trip_pk': 1}),
            data=self.invalid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleTripTest(APITestCase):
    def setUp(self):
        user = User.objects.create(username="nerd")
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        TripFactory.create()

    def test_valid_delete_trip(self):
        response = self.client.delete(
            reverse('api-trip:detail', kwargs={'trip_pk': 1}),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_trip(self):
        response = self.client.delete(
            reverse('api-trip:detail', kwargs={'trip_pk': 100}),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
