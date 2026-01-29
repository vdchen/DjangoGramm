from io import BytesIO

import pytest
from PIL import Image
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from users.models import Follow
from .models import Post, Tag, PostImage
import json

User = get_user_model()


# --- HELPER FUNCTION TO CREATE A REAL IMAGE ---
def create_test_image():
    file = BytesIO()
    # Create a 100x100 white square
    image = Image.new('RGB', (100, 100),
                      'white')
    image.save(file, 'JPEG')
    file.name = 'test.jpg'
    file.seek(0)
    return SimpleUploadedFile(file.name, file.read(),
                              content_type='image/jpeg')


class TagModelTest(TestCase):
    def test_tag_slug_generation(self):
        """Test that the save() method on Tag automatically generates a slug."""
        tag = Tag.objects.create(name="Python Coding")
        self.assertEqual(tag.slug, "python-coding")


class PostCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester',
                                             password='password')
        self.client = Client()
        self.client.login(username='tester', password='password')
        self.url = reverse('post_create')

    def test_create_post_with_tags(self):
        image = create_test_image()

        data = {
            'caption': 'Hello Berlin!',
            'tags_str': 'berlin, python, django',
            'images': [image]
        }

        response = self.client.post(self.url, data, follow=True)

        self.assertEqual(response.status_code, 200)

        post = Post.objects.first()
        self.assertEqual(post.caption, 'Hello Berlin!')
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.tags.count(), 3)
        self.assertTrue(post.tags.filter(name='berlin').exists())

    def test_create_post_duplicate_tags(self):
        image = create_test_image()

        data = {
            'caption': 'Testing duplicates',
            'tags_str': 'python, Python, PYTHON',
            'images': [image]
        }

        self.client.post(self.url, data)

        post = Post.objects.first()
        self.assertEqual(post.tags.count(), 1)
        self.assertEqual(post.tags.first().name, 'python')

@pytest.mark.django_db
def test_friends_first_ordering():
    # 1. Setup: Create 3 users
    vlad = User.objects.create_user(username='vlad', email='v@test.com')
    friend = User.objects.create_user(username='friend', email='f@test.com')
    stranger = User.objects.create_user(username='stranger', email='s@test.com')

    # 2. Vlad follows the friend
    Follow.objects.create(follower=vlad, following=friend)

    # 3. Create posts (Stranger posts later, Friend posts earlier)
    Post.objects.create(author=friend, content="Friend post")
    Post.objects.create(author=stranger, content="Stranger post")

    # 4. Act: Get the feed using your logic
    # (Assuming your feed logic is in a function or we call the view)
    from posts.views import feed_view # If you extract the logic
    posts = list(feed_view(vlad))

    # 5. Assert: The first post should be from the friend, even if it's older
    # because of our 'priority' annotation.
    assert posts[0].author == friend
    assert posts[1].author == stranger

#AJAX Logic
class LikeFunctionalityTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='liker',
                                             password='password')
        self.client = Client()
        self.client.login(username='liker', password='password')

        # Create a post to like
        self.post = Post.objects.create(author=self.user, caption="Like me!")
        self.url = reverse('toggle_like', args=[self.post.id])

    def test_like_and_unlike(self):
        # 1. First click (Like)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertTrue(data['liked'])
        self.assertEqual(data['count'], 1)


        self.assertTrue(self.post.likes.filter(id=self.user.id).exists())

        # 2. Second click (Unlike)
        response = self.client.post(self.url)
        data = json.loads(response.content)
        self.assertFalse(data['liked'])
        self.assertEqual(data['count'], 0)

        # Verify DB state: ensure the user is gone
        self.assertFalse(self.post.likes.filter(id=self.user.id).exists())


@pytest.mark.django_db
@patch('cloudinary.uploader.upload') # This mocks the actual network call to Cloudinary
def test_post_image_upload_mocked(mock_upload, user):
    # 1. Setup a fake response from Cloudinary
    mock_upload.return_value = {
        'public_id': 'test_id',
        'url': 'http://res.cloudinary.com/demo/image/upload/v123/test.jpg',
        'secure_url': 'https://res.cloudinary.com/demo/image/upload/v123/test.jpg',
    }

    # 2. Create a fake image file in memory
    fake_image = SimpleUploadedFile(
        name='test_image.jpg',
        content=b'file_content',
        content_type='image/jpeg'
    )

    # 3. Create the post and image
    post = Post.objects.create(author=user, content="Test Post")
    img_instance = PostImage.objects.create(post=post, image=fake_image)

    # 4. Assertions
    assert PostImage.objects.count() == 1
    # Check that our "fake" upload was called exactly once
    assert mock_upload.called
