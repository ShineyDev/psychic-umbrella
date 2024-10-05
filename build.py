from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from jinja2 import Environment

import os
import shutil
import sys

import jinja2 as jinja


path_static = "_static"


def render_error(environment: Environment, base_hostname: str | None, /, *, code: int, message: str) -> str:
    template = environment.get_template("error.html")

    return template.render(
        base_hostname=base_hostname,
        error_code=code,
        error_message=message,
        home_url="/",
        path_static=path_static,
    )


def render_index(environment: Environment, base_hostname: str | None, /) -> str:
    template = environment.get_template("index.html")

    return template.render(
        base_hostname=base_hostname,
        path_static=path_static,
    )


def main():
    try:
        base_hostname = sys.argv[1]
    except IndexError:
        base_hostname = None

    environment = jinja.Environment(
        autoescape=jinja.select_autoescape(),
        loader=jinja.FileSystemLoader("template"),
    )

    pages = {
        "404": render_error(environment, base_hostname, code=404, message="Whoops! This page doesn't exist."),
        "index": render_index(environment, base_hostname),
    }

    try:
        shutil.rmtree("./build")
    except FileNotFoundError:
        pass

    os.mkdir("./build")

    for page_name, page_content in pages.items():
        with open(f"./build/{page_name}.html", "w+") as stream:
            stream.write(page_content)

    shutil.copytree("./static", f"./build/{path_static}")

    return None


if __name__ == "__main__":
    main()
