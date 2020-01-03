from setuptools import setup, find_packages

setup(
    name="django-psycopg2-extension",
    version='0.0.3',
    description="",
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
