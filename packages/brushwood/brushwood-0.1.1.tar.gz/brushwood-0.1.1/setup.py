# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brushwood', 'brushwood.filter']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'brushwood',
    'version': '0.1.1',
    'description': 'Interleaved object structures to filterable and iteratable tree structure',
    'long_description': None,
    'author': '138',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
