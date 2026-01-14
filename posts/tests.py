from io import BytesIO
from PIL import Image
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Post, Tag
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

        # Verify DB state
        self.assertTrue(self.user in self.post.likes.all())

        # 2. Second click (Unlike)
        response = self.client.post(self.url)
        data = json.loads(response.content)
        self.assertFalse(data['liked'])
        self.assertEqual(data['count'], 0)