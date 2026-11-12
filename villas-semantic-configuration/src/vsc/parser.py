import importlib.resources
import json
import yaml

import jsonschema
from openapi_core import OpenAPI
from openapi_core.datatypes import RequestParameters
from openapi_core.protocols import Request


class DummyRequest:  # implements the Request Protocol
    def __init__(self, body: bytes):
        self.host_url = "http://localhost:8080"
        self.path = "/semantify-json"
        self.method = "post"
        self.body = body
        self.content_type = "application/json"
        self.parameters = RequestParameters()


def parse(body: bytes | str | dict, skip_validation=False) -> dict:
    # if isinstance(data, (bytes, str)):
    #     data = json.loads(data)
    if isinstance(body, dict):
        body = json.dumps(body)
    if isinstance(body, str):
        body = body.encode("utf-8")

    if not skip_validation:
        with importlib.resources.open_text(__package__, 'openapi.yaml') as stream:
            # spec_dict = yaml.safe_load(stream)
            spec = OpenAPI.from_file(stream)

        try:
            spec.validate_request(DummyRequest(body))
        except TypeError as e:
            raise e

    return json.loads(body)
