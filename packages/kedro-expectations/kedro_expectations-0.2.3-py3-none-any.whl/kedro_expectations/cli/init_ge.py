"""Defines all functions related to Great Expectations Datasources."""
import click
import os
import yaml
import great_expectations as ge
from kedro_expectations.utils import base_ge_folder_does_NOT_exist, location_is_kedro_root_folder
from ..constants import _DEFAULT_PANDAS_DATASOURCE_NAME
from subprocess import Popen, DEVNULL


@click.command()
def init() -> None:
    if location_is_kedro_root_folder() and base_ge_folder_does_NOT_exist():
        init_ge_and_create_datasources()


def init_ge_and_create_datasources() -> None:
    try:
        print("Creating base great_expectations folder...")
        env = dict(os.environ)
        Popen(
            "echo Y | great_expectations init",
            shell=True,
            stdout=DEVNULL,
            env=env
        ).wait()
        print("great_expectations folder successfully created!")

        print("Generating Kedro Expectations Datasource...")

        context = ge.get_context()
        context.sources.add_pandas(name=_DEFAULT_PANDAS_DATASOURCE_NAME)

        print("Kedro Expectations successfully generated!")

    except yaml.YAMLError as exc:
        print("Error while parsing YAML:\n", exc)
