from psycopg2 import sql

from django.conf import settings

from psycopg2_extension.base_command import PsycopgBaseCommand


class Command(PsycopgBaseCommand):
    help = 'Initialize the database. It is necessary to use role which has permissions to drop & create databases ' \
           'and roles.'

    def handle(self, *args, **options):
        db_object = self._get_db_object(**options)
        db_name = db_object['NAME']
        db_object['NAME'] = 'template1'
        conn = self._create_connection(db_object)

        with conn.cursor() as cursor:
            cursor.execute("SELECT pid, pg_terminate_backend(pid) "
                           "FROM pg_stat_activity "
                           "WHERE pid <> pg_backend_pid() AND datname = %s", [db_name])
            cursor.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(db_name)))
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            for extension in getattr(settings, 'PSYCOPG2_EXTENSIONS', ()):
                cursor.execute(sql.SQL("CREATE EXTENSION IF NOT EXISTS {}".format(extension)))
