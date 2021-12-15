# Django-psycopg2-extension

Library contains django commands which helps to prepare and manage PostgreSQL database.

## Quickstart

Install djjango-psycopg2-extension

```bash
pip install django-psycopg2-extension
```

Add psycopg2_extension to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # Django apps...
    'psycopg2_extension',
]
```

## Commands

### psqlinit

Django command psqlinit create a database defined in django settings. 

You can define specific database settings with standard django ``DATABASE`` settings:

```python
DATABASES = {
    'default': {
        ...
        'EXTENSIONS': ['postgis', 'unaccent'],  # extensions to be installed with psqlinit command
        'SNAPSHOT_FILE': Path('data', 'sql', 'local', 'init_default.sql'), # SQL which will be loaded after database initialization
    },
}
```

Snapshot and extensions are automatically loaded when database is preparing for tests too.

### psqlclean

PostgreSQL database requires often call `VACUUM` and `REINDEX`. The command `psqlclean` performs these operations. 

You can define specific database settings for psqlclean command with standard django ``DATABASE`` settings:

```python
DATABASES = {
    'default': {
        ...
        'VACUUM': {
            'EXCLUDE': ['users_user'],  # list of excluded tables
            'TABLES': ['users_permission'],  # list of tables to vacuum, all tables are selected if the setting is not set
            'TABLES_FULL': ['users_permission'],  # list of tables to vacuum full
            'TABLES_REINDEX': ['users_permission'],  # list of tables to reindex
        }
    },
}
```

### psqlsnapshot

Command which creates SQL dump with ``pg_dump`` script and store it to the database ``'SNAPSHOT_FILE'`` setting.
