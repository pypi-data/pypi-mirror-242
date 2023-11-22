import importlib
from inspect import isclass
from pathlib import Path
from typing import Any, Dict, Optional, TextIO, Type

import yaml
from dbt.contracts.connection import Credentials
from dbt.version import _get_adapter_plugin_names  # type: ignore
from mashumaro.jsonschema.models import Context, JSONSchema
from mashumaro.jsonschema.schema import Instance, Registry, get_schema
from ruamel.yaml import YAML


def on_new_type(instance: Instance, ctx: Context) -> Optional[JSONSchema]:
    # The 'Port' in PostgresCredentials is a NewType(int) and for some reason
    # that does not work, however if it was just an 'int' it would correctly include
    # the minimum and maximum constraints
    #
    # This forces the NewTypes of ints to call the base on number
    super_type = getattr(instance.origin_type, "__supertype__", None)

    if super_type is None:
        return

    instance.type = super_type
    instance.origin_type = super_type

    return get_schema(instance, Context())


# needs to come first: (using the decorator will put last)
Registry._registry = [on_new_type, *Registry._registry]


def get_adapter_credentials() -> Dict[str, Type[Credentials]]:
    output: Dict[str, Type[Credentials]] = {}

    for adapter_name in _get_adapter_plugin_names():
        adapter_module = importlib.import_module(f"dbt.adapters.{adapter_name}")

        for obj_name in dir(adapter_module):
            adapter = getattr(adapter_module, obj_name)

            if (
                isclass(adapter)
                and issubclass(adapter, Credentials)
                and adapter != Credentials
            ):
                output[adapter_name] = adapter

    return output


class DbtProjectNotFoundError(Exception):
    ...


class DbtProfileNotFoundError(Exception):
    ...


def load_dbt_project(project_path: Path) -> Dict[str, Any]:
    file_path = project_path / "dbt_project.yml"

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    except FileNotFoundError as error:
        raise DbtProjectNotFoundError(
            f"Could not find DBT Project at {file_path}"
        ) from error


class DbtProfileYAML:
    def __init__(self, profile_name: str, profiles_path: Path):
        self._profile_name = profile_name
        self._profiles_path = profiles_path

        self._setup_yaml()
        self._read_file()

    def _setup_yaml(self):
        profiles_yaml = YAML()
        profiles_yaml.explicit_start = True
        profiles_yaml.indent(mapping=3)
        profiles_yaml.preserve_quotes = True
        self._profiles_yaml = profiles_yaml

    def _read_file(self):
        try:
            with open(
                self._profiles_path / "profiles.yml", "r", encoding="utf-8"
            ) as file:
                self._profiles = self._profiles_yaml.load(file)
        except FileNotFoundError as error:
            raise DbtProfileNotFoundError(
                f"Could not file profiles.yml at {self._profiles_path}"
            ) from error

    @property
    def file_path(self):
        return self._profiles_path

    @property
    def profile_name(self):
        return self._profile_name

    @property
    def selected_profile(self):
        return self._profiles[self._profile_name]

    @property
    def outputs(self):
        return self.selected_profile["outputs"]

    @property
    def target_name(self):
        return self.selected_profile["target"]

    @property
    def target(self):
        return self.outputs[self.target_name]

    def write(self, new_profile_data: Dict[str, Any], file: TextIO):
        self._profiles_yaml.dump(new_profile_data, file)


def write_dbt_profile(
    profiles_yaml: DbtProfileYAML,
    inputs: Dict[str, Any],
    adapter_type_name: str,
) -> None:
    profiles_yaml._profiles[profiles_yaml.profile_name]["outputs"][
        profiles_yaml.target_name
    ] = {
        "type": adapter_type_name,
        **profiles_yaml.target,
        **inputs,
    }

    with open(profiles_yaml.file_path / "profiles.yml", "w", encoding="utf-8") as file:
        profiles_yaml.write(profiles_yaml._profiles, file)
