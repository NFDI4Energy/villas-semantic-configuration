# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictBytes, StrictStr
from typing import Optional, Tuple, Union
from typing_extensions import Annotated
from vsc_api.models.villas_config import VillasConfig


class BaseSemanticsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseSemanticsApi.subclasses = BaseSemanticsApi.subclasses + (cls,)
    async def semantify_file(
        self,
        body: Annotated[Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]], Field(description="The binary string containing the JSON file")],
        output_mime_type: Optional[str],
    ) -> bytes:
        """This endpoint takes an octet-stream and attempts to parse JSON from it and then attempts the conversion to RDF. The result is an octet-stream that includes the RDF version. Serialization format can be decided via query parameters."""
        ...


    async def semantify_json(
        self,
        villas_config: Annotated[VillasConfig, Field(description="JSON string that conforms to VILLAS node configuration")],
    ) -> str:
        """This endpoint takes the VILLAS configuration as a JSON string. It performs schema validation against the official VILLAS node configuration schema. Different RDF serializations can be picked using the Accept Header."""
        ...


    async def jsonld_context(
        self,
    ) -> str:
        """This endpoint provides the JSON LD context needed when working with the JSON LD output of this API."""
        ...
