import psycopg2
from psycopg2 import sql

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from environ import Env
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


from django.db import connections


def init_database(connection, log, connection_settings=None):
    connection_settings = {} if connection_settings is None else connection_settings

    settings_dict = {
        **connection.settings_dict,
        **connection_settings
    }

    extensions = settings_dict.get('EXTENSIONS')
    snapshot_file = settings_dict.get('SNAPSHOT_FILE')

    if extensions or snapshot_file:
        with connection.cursor() as cursor:
            if extensions:
                log(f'  Init database extensions {extensions}')
                for extension in extensions:
                    cursor.execute(sql.SQL("CREATE EXTENSION IF NOT EXISTS {}".format(extension)))

            if snapshot_file:
                log(f'  Load SQL from file {snapshot_file}')
                with open(snapshot_file, 'r') as sql_file:
                    cursor.execute(sql_file.read())
    connection.close()


def comma_separated_strings(value):
    return [v.strip() for v in value.split(',')]
