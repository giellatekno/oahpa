import datetime
from django import template
from django.template import Context

from django.template.loader import get_template

register = template.Library()

@register.simple_tag
def header_js_includes():
	return get_template('header_includes.html').render(Context())
