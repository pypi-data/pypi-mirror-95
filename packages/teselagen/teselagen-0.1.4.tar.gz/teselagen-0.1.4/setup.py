# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['teselagen',
 'teselagen.api',
 'teselagen.api.tests',
 'teselagen.examples',
 'teselagen.utils']

package_data = \
{'': ['*'],
 'teselagen.examples': ['pytested/*', 'pytested/.ipynb_checkpoints/*']}

install_requires = \
['dna_features_viewer>=3.0.3,<4.0.0',
 'fastaparser>=1.1,<2.0',
 'pandas>=1.0.0,<2.0.0',
 'pytest-cov>=2.8.1,<3.0.0',
 'pytest-notebook>=0.6.1,<0.7.0',
 'pytest-xdist>=1.31.0,<2.0.0',
 'pytest>=5.3.5,<6.0.0',
 'requests-mock>=1.8,<2.0',
 'requests>=2.22.0,<3.0.0',
 'setuptools>=45.1.0,<46.0.0',
 'single_version>=1.5.1,<2.0.0',
 'tqdm>=4.53.0,<5.0.0']

setup_kwargs = {
    'name': 'teselagen',
    'version': '0.1.4',
    'description': 'Teselagen Biotechnology API client',
    'long_description': '# TeselaGen Python Tools.\n\nThis package includes some Python tools to use in combination with TeselaGen platform.\nThese tools includes _TeselaGen Python API Client_ \n\nThis package runs on Python 3.6 and above.\n\n**NOTE :** All the following commands are supposed to be run on the `base` directory, unless specified.\n\n## Library Installation\nThis library contains the TeselaGen Python API Client.\n\nTo install it locally,\n\n1. By using PIP\n\n    Use `pip install teselagen`\n\n\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TeselaGen/api-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
