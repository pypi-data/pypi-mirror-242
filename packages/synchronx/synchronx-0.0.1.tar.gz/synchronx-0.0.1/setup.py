# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['synchronx']

package_data = \
{'': ['*']}

install_requires = \
['swarms', 'termcolor', 'toml']

setup_kwargs = {
    'name': 'synchronx',
    'version': '0.0.1',
    'description': 'synchro - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Synchro\n\n\n# License\nMIT\n\n\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/synchro',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
