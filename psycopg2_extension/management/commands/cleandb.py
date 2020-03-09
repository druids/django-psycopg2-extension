from psycopg2_extension.conf import settings
from psycopg2_extension.base_command import PsycopgBaseCommand


class Command(PsycopgBaseCommand):
    help = 'Clean database (VACUUM and REINDEX)'

    def _run_clean_command(self, connection, cursor, db_query):
        self.stdout.write(4 * ' ' + 'Running "{}"'.format(db_query))
        cursor.execute(db_query)
        for notice in connection.notices:
            for notice_line in notice.split('\n'):
                self.stdout.write(8 * ' ' + notice_line)

        # Stdout of PostgreSQL commands must be cleaned to not print the same more times
        del connection.notices[:]

    def _get_all_tables(self, cursor):
        cursor.execute(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_schema='public' AND table_type = 'BASE TABLE';"
        )
        return [result[0] for result in cursor.fetchall()]

    def handle(self, *args, **options):
        db_object = self._get_db_object(**options)
        connection = self._create_connection(db_object)

        with connection.cursor() as cursor:
            for table_name in self._get_all_tables(cursor):
                if table_name in settings.EXCLUDE_TABLES:
                    continue

                self.stdout.write('Clean table {}'.format(table_name))
                if table_name not in settings.EXCLUDE_VACUUM_TABLES:
                    self._run_clean_command(connection, cursor, 'VACUUM {} {}'.format(
                        (
                            '(FULL, VERBOSE, ANALYZE)' if table_name in settings.FULL_VACUUM_TABLES
                            else '(VERBOSE, ANALYZE)'
                        ),
                        table_name
                    ))
                if table_name not in settings.EXCLUDE_REINDEX_TABLES:
                    self._run_clean_command(connection, cursor, 'REINDEX (VERBOSE) TABLE {}'.format(table_name))
