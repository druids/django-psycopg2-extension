import subprocess

from django.core.management.base import CommandError

from django.core.exceptions import FieldDoesNotExist
from psycopg2_extension.base_command import PsycopgBaseCommand
from django.apps import apps


class Command(PsycopgBaseCommand):

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--noinput",
            "--no-input",
            action="store_false",
            dest="interactive",
            help="Tells Django to NOT prompt the user for input of any kind.",
        )
        parser.add_argument(
            "--create",
            action="store_const",
            dest="action",
            const="create",
            help="Create database views",
        )
        parser.add_argument(
            "--delete",
            action="store_const",
            dest="action",
            const="delete",
            help="Delete database views",
        )

    def _create(self, connection, models_config, schema):
        with connection.cursor() as cursor:
            for model_name, allowed_fields in models_config.items():
                print(model_name)
                try:
                    model = apps.get_model(model_name)
                except LookupError:
                    raise CommandError(f"Model {model_name} not found")

                table_name = model._meta.db_table
                view_name = f"{schema}.view_{table_name}"

                self.stdout.write(
                    f"Creating view for {model_name} with name {view_name}"
                )

                db_view_columns = []
                for allowed_field in allowed_fields:
                    try:
                        field = model._meta.get_field(allowed_field)
                        db_view_column = field.get_attname_column()[0]
                        if not db_view_column:
                            raise CommandError(
                                f"Field {allowed_field} is not shored in table {table_name} for model {model_name}"
                            )
                        db_view_columns.append(db_view_column)
                    except FieldDoesNotExist:
                        raise CommandError(
                            f"Field {allowed_field} not found in model {model_name}"
                        )

                cursor.execute(
                    f"CREATE OR REPLACE VIEW {view_name} AS (SELECT {', '.join(db_view_columns)} FROM {table_name})"
                )

    def _delete(self, connection, models_config, schema):
        with connection.cursor() as cursor:
            for model_name, allowed_fields in models_config.items():
                try:
                    model = apps.get_model(model_name)
                except LookupError:
                    raise CommandError(f"Model {model_name} not found")

                table_name = model._meta.db_table
                view_name = (
                    f"{schema}.view_{table_name}" if schema else f"view_{table_name}"
                )

                self.stdout.write(
                    f"Removing view for {model_name} with name {view_name}"
                )

                cursor.execute(f"DROP VIEW IF EXISTS {view_name}")

    def handle(self, *args, **options):
        if not options["action"]:
            raise CommandError(
                "No action specified. Must be one of '--create' or '--delete' ."
            )

        action = options["action"]

        connection = self._get_connection(options["database"])
        models_config = connection.settings_dict.get("VIEWS", {}).get("MODELS", {})
        schema = connection.settings_dict.get("VIEWS", {}).get("SCHEMA")

        if action == "create":
            self._create(connection, models_config, schema)
        elif action == "delete":
            self._delete(connection, models_config, schema)
