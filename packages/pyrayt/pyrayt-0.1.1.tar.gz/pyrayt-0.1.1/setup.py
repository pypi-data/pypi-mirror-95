# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrayt', 'pyrayt.components', 'pyrayt.shaders']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.0,<2.0.0', 'pandas>=1.2.2,<2.0.0', 'scipy>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'pyrayt',
    'version': '0.1.1',
    'description': 'a toolchain for developing and simulating optical packages',
    'long_description': None,
    'author': 'Frazier, Ryan',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.5,<4.0.0',
}


setup(**setup_kwargs)
