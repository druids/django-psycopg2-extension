import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="django-psycopg2-extension",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    version='0.0.4',
    description="Library contains django commands which helps to prepare and manage PostgreSQL database.",
    author='Lubos Matl',
    author_email='matllubos@gmail.com',
    url='https://github.com/druids/django-psycopg2-extension',
    license='MIT',
    package_dir={'psycopg2_extension': 'psycopg2_extension'},
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    install_requires=[
        'django>=1.11',
        'django-environ>=0.4.5',
    ],
    zip_safe=False
)
