import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Profile, Follow

User = get_user_model()


class UserSignalTests(TestCase):
    def test_profile_created_automatically(self):
        """
        Test that creating a CustomUser automatically creates a Profile
        via the post_save signal.
        """
        # Create a user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )

        # Check if Profile exists
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsInstance(user.profile, Profile)

        # Check default values
        self.assertEqual(user.profile.bio, "")

    def test_profile_str_method(self):
        """Test the string representation of the Profile model."""
        user = User.objects.create_user(username='vlad', password='123')
        self.assertEqual(str(user.profile), "Profile of vlad")


@pytest.mark.django_db
def test_follow_user():
    user_a = User.objects.create_user(username='vlad', password='password123')
    user_b = User.objects.create_user(username='mentor',
                                      password='password123')

    Follow.objects.create(follower=user_a, following=user_b)

    assert user_a.following.count() == 1
    assert user_b.followers.count() == 1