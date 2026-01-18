from django import template
from socials.models import SocialLink

register = template.Library()


@register.inclusion_tag('socials/social_links.html')
def show_social_links():
    """Display active social links"""
    social_links = SocialLink.objects.filter(is_active=True)
    return {'social_links': social_links}
