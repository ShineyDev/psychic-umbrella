from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from jinja2 import Environment

import os
import shutil

import jinja2 as jinja


path_static = "_static"


def render_error(environment: Environment, /, *, code: int, message: str) -> str:
    template = environment.get_template("error.html")

    return template.render(
        base_hostname="psychic-umbrella.shiney.dev",
        error_code=code,
        error_message=message,
        home_url="/",
        path_static=path_static,
    )


def render_index(environment: Environment, /) -> str:
    template = environment.get_template("index.html")

    return template.render(
        base_hostname="psychic-umbrella.shiney.dev",
        path_static=path_static,
    )


def main():
    environment = jinja.Environment(
        autoescape=jinja.select_autoescape(),
        loader=jinja.FileSystemLoader("template"),
    )

    pages = {
        "404": render_error(environment, code=404, message="Whoops! This page doesn't exist."),
        "index": render_index(environment),
    }

    os.mkdir("./build")

    for page_name, page_content in pages.items():
        with open(f"./build/{page_name}.html", "w+") as stream:
            stream.write(page_content)

    shutil.copytree("./static", f"./build/{path_static}")

    return None


if __name__ == "__main__":
    main()
