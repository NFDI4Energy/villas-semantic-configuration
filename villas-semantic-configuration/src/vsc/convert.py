import importlib.resources
import json
import re

from jsonpath import patch
from rdflib import Graph

from vsc.parser import parse


def _inject_context(data: dict):
    context = json.loads(importlib.resources.read_binary(__package__, 'context.json'))
    data.update(context)


def semantify(data: dict) -> Graph:
    _inject_context(data)
    data_string = json.dumps(data)
    g = Graph()
    g.parse(data=data_string, format='json-ld')
    return g



def _expand_signal_string(signal_value: str | list):
    if isinstance(signal_value, list):
        for val in signal_value:
            val['@type'] = 'oeo:OEO_0042XXXX-message_attribute'
        return signal_value
    if isinstance(signal_value, str):
        count, signal_type = re.match(r"(\d+)([if])", signal_value).groups()
        count = int(count)

        signal_type_lookup = {
            "i": "integer",
            "f": "float",
            "b": "boolean",
            "c": "complex"
        }

        return [
            {
                "name": f'{signal_type_lookup[signal_type]}_{idx}',
                "type": signal_type_lookup[signal_type],
                "@type": "oeo:OEO_0042XXXX-message_attribute"
            }
            for idx in range(count)
        ]
    raise ValueError('signal value is neither list nor string')


def perform_document_manipulations(data: dict):
    """
    Apply structural rule based changes on the JSON document to improve output quality of the semantics
    :param dict data: Input data structure according to VILLAS config schema
    """

    for node_name, node in data['nodes'].items():
        node['@type'] = 'oeo:OEO_00420006'

        if 'in' in node:
            node['in'].update({
                "@type": "oeo:OEO_0042XXXX-simulation_connection_input_port",
                "id": f'{node_name}/input'
            })

            if 'signals' in node['in']:
                node['in']['schema'] = {
                    "@type": "oeo:OEO_0042XXXX-message_schema",
                    "signals": _expand_signal_string(node['in']['signals'])
                }
                del node['in']['signals']

        if 'out' in node:
            node['out'].update({
                "@type": "oeo:OEO_0042XXXX-simulation_connection_output_port",
                "id": f'{node_name}/output'
            })

            if 'signals' in node['out']:
                node['out']['schema'] = {
                    "@type": "oeo:OEO_0042XXXX-message_schema",
                    "signals": _expand_signal_string(node['out']['signals'])
                }
                del node['out']['signals']


def get_semantic_representation(
        data: dict | str | bytes,
        target_mime_type: str,
        skip_validation=False
) -> bytes | None:
    data = parse(data, skip_validation=skip_validation)

    perform_document_manipulations(data)

    g = semantify(data)

    supported_format_map = {
        'application/ld+json': 'json-ld',
        'application/rdf+xml': 'rdf',
        'text/turtle': 'longturtle'
    }

    if target_mime_type not in supported_format_map:
        return None

    return g.serialize(format=supported_format_map[target_mime_type], encoding='utf-8')
