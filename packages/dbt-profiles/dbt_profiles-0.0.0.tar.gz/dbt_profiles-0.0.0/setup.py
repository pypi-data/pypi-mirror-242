# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbt_profiles']

package_data = \
{'': ['*']}

install_requires = \
['dbt-core>=1.6.1',
 'importlib>=1.0.4,<2.0.0',
 'mashumaro>=3.10,<4.0',
 'prompt-toolkit==3.0.41',
 'ruamel-yaml>=0.18.5,<0.19.0']

entry_points = \
{'console_scripts': ['dbt-profiles-setup = dbt_profiles_setup.cli:cli_main']}

setup_kwargs = {
    'name': 'dbt-profiles',
    'version': '0.0.0',
    'description': '',
    'long_description': '',
    'author': 'Alex Rudolph',
    'author_email': 'alex3rudolph@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '==3.8.18',
}


setup(**setup_kwargs)
