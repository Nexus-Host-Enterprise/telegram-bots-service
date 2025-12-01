from jinja2 import Environment, FileSystemLoader, select_autoescape
import os

BASE_TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")

env = Environment(
    loader=FileSystemLoader(BASE_TEMPLATES_DIR),
    autoescape=select_autoescape()
)

def render_template(template_name: str, context: dict) -> str:
    tpl = env.get_template(f"{template_name}/template.py.j2")
    return tpl.render(**context)
