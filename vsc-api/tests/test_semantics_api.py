# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictBytes, StrictStr  # noqa: F401
from typing import Optional, Tuple, Union  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from vsc_api.models.villas_config import VillasConfig  # noqa: F401


def test_semantify_file(client: TestClient):
    """Test case for semantify_file

    Convert JSON configuration file to semantic counterpart in RDF
    """
    body = None
    params = [("output_mime_type", 'text/turtle')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/semantify-file",
    #    headers=headers,
    #    json=body,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_semantify_json(client: TestClient):
    """Test case for semantify_json

    Insert a new data source meta record
    """
    villas_config = vsc_api.VillasConfig()

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/semantify-json",
    #    headers=headers,
    #    json=villas_config,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_jsonld_context(client: TestClient):
    """Test case for jsonld_context

    Get the jsonld context to be used with the jsonld version from this API
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/jsonld-context",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

