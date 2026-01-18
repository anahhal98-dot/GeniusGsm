from django.db import models


class SocialLink(models.Model):
    """Social Media Links Model"""
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter (X)'),
        ('linkedin', 'LinkedIn'),
        ('whatsapp', 'WhatsApp'),
        ('instagram', 'Instagram'),
        ('github', 'GitHub'),
        ('youtube', 'YouTube'),
        ('telegram', 'Telegram'),
    ]
    
    platform = models.CharField(
        max_length=50,
        choices=PLATFORM_CHOICES,
        unique=True,
        verbose_name="Platform"
    )
    url = models.URLField(verbose_name="URL")
    icon_emoji = models.CharField(
        max_length=10,
        default="🌐",
        verbose_name="Icon/Emoji"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Display Order"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"
    
    def __str__(self):
        return f"{self.get_platform_display()} - {self.url}"
