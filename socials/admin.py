from django.contrib import admin
from .models import SocialLink


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['platform', 'icon_emoji', 'is_active', 'order']
    list_filter = ['is_active', 'platform']
    list_editable = ['is_active', 'order']
    fieldsets = (
        ('Platform Info', {
            'fields': ('platform', 'icon_emoji')
        }),
        ('Link', {
            'fields': ('url',)
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )
    ordering = ['order']
