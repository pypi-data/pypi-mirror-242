"""Implementation of the Kedro Expectations Hooks."""
import great_expectations as ge
import os
from typing import Any, Dict, cast, Callable
from kedro.framework.hooks import hook_impl
from kedro.io import DataCatalog, PartitionedDataSet

from kedro_expectations.exceptions import SuiteValidationFailure
from pandas import DataFrame as PandasDataFrame
from kedro_expectations.utils import (
    dot_to_underscore,
    validate,
    get_suite_name,
    get_all_expectations,
    base_ge_folder_exists,
    location_is_kedro_root_folder,
)


class KedroExpectationsHooks:
    """Implementation of the Kedro Expectations Hooks."""

    def __init__(self, fail_fast: bool = False,
                 check_orphan_expectation_suites: bool = True) -> None:
        self._fail_fast = fail_fast
        self._check_orphan_expectation_suites = check_orphan_expectation_suites

    @hook_impl
    def after_catalog_created(
        self,
        catalog,
    ) -> None:
        """Make sure each expectation suite"""
        if self._check_orphan_expectation_suites:
            gx = ge.get_context()
            exp_datasets = set(
                entry.expectation_suite_name.split(".")[0]
                for entry in gx.list_expectation_suites()
            )
            catalog_datasets = set(
                entry
                for entry in catalog.list()
                if not entry.startswith("params:") and entry != "parameters"
            )
            orphan_expectation_suites = exp_datasets - catalog_datasets
            if len(orphan_expectation_suites) > 0:
                if self._fail_fast:
                    raise SuiteValidationFailure(f'Found orphan expectation suites not corresponding to any dataset in'
                                                 f'the catalog: {orphan_expectation_suites}.')
                else:
                    print(f'Found orphan expectation suites not corresponding to any dataset in'
                          f'the catalog: {orphan_expectation_suites}.')

    @hook_impl
    def before_node_run(self, catalog: DataCatalog, inputs: Dict[str, Any]) -> None:
        """Validate inputs that are supported and have an expectation suite available."""
        if (
            self.before_node_run
            and base_ge_folder_exists(verbose=False)
            and location_is_kedro_root_folder()
        ):
            self._run_validation(catalog, inputs)

    def _run_validation(self, catalog: DataCatalog, data: Dict[str, Any]) -> None:
        for key, value in data.items():

            if isinstance(getattr(catalog.datasets, key), PartitionedDataSet):
                partitions = cast(Dict[str, Callable], value)

                for casted_key, casted_value in partitions.items():

                    # Looking for an specific expectation
                    adjusted_key_pt1 = dot_to_underscore(key)
                    adjusted_key_pt2 = dot_to_underscore(casted_key)

                    adjusted_key = os.path.join(adjusted_key_pt1, adjusted_key_pt2)
                    all_expectations = get_all_expectations(adjusted_key)

                    ge_adjusted_key = adjusted_key_pt1 + "." + adjusted_key_pt2

                    # Looking for a general expectation
                    if not all_expectations:
                        adjusted_key = dot_to_underscore(key)
                        all_expectations = get_all_expectations(adjusted_key)
                        ge_adjusted_key = adjusted_key

                    for exp_file in all_expectations:
                        suite_name = get_suite_name(exp_file, ge_adjusted_key)
                        result = validate(casted_key, suite_name, casted_value())

                        if self._fail_fast and not result.success:
                            raise SuiteValidationFailure(
                                f"Suite {suite_name} for DataSet {adjusted_key} failed!"
                            )
                    if not all_expectations:
                        print(
                            f'No expectation suite was found for "{key}".',
                            "Validation will be skipped!",
                        )
            else:
                adjusted_key = dot_to_underscore(key)
                all_expectations = get_all_expectations(adjusted_key)
                for exp_file in all_expectations:
                    suite_name = get_suite_name(exp_file, adjusted_key)

                    if isinstance(value, PandasDataFrame):
                        result = validate(adjusted_key, suite_name, value)
                    else:
                        print(
                            f"Dataset {adjusted_key} is not supported by Kedro Expectations"
                        )

                    if self._fail_fast and not result.success:
                        raise SuiteValidationFailure(
                            f"Suite {suite_name} for DataSet {adjusted_key} failed!"
                        )
                if not all_expectations:
                    print(
                        f'No expectation suite was found for "{key}".',
                        "Validation will be skipped!",
                    )
