# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['meraki_exception']

package_data = \
{'': ['*']}

install_requires = \
['meraki>=1.4.3,<2.0.0', 'rich>=9.10.0,<10.0.0']

setup_kwargs = {
    'name': 'meraki-exception',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Thomas Christory',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
