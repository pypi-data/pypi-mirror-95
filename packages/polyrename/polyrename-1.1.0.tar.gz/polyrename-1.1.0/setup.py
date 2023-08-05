# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polyrename',
 'polyrename.driver',
 'polyrename.driver.dev',
 'polyrename.driver.gui',
 'polyrename.transformation',
 'polyrename.transformation.utils']

package_data = \
{'': ['*'], 'polyrename.driver.gui': ['icons/*']}

install_requires = \
['PySide2>=5.15.2,<6.0.0', 'mediafile>=0.2.0,<1.0.0']

entry_points = \
{'console_scripts': ['polyrename = polyrename.__main__:main']}

setup_kwargs = {
    'name': 'polyrename',
    'version': '1.1.0',
    'description': 'A cross-platform, bulk-file rename tool',
    'long_description': "[![PyPI](https://img.shields.io/pypi/v/PolyRename)](https://pypi.org/project/PolyRename/)\n[![Documentation Status](https://readthedocs.org/projects/polyrename/badge/?version=latest)](https://polyrename.readthedocs.io/en/latest/?badge=latest)\n\n# PolyRename\nA cross-platform, bulk-file rename tool\n\n## Installation\nPolyRename is available on [PyPI](https://pypi.org/project/PolyRename/) and can be installed via:\n\n    $ pip3 install --user PolyRename\n\n## Documentation\nPolyRename's documentation is hosted on [ReadTheDocs](http://polyrename.readthedocs.io/)\n",
    'author': 'Andrew Simmons',
    'author_email': 'agsimmons0@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/agsimmons/PolyRename',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<3.10',
}


setup(**setup_kwargs)
