from django.db import models
from django.utils import timezone
from datetime import timedelta
import string
import random

# ShortURL Model For Anonymous Users

class AnonymousShortURL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField()
    click_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        # Generate short code if not provided
        if not self.short_code:
            self.short_code = self.generate_short_code()

        # Set expiry to 3 months from creation
        if not self.expire_at:
            self.expire_at = timezone.now() + timedelta(days=90)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"

    def generate_short_code(self, length=6):
        """Generate a random alphanumeric short code."""
        characters = string.ascii_letters + string.digits
        while True:
            code = ''.join(random.choices(characters, k=length))
            if not AnonymousShortURL.objects.filter(short_code=code).exists():
                return code

    def short_url(self):
        """Return the full short URL path."""
        return f"/{self.short_code}"
