from django import template
from product.models import Files_upload

register = template.Library()


@register.simple_tag(takes_context=True)
def get_path(context, id):
    request = context['request']
    # files = Files_upload.objects.filter(user=request.user, id=id ).first()

    return "www.google.com"


@register.simple_tag(takes_context=False)
def get_value(dict, key):
    for key0, value0 in dict.items():
        if (key0 == key):
            return value0
    return ""


@register.simple_tag(takes_context=False)
def format_key_txt(key):
    tmp = str(key).split(':', 1)[1]
    return tmp.capitalize()
