from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connections


class PsycopgBaseCommand(BaseCommand):
    help = 'Clean database (vacuum full and reindex)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--database',
            dest='database',
            help='Database name in django settings',
            default='default'
        )

    def _get_connection(self, alias):
        connection = connections[alias]
        if connection.settings_dict['ENGINE'] not in {'django.db.backends.postgresql',
                                                      'django.contrib.gis.db.backends.postgis'}:
            raise CommandError('Unsupported database backend!')
        return connection
