from typing import MutableMapping, Any
import os
import toml
from typing import Dict, Union, SupportsFloat


def get_config() -> MutableMapping[str, Any]:
    """
    Returns the existing configuration from the local environment
    """
    try:
        with open(os.path.join(os.path.expanduser("~"), "maildown.toml")) as f:
            return toml.loads(f.read())
    except FileNotFoundError:
        pass
    return {}


def write_config(**config: Dict[str, Union[str, SupportsFloat, bool]]) -> None:
    """
    Updates the existing local config with the given additional arguments

    ### Parameters:

    - `config`: the new configuration items to add to the configuration

    """
    existing = get_config()
    for key, val in config.items():
        existing[key] = val
    with open(os.path.expanduser("~/maildown.toml"), "w") as f:
        f.write(toml.dumps(config))
