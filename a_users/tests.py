from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .models import Profile

class ProfileModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")

        # Delete existing profile if it exists
        existing_profile = Profile.objects.filter(user=self.user)
        if existing_profile.exists():
            existing_profile.delete()

        # Now create a new profile
        self.profile = Profile.objects.create(
            user=self.user,
            image=self.image,
            realname='Test Realname',
            email='test@example.com',
            location='Test Location',
            bio='Test Bio'
        )

    # def tearDown(self):
    #     self.user.delete()
    #     self.profile.delete()

    def test_profile_model(self):
        self.assertEqual(str(self.profile), 'testuser')
        self.assertEqual(self.profile.name, 'Test Realname')
    
        expected_avatar_path = f'/media/{self.profile.image.name}'
        self.assertEqual(self.profile.avatar, expected_avatar_path)

    def test_default_avatar(self):
        # Delete existing profile if it exists
        existing_profile = Profile.objects.filter(user=self.user)
        if existing_profile.exists():
            existing_profile.delete()
        profile_without_image = Profile.objects.create(user=self.user)
        self.assertEqual(profile_without_image.avatar, '/static/images/avatar_default.svg')

    def test_default_name(self):
        # Delete existing profile if it exists
        existing_profile = Profile.objects.filter(user=self.user)
        if existing_profile.exists():
            existing_profile.delete()
        profile_without_realname = Profile.objects.create(user=self.user)
        self.assertEqual(profile_without_realname.name, 'testuser')


class ProfilePageTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_profile_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_userprofile_view(self):
        self.client.logout()
        response = self.client.get(reverse('userprofile', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)

   
    # def test_media_url(self):
    #     response = self.client.get(settings.MEDIA_URL + 'test_image.jpg')
    #     # Assuming that this should return a 404 (status code 404) for a non-existent media file
    #     self.assertEqual(response.status_code, 404)