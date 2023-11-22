"""
MiCADO Submission Engine TOSCA Utilities
---------------------------------------
Handles various TOSCA features not supported by the TOSCA Parser

Eg. instance_count and occurrences from TOSCA v1.3
"""

import copy

from micadoparser.utils.utils import resolve_get_functions

CUSTOM_TYPE_MAP = {
    "secret": "string"
}

TOSCA_INPUT_TYPES = [
    "map",
    "list",
    "string",
    "integer",
    "boolean",
    "float",
    "timestamp"
]

def is_v1_3(tpl):
    """
    Check if template is of TOSCA v1.3
    """
    return tpl.get("tosca_definitions_version") == "tosca_simple_yaml_1_3"


def fix_version(tpl):
    """
    Check if template is of TOSCA v1.3
    """
    tpl["tosca_definitions_version"] = "tosca_simple_yaml_1_2"


def resolve_occurrences(tpl_dict, parsed_params):
    """
    Handle TOSCA v1.3 occurrences feature, for multiple occurrences of
    a node that require different properties pulled from a list of inputs

    For occurrences where different properties are not required, store
    the occurrences count in the node metadata
    """
    nodes = tpl_dict.get("topology_template", {}).get("node_templates")
    inputs = _determine_inputs(tpl_dict, parsed_params)

    nodes_with_occurrences = {
        name: node
        for name, node in nodes.items()
        if "occurrences" or "instance_count" in node
    }

    for name, node in nodes_with_occurrences.items():
        count = _get_instance_count(node, inputs)
        occurrences = node.pop("occurrences", None)
        _validate_values(count, occurrences)
        if not count:
            node.setdefault("metadata", {})["occurrences"] = occurrences
            continue

        old_node = nodes.pop(name)
        new_nodes = _create_occurrences(count, name, old_node, inputs)
        nodes.update(new_nodes)

def fix_custom_input_types(tpl_dict):
    input_dict = tpl_dict.get("topology_template", {}).get("inputs", {})
    for name, field in input_dict.items():
        input_type = field.get("type")
        if input_type in TOSCA_INPUT_TYPES:
            continue
        if input_type not in CUSTOM_TYPE_MAP:
            raise TypeError(f"Unsupported input type {input_type} for {name}!")
        field["type"] = CUSTOM_TYPE_MAP[input_type]


def _validate_values(count, occurrences):
    """
    Validate instance_count and occurrences values
    """
    if occurrences and not all(
        [
            isinstance(occurrences, list),
            len(occurrences) == 2,
            isinstance(occurrences[0], int),
        ]
    ):
        raise ValueError("occurrences should be a two-item list of integers")
    elif (
        count
        and occurrences
        and any(
            [
                str(count) > str(occurrences[1]),
                count < occurrences[0],
            ]
        )
    ):
        raise ValueError("instance_count is out of bounds")


def _determine_inputs(tpl_dict, parsed_params):
    """
    Store input values from parsed_params or defaults
    """
    params = parsed_params if parsed_params else {}
    inputs = tpl_dict.get("topology_template", {}).get("inputs", {})
    values = {}
    for key, value in inputs.items():
        values[key] = params.get(key) or value["default"]
    return values


def _get_instance_count(node, inputs):
    """
    Return the instance count
    """
    count = node.pop("instance_count", None)
    if not count:
        return None

    if isinstance(count, str):
        count = int(count)
    elif isinstance(count, dict):
        try:
            count = int(inputs[count["get_input"]])
        except (KeyError, TypeError):
            raise KeyError("Could not resolve instance_count input")
    return count


def _create_occurrences(count, name, node, inputs):
    """
    Remove occurrences and instance count keys
    """

    new_nodes = {}
    for i in range(count):
        new_name = f"{name}-{i+1}"
        new_node = copy.deepcopy(node)
        resolve_get_functions(
            new_node,
            "get_input",
            lambda x: isinstance(x, list),
            _set_indexed_input,
            inputs,
            i,
        )

        new_nodes[new_name] = new_node

    return new_nodes


def _set_indexed_input(result, inputs, index):
    """
    Set the value of indexed inputs
    """
    if result[1] != "INDEX":
        raise TypeError("Unrecognised get_input format")
    try:
        return inputs[result[0]][index]
    except IndexError:
        raise IndexError(
            f"Input '{result[0]}' does not match node occurrences!"
        ) from None
