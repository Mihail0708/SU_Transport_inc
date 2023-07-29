from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse

from SU_Transportation.freights.forms import LoadCreateForm, CompleteLoadForm
from SU_Transportation.freights.models import LoadCreateModel
from SU_Transportation.freights.validators import positive_number

UserModel = get_user_model()

class PositiveNumberValidator(TestCase):

    def test_positive_number_whenValidData(self):
        positive_number('5894240')
        self.assertTrue(True)

    def test_positive_number_whenInvalidData(self):
        with self.assertRaises(ValidationError) as context:
            positive_number('-920342')
        self.assertIsNotNone(context.exception)


class LoadFormsTests(TestCase):
    CREATE_LOAD_DATA = {
        'Load_Number': '44978',
        'Pickup': 'PickupTest',
        'Pickup_Address': '1 Test str.',
        'Delivery': 'DeliveryTest',
        'Delivery_Address': '2 Test str.',
        'Commodity': 'TestCommodity',
        'Weight': '42000',
        'Pickup_Date': '05/05/2023',
        'Pickup_Time': '08:00',
        'Delivery_Date': '05/06/2033',
        'Delivery_Time': '08:00',
    }
    COMPLETE_LOAD_DATA = {
        'Load_Number': '44978',
        'Load_POD': 'C:\\Users\\moni\\PycharmProjects\\SU_Transportation\\media\\documents\\BOL.jpg'
    }

    def test_postCreateLoadForm_whenValid(self):
        form = LoadCreateForm(LoadFormsTests.CREATE_LOAD_DATA)
        self.assertTrue(form.is_valid())

    def test_postCompleteLoadForm_whenValid(self):
        form = CompleteLoadForm(LoadFormsTests.COMPLETE_LOAD_DATA)
        self.assertTrue(form.is_valid())


class FreightViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(
            username='TestUser',
            email='test@test.com',
            password='Mpp#1983'
        )
        self.user.is_staff = True
        self.login_data = {
            'username': 'TestUser',
            'password': 'Mpp#1983',
        }

    def test_load_freights(self):
        self.client.login(**self.login_data)
        self.client.post(reverse('create load'), LoadFormsTests.CREATE_LOAD_DATA)
        freight = LoadCreateModel.objects.get()
        response = self.client.get(reverse('details load'))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, freight.Load_Number)
        self.assertContains(response, freight.Pickup)

    def test_create_freight_view(self):
        self.client.login(**self.login_data)
        response = self.client.post(reverse('create load'), LoadFormsTests.CREATE_LOAD_DATA)
        freight = LoadCreateModel.objects.get()
        self.assertEqual(302, response.status_code)
        self.assertIsNotNone(freight)

    def test_delete_freight_view(self):
        self.client.login(**self.login_data)
        self.client.post(reverse('create load'), LoadFormsTests.CREATE_LOAD_DATA)
        freight = LoadCreateModel.objects.get()
        response = self.client.post(reverse('delete load', args=[freight.pk]))
        self.assertEqual(302, response.status_code)
        self.assertFalse(LoadCreateModel.objects.filter(pk=freight.pk).exists())

