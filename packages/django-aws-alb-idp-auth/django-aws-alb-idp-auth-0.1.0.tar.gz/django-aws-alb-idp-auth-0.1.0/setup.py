# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_aws_alb_idp_auth']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.1.6,<4.0.0', 'PyJWT[crypto]>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'django-aws-alb-idp-auth',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Atsushi Odagiri',
    'author_email': 'aodagx@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
