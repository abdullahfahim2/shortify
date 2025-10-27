from django.contrib import admin
from .models import AnonymousShortURL

# register annonymous user model to admin panel
@admin.register(AnonymousShortURL)
class AnonymousShortURLAdmin(admin.ModelAdmin):
    list_display = ('short_code', 'original_url', 'created_at', 'expire_at', 'click_count')
    search_fields = ('short_code', 'original_url')
    list_filter = ('created_at', 'expire_at')
    readonly_fields = ('click_count',)
