from psycopg2_extension.base_command import PsycopgBaseCommand


class Command(PsycopgBaseCommand):
    help = 'Clean database (vacuum full and reindex)'

    def handle(self, *args, **options):
        db_object = self._get_db_object(**options)
        conn = self._create_connection(db_object)

        with conn.cursor() as cursor:
            vacuum_query = 'VACUUM FULL ANALYZE'
            self.stdout.write('Running "{}"'.format(vacuum_query))
            cursor.execute(vacuum_query)
            reindex_query = 'REINDEX DATABASE {}'.format(db_object['NAME'])
            self.stdout.write('Running "{}"'.format(reindex_query))
            cursor.execute(reindex_query)
