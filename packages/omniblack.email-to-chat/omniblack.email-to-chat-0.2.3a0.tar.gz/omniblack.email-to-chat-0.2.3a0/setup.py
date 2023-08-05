# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['email_to_chat']

package_data = \
{'': ['*']}

install_requires = \
['aiosmtpd>=1.2.4,<2.0.0', 'omniblack.logging>=0.2.1,<0.3.0']

extras_require = \
{'discord': ['discord.py>=1.6.0,<2.0.0'],
 'systemd': ['omniblack.systemd>=0.1.2,<0.2.0']}

entry_points = \
{'console_scripts': ['email_to_chat = omniblack.email_to_chat:run_email']}

setup_kwargs = {
    'name': 'omniblack.email-to-chat',
    'version': '0.2.3a0',
    'description': 'An smtp server that forwards messages to chat services.',
    'long_description': None,
    'author': 'Terry Patterson',
    'author_email': 'Terryp@wegrok.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
