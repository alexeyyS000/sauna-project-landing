from django import template
from django.template import Context, Template

register = template.Library()

@register.filter
def render_template(value, context=None):

    if not value:
        return ""
    try:
        template = Template(value)

        return template.render(Context(context or {}))
    except Exception as e:

        return f"Error rendering template: {e}"
