from django.conf import settings

from django.db.backends.postgresql.creation import DatabaseCreation

from psycopg2_extension.utils import init_database


def _patch_execute_create_test_db(self, cursor, parameters, keepdb=False):
    if keepdb and self._database_exists(cursor, parameters['dbname']):
        return

    self.log(f'Init test database with alias {self.connection.settings_dict["NAME"]}')
    self._tmp_execute_create_test_db(cursor, parameters, keepdb)

    if not parameters['suffix']:
        origin_name = self.connection.settings_dict['NAME']
        self.set_as_test_mirror({'NAME': parameters['dbname'][1:-1]})
        init_database(self.connection, self.log)
        self.set_as_test_mirror({'NAME': origin_name})


DatabaseCreation._tmp_execute_create_test_db = DatabaseCreation._execute_create_test_db
DatabaseCreation._execute_create_test_db = _patch_execute_create_test_db
