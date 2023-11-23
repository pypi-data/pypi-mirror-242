# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytoshop', 'pytoshop.user']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=3.0.5,<4.0.0', 'numpy>=1.26.2,<2.0.0']

setup_kwargs = {
    'name': 'pytoshop-layer',
    'version': '0.1.1',
    'description': '',
    'long_description': 'None',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
