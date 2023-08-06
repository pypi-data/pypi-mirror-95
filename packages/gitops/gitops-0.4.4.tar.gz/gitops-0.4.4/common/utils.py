import os
import yaml


def load_yaml(path, default_value=None):
    try:
        with open(path, 'r') as file:
            return resolve_values(yaml.safe_load(file), path)
    except Exception:
        if default_value is not None:
            return default_value
        raise


def resolve_values(values, path):
    if 'extends' not in values:
        return values
    parent_values = load_yaml(os.path.join(os.path.dirname(path), values['extends']))
    return deep_merge(parent_values, values)


def deep_merge(parent, child):
    """ Deeply merge two dictionaries.

    Dictionary entries will be followed and merged, anything else will be
    replaced. If the child dictionary has overlapping values. `child` is merged
    into `parent`. The operation is in-place, but the result is still returned.
    """
    for key, value in child.items():
        parent_value = parent.get(key)
        if isinstance(parent_value, dict):
            if isinstance(value, dict):
                deep_merge(parent_value, value)
            else:
                parent[key] = value
        else:
            parent[key] = value
    return parent
