from django.conf import settings as django_settings


DEFAULTS = {
    'EXCLUDE_TABLES': {},
    'EXCLUDE_VACUUM_TABLES': {},
    'EXCLUDE_REINDEX_TABLES': {},
    'FULL_VACUUM_TABLES': {}
}


class Settings:

    def __getattr__(self, attr):
        if attr not in DEFAULTS:
            raise AttributeError('Invalid setting: "{}"'.format(attr))

        return getattr(django_settings, 'PSYCOPG2_EXTENSION_{}'.format(attr), DEFAULTS[attr])


settings = Settings()
