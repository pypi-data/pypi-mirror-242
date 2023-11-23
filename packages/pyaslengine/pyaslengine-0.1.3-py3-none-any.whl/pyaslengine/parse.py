"""pyaslengine.parse"""

from jsonpath_ng import parse

from pyaslengine.log import get_logger

logger = get_logger(__name__)


def single_value_from_path(jsonpath, data, default=None, output=dict):
    expr = parse(jsonpath)
    matches = expr.find(data)

    if len(matches) > 1:
        raise ValueError(
            "JSONPatch match should match one and only one node, "
            "https://states-language.net/spec.html#ref-paths"
        )
    elif not matches:
        return default

    value = matches[0].value
    if output == dict:
        return value
    else:
        init_kwargs = {
            attr_name: single_value_from_path(jsonpath, data)
            for jsonpath, attr_name in output.asl_field_mapping.items()
        }
        return output(**init_kwargs)
