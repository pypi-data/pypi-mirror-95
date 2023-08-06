# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
# Copyright (C) 2019 Northwestern University.
#
# Invenio-Records-Permissions is free software; you can redistribute it
# and/or modify it under the terms of the MIT License; see LICENSE file for
# more details.

"""Permission policies for Invenio records."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

sphinx_require = 'Sphinx>=3'

tests_require = [
    'pytest-mock>=1.6.0',
    'pytest-invenio>=1.4.1',
    'invenio-accounts>=1.4.3',
    'invenio-app>=1.3.0',
    sphinx_require,
]

# Should follow inveniosoftware/invenio versions
invenio_search_version = '>=1.4.0,<2.0.0'
invenio_db_version = '>=1.0.5,<2.0.0'

extras_require = {
    'elasticsearch6': [
        f'invenio-search[elasticsearch6]{invenio_search_version}'
    ],
    'elasticsearch7': [
        f'invenio-search[elasticsearch7]{invenio_search_version}'
    ],
    'mysql': [
        f'invenio-db[mysql,versioning]{invenio_db_version}'
    ],
    'postgresql': [
        f'invenio-db[postgresql,versioning]{invenio_db_version}'
    ],
    'sqlite': [
        f'invenio-db[versioning]{invenio_db_version}'
    ],
    'docs': [
        sphinx_require,
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    if name[0] == ':' or name in ('elasticsearch6', 'elasticsearch7',
                                  'mysql', 'postgresql', 'sqlite'):
        continue
    extras_require['all'].extend(reqs)

setup_requires = [
    'Babel>=1.3',
    'pytest-runner>=3.0.0,<5',
]

install_requires = [
    'invenio-access>=1.4.2,<2.0.0',
    'invenio-i18n>=1.2.0',
    'invenio-records>=1.4.0'
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('invenio_records_permissions', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='invenio-records-permissions',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='invenio permissions',
    license='MIT',
    author='CERN',
    author_email='info@inveniosoftware.org',
    url='https://github.com/inveniosoftware/invenio-records-permissions',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'invenio_base.api_apps': [
            'invenio_records_permissions = invenio_records_permissions:InvenioRecordsPermissions',
        ],
        'invenio_base.apps': [
            'invenio_records_permissions = invenio_records_permissions:InvenioRecordsPermissions',
        ],
        'invenio_i18n.translations': [
            'messages = invenio_records_permissions',
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 3 - Alpha',
    ],
)
