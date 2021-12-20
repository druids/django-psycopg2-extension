from psycopg2_extension.base_command import PsycopgBaseCommand
from psycopg2_extension.utils import comma_separated_strings


class Command(PsycopgBaseCommand):
    help = 'Clean database (VACUUM and REINDEX)'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--tables',
            dest='tables',
            help='Tables to vaccum separated with ,',
            type=comma_separated_strings
        )
        parser.add_argument(
            '--tables-full',
            dest='tables_full',
            help='Tables to vaccum full separated with ,',
            type=comma_separated_strings
        )
        parser.add_argument(
            '--tables-reindex',
            dest='tables_reindex',
            help='Tables be excluded separated with ,',
            type=comma_separated_strings
        )
        parser.add_argument(
            '--exclude-tables',
            dest='exclude_tables',
            help='Tables to reindex separated with ,',
            type=comma_separated_strings
        )

    def _run_clean_command(self, connection, cursor, db_query):
        self.stdout.write(4 * ' ' + 'Running "{}"'.format(db_query))
        cursor.execute(db_query)
        for notice in connection.connection.notices:
            for notice_line in notice.split('\n'):
                self.stdout.write(8 * ' ' + notice_line)

        # Stdout of PostgreSQL commands must be cleaned to not print the same more times
        del connection.connection.notices[:]

    def _get_all_tables(self, cursor):
        cursor.execute(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_schema='public' AND table_type = 'BASE TABLE';"
        )
        return [result[0] for result in cursor.fetchall()]

    def handle(self, *args, **options):
        connection = self._get_connection(options['database'])

        vacuum_settings_dict = connection.settings_dict.get('VACCUM', {})

        exclude_tables = set(options['exclude_tables'] or vacuum_settings_dict.get('EXCLUDE', ()))
        vacuum_tables = set(options['tables'] or vacuum_settings_dict.get('TABLES', ()))
        tables_full = set(options['tables_full'] or vacuum_settings_dict.get('TABLES_FULL', ()))
        tables_reindex = set(options['tables_reindex'] or vacuum_settings_dict.get('TABLES_REINDEX', ()))

        vacuum_tables |= tables_full
        tables = vacuum_tables | tables_reindex

        with connection.cursor() as cursor:
            for table_name in self._get_all_tables(cursor):
                if table_name in exclude_tables or (tables and table_name not in tables):
                    continue

                self.stdout.write('Clean table {}'.format(table_name))
                if not vacuum_tables or table_name in vacuum_tables:
                    self._run_clean_command(connection, cursor, 'VACUUM {} {}'.format(
                        '(FULL, VERBOSE, ANALYZE)' if table_name in tables_full else '(VERBOSE, ANALYZE)',
                        table_name
                    ))
                if table_name in tables_reindex:
                    self._run_clean_command(connection, cursor, 'REINDEX (VERBOSE) TABLE {}'.format(table_name))
