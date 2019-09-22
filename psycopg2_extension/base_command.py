import psycopg2
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from environ import Env
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class PsycopgBaseCommand(BaseCommand):
    help = 'Clean database (vacuum full and reindex)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--db-url',
            dest='db_url',
            help='Connection string to Database',
        )

    def _create_connection(self, db_object):
        if db_object['ENGINE'] not in {'django.db.backends.postgresql_psycopg2',
                                       'django.db.backends.postgresql',
                                       'django.contrib.gis.db.backends.postgis'}:
            raise CommandError('The supplied DB object targets unsupported database backend!')

        con = psycopg2.connect(
            "host='{HOST}' dbname='{NAME}' user='{MASTER_USER}' password='{MASTER_PASSWORD}' port='{PORT}'"
            .format(**db_object)
        )

        # CREATE/DROP commands cannot run in transaction ==> turning it off for the connection
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return con

    def _get_db_object(self, **options):
        if options['db_url']:
            db_object = Env.db_url_config(options['db_url'])
        else:
            db_object = settings.DATABASES['default']
        db_object['MASTER_USER'] = db_object['USER']
        db_object['MASTER_PASSWORD'] = db_object['PASSWORD']
        return db_object
