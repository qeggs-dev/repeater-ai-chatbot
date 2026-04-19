import aiofiles
import environs
import pydantic
import fastapi
import python_multipart
import loguru
import openai
import orjson
import uvicorn
import markdown
import httpx
import numpy
import yaml
import box
import tzdata
import jinja2
import yarl
import bleach
import asteval

from ._module_unit import ModuleUnit

modules_list = [
    ModuleUnit(
        module = aiofiles,
        expected_version = "25.1.0",
    ),
    ModuleUnit(
        module = environs,
        expected_version = "14.5.0",
    ),
    ModuleUnit(
        module = pydantic,
        expected_version = "2.12.5",
    ),
    ModuleUnit(
        module = fastapi,
        expected_version = "0.129.0",

    ),
    ModuleUnit(
        module = python_multipart,
        expected_version = "0.0.22",
    ),
    ModuleUnit(
        module = loguru,
        expected_version = "0.7.3",
    ),
    ModuleUnit(
        module = openai,
        expected_version = "2.21.0",
    ),
    ModuleUnit(
        module = orjson,
        expected_version = "3.11.7",
    ),
    ModuleUnit(
        module = uvicorn,
        expected_version = "0.40.0",
    ),
    ModuleUnit(
        module = markdown,
        expected_version = "3.10.2",
    ),
    ModuleUnit(
        module = httpx,
        expected_version = "0.28.1",
    ),
    ModuleUnit(
        module = numpy,
        expected_version = "2.4.2",
    ),
    ModuleUnit(
        module = yaml,
        expected_version = "6.0.3",
    ),
    ModuleUnit(
        module = box,
        expected_version = "7.3.2",
    ),
    ModuleUnit(
        module = tzdata,
        expected_version = "2025.3",
    ),
    ModuleUnit(
        module = jinja2,
        expected_version = "3.1.6",
    ),
    ModuleUnit(
        module = yarl,
        expected_version = "1.23.0",
    ),
    ModuleUnit(
        module = bleach,
        expected_version = "6.3.0",
    ),
    ModuleUnit(
        module = asteval,
        expected_version = "1.0.8",
    ),
]