from psycopg2 import sql

from django.core.management.base import CommandError
from django.db import connections

from psycopg2_extension.base_command import PsycopgBaseCommand
from psycopg2_extension.utils import init_database, comma_separated_strings


class Command(PsycopgBaseCommand):
    help = 'Initialize the database. It is necessary to use role which has permissions to drop & create databases ' \
           'and roles.'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--snapshot-file',
            dest='snapshot_file',
            help='Snapshot file path'
        )
        parser.add_argument(
            '--extensions',
            dest='extensions',
            help='Database extensions separated with ,',
            type=comma_separated_strings
        )
        parser.add_argument(
            '--noinput', '--no-input', action='store_false', dest='interactive',
            help='Tells Django to NOT prompt the user for input of any kind.',
        )
        parser.add_argument(
            '--nosnapshot', action='store_true', dest='no_snapshot',
            help='Do not load snapshot.',
        )

    def handle(self, *args, **options):
        connection = self._get_connection(options['database'])

        if options['interactive']:
            message = (
                'This will delete existing database!\n'
                'Are you sure you want to do this?\n\n'
                "Type 'yes' to continue, or 'no' to cancel: "
            )
            if input(message) != 'yes':
                raise CommandError('Init SQL database cancelled.')

        db_name = connection.settings_dict['NAME']
        self.stdout.write(f'Init database {db_name}')
        with connection._nodb_cursor() as cursor:
            cursor.execute("SELECT pid, pg_terminate_backend(pid) "
                           "FROM pg_stat_activity "
                           "WHERE pid <> pg_backend_pid() AND datname = %s", [db_name])
            cursor.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(db_name)))
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        connection.close()

        connection_settings = {}
        if options['no_snapshot'] or options['snapshot_file']:
            connection_settings['SNAPSHOT_FILE'] = None if options['no_snapshot'] else options['snapshot_file']
        if options['extensions']:
            connection_settings['EXTENSIONS'] = options['extensions']

        init_database(connection, self.stdout.write, connection_settings)
