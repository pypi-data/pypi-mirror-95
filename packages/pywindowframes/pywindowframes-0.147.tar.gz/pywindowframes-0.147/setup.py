# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pywindowframes']

package_data = \
{'': ['*'], 'pywindowframes': ['.idea/*', '.idea/inspectionProfiles/*']}

install_requires = \
['pygame>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'pywindowframes',
    'version': '0.147',
    'description': 'Window based GUI for pygame',
    'long_description': None,
    'author': 'afmelin',
    'author_email': '79141108+afmelin@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/afmelin/pywindowframes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
