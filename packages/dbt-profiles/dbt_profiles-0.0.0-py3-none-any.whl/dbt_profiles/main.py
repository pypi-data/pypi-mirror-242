from pathlib import Path
from typing import Any, Dict, cast

from .dbt_utils import (
    DbtProfileNotFoundError,
    DbtProfileYAML,
    get_adapter_credentials,
    load_dbt_project,
    write_dbt_profile,
)
from .prompt import Prompt


def main(dbt_profiles_dir: Path, dbt_project_dir: Path, required_fields_only: bool):
    dbt_project = load_dbt_project(dbt_project_dir)

    selected_profile = dbt_project.get("profile", None)
    if selected_profile is None:
        # todo: if you have profiles in profiles.yml then add to the dbt project
        # otherwise prompt for profile name (already doing down below)
        raise Exception("Could not find 'profile' in dbt_project.yml.")

    try:
        dbt_profiles = DbtProfileYAML(selected_profile, dbt_profiles_dir)
    except DbtProfileNotFoundError as error:
        # todo create profiles.yml
        raise error

    adapter = get_adapter_credentials()

    if len(adapter) == 0:
        raise Exception("No adapters found, install a dbt package")
    elif len(adapter) > 1:
        # todo: prompt to selected adapter
        raise Exception("multiple adapters found")
    else:
        adapter_type_name = list(adapter.keys())[0]
        schema = cast(
            Dict[str, Any],
            adapter[adapter_type_name].json_schema(),
        )

    profile_names = list(dbt_profiles.outputs.keys())

    if len(profile_names) == 0:
        # todo: prompt to create ($selected_profile)
        already_have_profile_fields = []
        raise Exception("no profiles found")
    elif dbt_profiles.target_name not in profile_names:
        # todo: prompt to create $selected_profile and update dbt_project
        raise Exception("invalid target selected")
    else:
        already_have_profile_fields = [
            f for f in dbt_profiles.target.keys() if f != "type"
        ]

    prompt_factory = Prompt(schema)

    if required_fields_only:
        required_fields = prompt_factory.json_schema.required
    else:
        required_fields = prompt_factory.json_schema.properties

    profile_fields_to_prompt = [
        required
        for required in required_fields
        if required not in already_have_profile_fields
    ]

    p = prompt_factory.questions_for_fields(profile_fields_to_prompt)
    inputs = p()

    write_dbt_profile(
        dbt_profiles,
        inputs,
        adapter_type_name,
    )
