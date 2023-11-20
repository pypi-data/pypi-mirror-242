# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alr_transformer']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch', 'zetascale']

setup_kwargs = {
    'name': 'alr-transformer',
    'version': '0.0.2',
    'description': 'Paper - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# ALR Transformer\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/ShallowFF',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
