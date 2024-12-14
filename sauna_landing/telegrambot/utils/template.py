from jinja2 import Environment, FileSystemLoader
from django.conf import settings
# Укажите папку с шаблонами
env = Environment(loader=FileSystemLoader(settings.TG_TEMPLATE_DIR))

def render_template(template_name, context):
    template = env.get_template(template_name)
    return template.render(context)
