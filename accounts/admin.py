from django.contrib import admin
from .models import *


admin.site.register(CustomUser)

# @admin.register(UserLink)
# class UserLinkAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'user',
#         'original_url',
#         'short_url',
#         'is_active',
#         'created_at',
#         'expire_at',
#     )
#     list_filter = ('is_active', 'created_at', 'expire_at')
#     search_fields = ('original_url', 'short_url', 'user__email')
#     readonly_fields = ('qr_code', 'created_at')
#     ordering = ('-created_at',)

#     fieldsets = (
#         ('Link Info', {
#             'fields': ('user', 'original_url', 'short_url', 'short_path', 'custom_alias', 'qr_code')
#         }),
#         ('Settings', {
#             'fields': ('expire_at', 'password', 'is_active')
#         }),
#         ('Timestamps', {
#             'fields': ('created_at',)
#         }),
#     )

#     def get_queryset(self, request):
#         """Optimize query performance."""
#         return super().get_queryset(request).select_related('user')


# @admin.register(ClickEvent)
# class ClickEventAdmin(admin.ModelAdmin):
#     list_display = ('id', 'link', 'ip_address', 'timestamp', 'referrer')
#     list_filter = ('timestamp',)
#     search_fields = ('ip_address', 'referrer', 'link__short_url')
#     ordering = ('-timestamp',)
