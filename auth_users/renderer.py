from datetime import datetime
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader(Path(Path(__file__).parent, 'templates')),
    autoescape=select_autoescape(['html'])
)


def render(template: str, **kwargs) -> str:
    """
    Заполняет указанный шаблон и возвращает

    :param template: имя шаблона, например templates.html
    :return:
    """
    template: Any = env.get_template(template)
    rendered_page: str = template.render(**kwargs)
    return rendered_page
