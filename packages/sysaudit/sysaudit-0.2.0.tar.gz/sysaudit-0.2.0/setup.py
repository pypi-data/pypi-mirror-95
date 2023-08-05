# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sysaudit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sysaudit',
    'version': '0.2.0',
    'description': 'Backport module for sys.audit and sys.addaudithook from Python 3.8',
    'long_description': 'sysaudit\n========\n\nBackport module of [sys.audit](https://docs.python.org/3.8/library/sys.html#sys.audit)\nand [sys.addaudithook](https://docs.python.org/3.8/library/sys.html#sys.addaudithook)\nfrom Python 3.8.\n\n**Note:** This module does _not_ backport any of the built-in\n[audit events](https://docs.python.org/3.8/library/audit_events.html#audit-events).\n\n\n## Installation\n\n```\npip install sysaudit\n```\n\n## Usage\n\n`sysaudit` can be used as a drop-in replacement for `sys.audit` and `sys.addaudithook`.\n\n``` python\nimport sysaudit\n\ndef hook(event, args):\n    print("Event:", event, args)\n    \nsysaudit.addaudithook(hook)\n\nsysaudit.audit("event_name", 1, 2, dict(key="value"))\n# Event: event_name (1, 2, {\'key\': \'value\'})\n```\n',
    'author': 'brettlangdon',
    'author_email': 'me@brett.is',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/brettlangdon/sysaudit',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
