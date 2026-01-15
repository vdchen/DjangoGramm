from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils.text import slugify
from django.contrib.auth import get_user_model

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

User = get_user_model()

class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    caption = models.TextField(blank=True)

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='posts'
    )

    likes = models.ManyToManyField(
        User,
        blank=True,
        related_name='liked_posts'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def total_likes(self):
        return self.likes.count()


class PostImage(models.Model):
    post = models.ForeignKey('Post', related_name='images',
                             on_delete=models.CASCADE)


    image = ProcessedImageField(
        upload_to='posts/%Y/%m/%d/',
        processors=[ResizeToFill(1080, 1080)],
        format='JPEG',
        options={'quality': 85}  # Compresses the image to save space
    )