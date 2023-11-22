import argparse
import os
from pathlib import Path

from .main import main

parser = argparse.ArgumentParser(
    prog="dbt_profiles_setup",
    description="CLI to setup your dbt profile",
)
parser.add_argument("-p", "--project-path", default=".", required=False)
parser.add_argument("-r", "--required-only", action="store_true")
# parser.add_argument("-r", "--required-only", action=argparse.BooleanOptionalAction)


def cli_main():
    args = parser.parse_args()

    dbt_project_dir = args.project_path
    required_only = args.required_only

    # dbt_project_dir = r.check_str("--project-path", args.project_path)
    # required_only = r.check_bool("--required-only", args.required_only)

    dbt_profiles_dir = os.environ.get("DBT_PROFILES_DIR")
    # todo: check ~/.dbt/
    if dbt_profiles_dir is None:
        # todo: prompt instead
        raise Exception("Need to set the environment variable 'DBT_PROFILES_DIR'")

    main(
        Path(os.path.abspath(dbt_profiles_dir)),
        Path(os.path.abspath(dbt_project_dir)),
        required_only,
    )
