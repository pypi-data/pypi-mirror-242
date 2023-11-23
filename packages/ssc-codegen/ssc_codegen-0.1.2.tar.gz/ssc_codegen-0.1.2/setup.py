# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ssc_codegen',
 'ssc_codegen.configs',
 'ssc_codegen.configs.dart',
 'ssc_codegen.configs.python']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0', 'PyYAML>=6.0.1,<7.0.0', 'cssselect>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['ssc-gen = ssc_codegen.cli:main']}

setup_kwargs = {
    'name': 'ssc-codegen',
    'version': '0.1.2',
    'description': 'generate selector schemas classes from yaml config and DSL-lang script',
    'long_description': None,
    'author': 'georgiy',
    'author_email': '59173419+vypivshiy@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
