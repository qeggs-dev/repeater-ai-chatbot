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
import pip_requirements_parser
import jsonpatch
import pythonping
import cachetools

modules_list = [
    aiofiles,
    environs,
    pydantic,
    fastapi,
    python_multipart,
    loguru,
    openai,
    orjson,
    uvicorn,
    markdown,
    httpx,
    numpy,
    yaml,
    box,
    tzdata,
    jinja2,
    yarl,
    bleach,
    asteval,
    pip_requirements_parser,
    jsonpatch,
    pythonping,
    cachetools,
]

name_map = {
    module.__name__: module for module in modules_list
}
name_map["python-multipart"] = python_multipart
name_map["pip-requirements-parser"] = pip_requirements_parser
name_map["python-box"] = box
name_map["pyyaml"] = yaml