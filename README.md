# Django-psycopg2-extension

Library contains django commands which helps prepare and manage PostgreSQL database.

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

### initdb

Django command initdb create a database defined in django settings. If postgres user is not allowed to create database you can define it via `--db-url` parameter (format from [django-environ](https://github.com/joke2k/django-environ)) 

If you are using some Postgres extenstions you can define it with `PSYCOPG2_EXTENSIONS` setting (list of extension names). Command will automatically create it.

### cleandb

PostgreSQL database requires often call `VACUUM FULL` and `REINDEX`. The command `cleandb` performs these operations. Again you can specify database or root user with `--db-url` parameter.
