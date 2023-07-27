from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse

from SU_Transportation.accounts.forms import SuUserEditForm
from SU_Transportation.accounts.models import SuUser

UserModel = get_user_model()


class ModelValidatorTest(TestCase):

    def test_profileCreate_whenInvalidName(self):
        p = UserModel(
            username='SomeUser',
            password='Mpp#1983',
            email='test@test.com',
            first_name='George5',
            last_name='Ivanov',
            gender='Male',
        )

        try:
            p.full_clean()
            p.save()
            self.fail()
        except ValidationError as ex:
            self.assertIsNotNone(ex)

    def test_profileCreate_whenInvalidImageSize(self):
        p = UserModel(
            username='SomeUser',
            password='Mpp#1983',
            email='test@test.com',
            profile_picture='C:\\Users\\moni\\PycharmProjects\\SU_Transportation\\media\\images\\test_img.jpg',
            first_name='George',
            last_name='Ivanov',
            gender='Male',
        )
        try:
            p.full_clean()
            p.save()
            self.fail()
        except ValidationError as ex:
            self.assertIsNotNone(ex)


class FormTests(TestCase):
    VALID_DATA = {
        'username' : 'SomeUser',
        'first_name' : 'George',
        'last_name' : 'Ivanov',
        'email' : 'test@test.com',
        'gender' : 'Male',
    }

    INVALID_DATA = {
        'username': 'SomeUser',
        'first_name': 'G',
        'last_name': 'Ivanov7',
        'email': 'test@test.com',
        'gender': 'Male',
    }

    def test_postEditForm_whenValid(self):
        form = SuUserEditForm(FormTests.VALID_DATA)

        self.assertTrue(form.is_valid())

    def test_postEditForm_whenInValid(self):
        form = SuUserEditForm(FormTests.INVALID_DATA)

        self.assertFalse(form.is_valid())


class RegisterViewTests(TestCase):
    VALID_DATA = {
        'username': 'SomeUser',
        'email': 'test@test.com',
        'password1': 'Mpp#1983',
        'password2': 'Mpp#1983'
    }

    INVALID_DATA = {
        'username': 'SomeUser',
        'email': 'test@test.com',
        'password1': 'user',
        'password2': 'user',
    }

    def test_postRegister_whenValidData(self):
        response = self.client.post(reverse('register user'), RegisterViewTests.VALID_DATA)

        person = SuUser.objects.get()

        self.assertIsNotNone(person)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, '/')

    def test_postRegister_whenInvalidData(self):
        response = self.client.post(reverse('register user'), RegisterViewTests.INVALID_DATA)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())


class LoginLogoutViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(
            username='TestUser',
            email='test@test.com',
            password='Mpp#1983'
        )
        self.login_data = {
            'username': 'TestUser',
            'password': 'Mpp#1983',
        }

    def test_login_view_correct_template(self):
        self.client.login(**self.login_data)
        response = self.client.get(reverse('login user'))
        self.assertTemplateUsed(response, 'login-user.html')

    def test_valid_user_login(self):
        response = self.client.post(reverse('login user'), self.login_data)
        self.assertRedirects(response, reverse('home page'))

    def test_invalid_user_login(self):
        invalid_data = {
            'username': 'TestUser',
            'password': 'wrong',
        }
        response = self.client.post(reverse('login user'), invalid_data)
        self.assertContains(response, 'Please enter a correct username and password.')

    def test_logout_user(self):
        self.client.login(**self.login_data)
        response = self.client.get(reverse('logout user'))
        self.assertRedirects(response, reverse('home page'))


class DetailsUserViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(
            username='TestUser',
            email='test@test.com',
            password='Mpp#1983'
        )
        self.client.login(username='TestUser', password='Mpp#1983')
        self.url = reverse('profile details', args=[self.user.pk])

    def test_user_detail_view_return_200_and_load_correct_data(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.email)


class EditUserViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(
            username='TestUser',
            email='test@test.com',
            password='Mpp#1983'
        )
        self.client.login(username='TestUser', password='Mpp#1983')
        self.url = reverse('profile edit', args=[self.user.pk])

    def test_edit_user_view_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_edit_user_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'edit-user.html')

    def test_edit_user_view_updates_user_data(self):
        data = {
            'username': 'UpdateName',
            'first_name': 'FName',
            'last_name': 'LName',
            'email': 'new@new.com',
            'gender': 'Male',
        }

        response = self.client.post(reverse('profile edit', args=[self.user.pk]), data)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'UpdateName')
        self.assertEqual(self.user.gender, 'Male')

    def test_edit_user_view_returns_404_for_invalid_id(self):
        invalid_url = reverse('profile edit', args=[self.user.pk + 1])
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)


class DeleteUserViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(
            username='TestUser',
            email='test@test.com',
            password='Mpp#1983'
        )
        self.client.login(username='TestUser', password='Mpp#1983')
        self.url = reverse('profile delete', args=[self.user.pk])

    def test_delete_user_view_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_delete_user_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'delete-user.html')

    def test_delete_user_view_deletes_user(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(UserModel.objects.filter(pk=self.user.pk).exists())

