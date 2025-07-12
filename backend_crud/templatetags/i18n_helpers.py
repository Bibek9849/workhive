from django import template
from django.conf import settings

register = template.Library()

@register.filter
def remove_language_prefix(path):
    lang_codes = [code for code, _ in settings.LANGUAGES]
    
    # Check if path starts with a language code
    parts = path.strip("/").split("/", 1)
    if parts and parts[0] in lang_codes:
        return "/" + parts[1] if len(parts) > 1 else "/"
    return path