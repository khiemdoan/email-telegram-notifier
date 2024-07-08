__author__ = 'Khiem Doan'
__github__ = 'https://github.com/khiemdoan'
__email__ = 'doankhiem.crazy@gmail.com'
__url__ = 'https://github.com/khiemdoan/clean-architecture-python-boilerplate/blob/main/src/templates/__init__.py'

__all__ = ['arender', 'render']

from asyncio import to_thread
from pathlib import Path
from typing import Any

from jinja2 import FileSystemLoader, select_autoescape
from jinja2.nativetypes import NativeEnvironment

this_dir = Path(__file__).parent
env = NativeEnvironment(
    loader=FileSystemLoader(this_dir),
    autoescape=select_autoescape(['html', 'xml']),
)


def render(file: str, context: dict[str, Any] = {}, **kwargs) -> str:
    template = env.get_template(file)
    return template.render(context, **kwargs)


async def arender(file: str, context: dict[str, Any] = {}, **kwargs) -> str:
    return await to_thread(render, file, context, **kwargs)
