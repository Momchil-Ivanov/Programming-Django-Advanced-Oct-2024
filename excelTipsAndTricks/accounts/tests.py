from django.conf import settings
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from excelTipsAndTricks.accounts.models import UserProfile


class UserProfileTests(TestCase):
    def test_user_profile_creation(self):
        # Create a new user
        user = User.objects.create_user(username='testuser', password='testpassword')
        user.save()  # Ensure the user is saved
        user_profile = UserProfile.objects.get(user=user)

        # Verify that the UserProfile was created
        self.assertTrue(UserProfile.objects.filter(user=user).exists())
        user_profile = UserProfile.objects.get(user=user)
        self.assertEqual(user_profile.user, user)

class UserProfilePictureTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.get(user=self.user)

    def test_get_profile_picture_uploaded(self):
        # Simulate a profile picture upload
        self.user_profile.profile_picture = 'profile_pictures/test_image.jpg'
        self.user_profile.save()

        # Use MEDIA_URL to build the correct path
        self.assertEqual(
            self.user_profile.get_profile_picture(),
            f'{settings.MEDIA_URL}profile_pictures/test_image.jpg'
        )


class UserProfileIntegrationTests(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'password123'
        UserProfile.objects.all().delete()
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.user)

    def test_user_registration_and_profile_creation(self):
        # Check that the user has been created successfully
        user = User.objects.get(username=self.username)
        self.assertEqual(user.username, self.username)

        # Check that a UserProfile was created for the user
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(user_profile.user, self.user)

    def test_profile_update(self):
        # Update the profile picture
        self.user_profile.profile_picture = 'profile_pictures/new_image.jpg'
        self.user_profile.save()

        # Retrieve the updated profile and check the change
        updated_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(updated_profile.profile_picture, 'profile_pictures/new_image.jpg')

    def test_user_login_and_profile_access(self):
        # Simulate user login
        self.client.login(username=self.username, password=self.password)

        # Check that the user can access their profile page (assuming you have a URL for this)
        response = self.client.get(reverse('profile'))  # Adjust with actual URL name
        self.assertEqual(response.status_code, 200)

        # Ensure the profile information is included in the response (assuming you show profile info)
        self.assertContains(response, self.username)