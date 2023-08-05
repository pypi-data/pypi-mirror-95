import argparse
from argparse import Namespace
from typing import Optional

from google.api_core.exceptions import NotFound
from google.cloud.bigquery.table import Table

from bq_schema.cli.bigquery_connection import create_connection
from bq_schema.migration.schema_diff import check_schemas
from bq_schema.migration.table_finder import find_tables


def parse_args() -> Namespace:
    parser = argparse.ArgumentParser(
        description="Manage your bigquery table migrations."
    )
    parser.add_argument("--project", required=False, help="Target bigquery project.")
    parser.add_argument("--dataset", required=False, help="Target bigquery dataset")
    parser.add_argument(
        "--module-path", required=True, help="Module path to your bigquery models."
    )

    parser.add_argument(
        "--apply",
        default=False,
        action="store_true",
        help="If set to true, this script will apply all open migrations.",
    )

    parser.add_argument(
        "--validate",
        default=False,
        action="store_true",
        help="If set to true, this script will fail if a difference in schemas is found. Useful for CI.",
    )

    return parser.parse_args()


def main(
    project: Optional[str],
    dataset: Optional[str],
    module_path: str,
    apply: bool,
    validate: bool,
) -> None:
    client = create_connection()
    global_project = project
    global_dataset = dataset
    for local_table in set(find_tables(module_path)):
        project = global_project or local_table.project
        assert project, "Project has not been set."
        dataset = global_dataset or local_table.dataset
        assert dataset, "Dataset has not been set."

        table_identifier = f"{project}.{dataset}.{local_table.full_table_name()}"
        print(f"Checking migrations for: {table_identifier}")

        try:
            remote_table = client.get_table(table_identifier)
        except NotFound as not_found:
            table_exists_msg = f"Table does not exist in bq: {table_identifier}"
            if validate:
                raise Exception(table_exists_msg) from not_found

            print(table_exists_msg)
            if apply:
                print("Creating table.")
                table = Table(
                    table_identifier,
                    schema=local_table.get_schema_fields(),
                )
                if local_table.time_partitioning:
                    table.time_partitioning = local_table.time_partitioning
                print(client.create_table(table))
        else:
            schemas_diff = list(
                check_schemas(local_table.get_schema_fields(), remote_table.schema)
            )
            if schemas_diff:
                schemas_diff_msg = f"Schemas diff: {schemas_diff}"
                if validate:
                    raise Exception(schemas_diff_msg)
                print(schemas_diff_msg)
                if apply:
                    print("Applying changes")
                    remote_table.schema = local_table.get_schema_fields()
                    print(client.update_table(remote_table, ["schema"]))


def cli() -> None:
    args = parse_args()
    main(args.project, args.dataset, args.module_path, args.apply, args.validate)


if __name__ == "__main__":
    cli()
