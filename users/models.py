from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                related_name='profile')
    full_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    avatar = ProcessedImageField(
        upload_to='avatars/',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 90},
        null=True, blank=True
    )

    # Track when the profile was updated
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"