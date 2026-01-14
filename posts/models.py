from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings
from django.utils.text import slugify

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(blank=True)

    # ManyToMany for Tags
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    # ManyToMany for Likes (Users who liked this post)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                   related_name='liked_posts')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Newest posts first by default

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