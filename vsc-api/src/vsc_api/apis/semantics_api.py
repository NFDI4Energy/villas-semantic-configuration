# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from vsc_api.apis.semantics_api_base import BaseSemanticsApi
import vsc_api.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from pydantic import Field, StrictBytes, StrictStr
from typing import Optional, Tuple, Union
from typing_extensions import Annotated
from vsc_api.models.villas_config import VillasConfig

router = APIRouter()

ns_pkg = vsc_api.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/semantify-file",
    responses={
        200: {"model": bytes, "description": "successful operation"},
        400: {"model": str, "description": "invalid JSON configuration input file"},
    },
    tags=["semantics"],
    summary="Convert JSON configuration file to semantic counterpart in RDF",
    response_model_by_alias=True,
)
async def semantify_file(
    body: Annotated[Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]], Field(description="The binary string containing the JSON file")] = Body(..., description="The binary string containing the JSON file"),
    output_mime_type: Optional[str] = Query('text/turtle', description="", alias="output-mime-type"),
) -> bytes:
    """This endpoint takes an octet-stream and attempts to parse JSON from it and then attempts the conversion to RDF. The result is an octet-stream that includes the RDF version. Serialization format can be decided via query parameters."""
    if not BaseSemanticsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSemanticsApi.subclasses[0]().semantify_file(body, output_mime_type)


@router.post(
    "/semantify-json",
    responses={
        200: {"model": str, "description": "successful operation"},
        400: {"model": str, "description": "Invalid JSON configuration input"},
    },
    tags=["semantics"],
    summary="Insert a new data source meta record",
    response_model_by_alias=True,
)
async def semantify_json(
    villas_config: Annotated[VillasConfig, Field(description="JSON string that conforms to VILLAS node configuration")] = Body(..., description="JSON string that conforms to VILLAS node configuration"),
) -> str:
    """This endpoint takes the VILLAS configuration as a JSON string. It performs schema validation against the official VILLAS node configuration schema. Different RDF serializations can be picked using the Accept Header."""
    if not BaseSemanticsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSemanticsApi.subclasses[0]().semantify_json(villas_config)


@router.get(
    "/jsonld-context",
    responses={
        200: {"model": str, "description": "successful operation"},
    },
    tags=["semantics"],
    summary="Get the jsonld context to be used with the jsonld version from this API",
    response_model_by_alias=True,
)
async def jsonld_context(
) -> str:
    """This endpoint provides the JSON LD context needed when working with the JSON LD output of this API."""
    if not BaseSemanticsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSemanticsApi.subclasses[0]().jsonld_context()
