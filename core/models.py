from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
import string
from django.core.files import File
from io import BytesIO
import random
import qrcode

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
    


class UserLink(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='links'
    )
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True)
    custom_alias = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    click_count = models.PositiveIntegerField(default=0)


    def save(self , *args , **kwargs):
        if not self.short_code:
            self.short_code = self.generate_short_code()

        super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"
    
    def generate_short_code(self , length=6):
        characters = string.ascii_letters + string.digits
        while True:
            code = ''.join(random.choices(characters,k=length))
            if not UserLink.objects.filter(short_code=code).exists():
                return code
            
    def short_url(self):
        return f"/{self.short_code}"

    def generate_qr_code(self):
        """Create QR code for the short URL."""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(self.short_url())
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        blob = BytesIO()
        img.save(blob, 'PNG')
        self.qr_code.save(f"{self.short_code}.png", File(blob), save=False)



class ClickEvent(models.Model):
    link = models.ForeignKey(
        UserLink,
        on_delete=models.CASCADE,
        related_name='clicks'
    )
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    referrer = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.link.short_url} clicked at {self.timestamp}"
