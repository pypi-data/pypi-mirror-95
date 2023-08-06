# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'foursight_core/checks'}

packages = \
['checks',
 'checks.helpers',
 'foursight_core',
 'foursight_core.checks',
 'foursight_core.checks.helpers',
 'helpers']

package_data = \
{'': ['*'], 'foursight_core': ['templates/*']}

install_requires = \
['Jinja2==2.10.1',
 'MarkupSafe==1.1.1',
 'PyJWT==1.5.3',
 'click>=7.1.2,<8.0.0',
 'dcicutils>=1.7.0,<2.0.0',
 'elasticsearch-dsl>=6.4.0,<7.0.0',
 'elasticsearch>=6.8.1,<7.0.0',
 'fuzzywuzzy==0.17.0',
 'geocoder==1.38.1',
 'gitpython>=3.1.2,<4.0.0',
 'google-api-python-client==1.7.4',
 'python-Levenshtein==0.12.0',
 'pytz>=2020.1,<2021.0']

setup_kwargs = {
    'name': 'foursight-core',
    'version': '0.1.8',
    'description': 'Serverless Chalice Application for Monitoring',
    'long_description': None,
    'author': '4DN-DCIC Team',
    'author_email': 'support@4dnucleome.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.7',
}


setup(**setup_kwargs)
