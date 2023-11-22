# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src\\main\\python'}

packages = \
['fameprotobuf']

package_data = \
{'': ['*']}

install_requires = \
['protobuf>=4.21.1,<5.0.0']

setup_kwargs = {
    'name': 'fameprotobuf',
    'version': '1.3.0',
    'description': 'Protobuf definitions converted to python classes for use in `fameio`',
    'long_description': '[![PyPI version](https://badge.fury.io/py/fameprotobuf.svg)](https://badge.fury.io/py/fameprotobuf)\n[![PyPI license](https://img.shields.io/pypi/l/fameprotobuf.svg)](https://badge.fury.io/py/fameprotobuf) \n\n# FAME-Protobuf\nGoogle Protocol Buffer (protobuf) definitions define the structure of binary input and output files for FAME applications.\nPlease visit the [Wiki for FAME](https://gitlab.com/fame-framework/wiki/-/wikis/home) to get an explanation of FAME and its components.\n\nFAME-Protobuf connects FAME-Io to applications based on FAME-Core. Thus, both depend on FAME-Protobuf.\n\n## Repository\nThe repository is split into three source code parts:\n* protobuf definitions reside in `src/main/resources`,\n* derived Python classes for FAME-Io reside in `src/main/python`.\n* derived Java classes for FAME-Core reside in `target/generated-java-sources`, and\n\n## Installation instructions\nUse this Maven dependency:\n```\n<dependency>\n  <groupId>de.dlr.gitlab.fame</groupId>\n  <artifactId>protobuf</artifactId>\n  <version>1.3.0</version>\n</dependency>\n```\n\n## Packaging\n### Compile\nThe `pom.xml` is configured to allow automated compilation of the protobuf definitions to Python and Java classes.\n\n### Maven build\nIn the cloned repository of fame-protobuf, compile and package fame-protobuf locally to your Maven repository: \n\n```\nmvn package\n```\n\n### Deploy to PyPI\nFAME-Protobuf is packaged to PyPI.\nWe use [poetry](https://python-poetry.org) for packaging.\nPackaging requires these steps:\n* install poetry: `pip install poetry`\n* run the packaging script: `python packaging.py`\n* build wheel: `poetry build` \n* publish: `poetry publish`\n\n# Contribute\nPlease read the Contributors License Agreement (cla.md), sign it and send it to fame@dlr.de before contributing.\n',
    'author': 'Christoph Schimeczek',
    'author_email': 'fame@dlr.de',
    'maintainer': 'Christoph Schimeczek',
    'maintainer_email': 'fame@dlr.de',
    'url': 'https://gitlab.com/fame-framework/wiki/-/wikis/home',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
