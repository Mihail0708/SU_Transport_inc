from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse

from SU_Transportation.accounts.validators import only_integers
from SU_Transportation.common.forms import DriverApplicationForm, ApplicationAddressForm
from SU_Transportation.common.models import DriverApplication, ContactUsModel

UserModel = get_user_model()


class IntegerValidator(TestCase):

    def test_validator_integer_whenValidData(self):
        only_integers('5894240')
        self.assertTrue(True)

    def test_validator_integer_whenInvalidData(self):
        with self.assertRaises(ValidationError) as context:
            only_integers('9203tjt42')
        self.assertIsNotNone(context.exception)


class FormTests(TestCase):
    VALID_APPLICATION_DATA = {
        'First_Name': 'TestFName',
        'Last_Name': 'TestLName',
        'Date_of_Birth': '05/05/1989',
        'Cell_Phone': '2242245656',
        'email': 'test@test.com',
        'SSL_Number': '005050505',
        'CDL_NUmber': 'P-7489984',
    }
    VALID_ADDRESS_DATA = {
        'Street' : '15 E. Test str.',
        'City' : 'Chicago',
        'State' : 'IL',
        'Zipcode' : '60077',
    }

    def test_postCreateApplicationForm_whenValid(self):
        form = DriverApplicationForm(FormTests.VALID_APPLICATION_DATA)

        self.assertTrue(form.is_valid())

    def test_postCreateAddressForm_whenValid(self):
        form = ApplicationAddressForm(FormTests.VALID_ADDRESS_DATA)

        self.assertTrue(form.is_valid())


class IndexViewTest(TestCase):

    def test_index_view(self):
        response = self.client.get(reverse('home page'))
        self.assertTemplateUsed(response, 'home_page.html')
        self.assertEqual(response.status_code, 200)


class DriverApplicationViewTest(TestCase):

    def test_driver_application_view_get(self):
        response = self.client.get(reverse('driver apply'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')
        self.assertIsInstance(response.context['form'], DriverApplicationForm)

    def test_driver_application_view_post_with_valid_data(self):
        data = {
            **FormTests.VALID_APPLICATION_DATA,
            **FormTests.VALID_ADDRESS_DATA
        }
        response = self.client.post(reverse('driver apply'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DriverApplication.objects.count(), 1)


class ContactUsViewTest(TestCase):
    VALID_DATA = {
        'Name': 'TestCompany',
        'Email': 'test@test.com',
        'Phone': '2242245454',
        'Message': 'test message'
    }
    INVALID_DATA = {
        'Name': 'TestCompany',
        'Email': 'testtestcom',
        'Phone': '92242245454',
        'Message': 'test message'
    }

    def test_contact_us_view_get(self):
        response = self.client.get(reverse('contact us'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')
        self.assertTemplateUsed(response, 'contact_us_page.html')

    def test_contact_us_view_post_with_valid_data(self):
        response = self.client.post(reverse('contact us'), ContactUsViewTest.VALID_DATA)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactUsModel.objects.count(), 1)

    def test_contact_us_view_post_with_invalid_data(self):
        response = self.client.post(reverse('contact us'), ContactUsViewTest.INVALID_DATA)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(ContactUsModel.objects.count(), 0)


class MessageViewTest(TestCase):
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
        self.client.post(reverse('contact us'), ContactUsViewTest.VALID_DATA)

    def test_load_massages(self):
        self.client.login(**self.login_data)
        message = ContactUsModel.objects.get()
        response = self.client.get(reverse('messages'))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, message.Name)
        self.assertContains(response, message.Email)

    def test_read_message_view(self):
        self.client.login(**self.login_data)
        message = ContactUsModel.objects.get()
        response = self.client.get(reverse('message read', args=[message.pk]))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, message.Name)
        self.assertContains(response, message.Email)

    def test_delete_message_view(self):
        self.client.login(**self.login_data)
        message = ContactUsModel.objects.get()
        response = self.client.get(reverse('message delete', args=[message.pk]))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'delete_message_page.html')

    def test_message_deleted(self):
        self.client.login(**self.login_data)
        message = ContactUsModel.objects.get()
        response = self.client.post(reverse('message delete', args=[message.pk]))
        self.assertEqual(302, response.status_code)
        self.assertFalse(ContactUsModel.objects.filter(pk=message.pk).exists())
