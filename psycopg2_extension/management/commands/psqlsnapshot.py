import subprocess

from django.core.management.base import CommandError

from psycopg2_extension.base_command import PsycopgBaseCommand


class Command(PsycopgBaseCommand):

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--file',
            dest='file',
            help='Snapshot file path'
        )
        parser.add_argument(
            '--noinput', '--no-input', action='store_false', dest='interactive',
            help='Tells Django to NOT prompt the user for input of any kind.',
        )
        parser.add_argument(
            '--stdout', action='store_true', dest='write_to_stdout', help='Write snapshot to stdout',
        )

    def handle(self, *args, **options):
        connection = self._get_connection(options['database'])

        command = [
            'pg_dump', 'postgres://{}:{}@{}:{}/{}'.format(
                connection.settings_dict['USER'],
                connection.settings_dict['PASSWORD'],
                connection.settings_dict['HOST'],
                connection.settings_dict['PORT'],
                connection.settings_dict['NAME'],
            ), '--inserts'
        ]

        if options['write_to_stdout']:
            self.stdout.write(subprocess.check_output(command).decode('utf-8'))
        else:
            file_path = options.get('file') or connection.settings_dict.get('SNAPSHOT_FILE')

            if options['interactive']:
                message = (
                    f"This will overwrite existing file '{file_path}'!\n"
                    'Are you sure you want to do this?\n\n'
                    "Type 'yes' to continue, or 'no' to cancel: "
                )
                if input(message) != 'yes':
                    raise CommandError("SQL snapshot cancelled.")

            if not file_path:
                raise CommandError('You must set snapshot file')

            self.stdout.write(f'Take a snapshot of database "{options["database"]}" to "{file_path}"')
            with open(file_path, 'w') as file:
                subprocess.call(command, stdout=file)
