# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonline']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jsonline',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Jsonline\n\n<img alt="PyPI - License" src="https://img.shields.io/github/license/fsadannn/jsonline"> <img alt="PyPI - License" src="https://travis-ci.org/fsadannn/jsonline.svg"> <img alt="Codecov" src="https://img.shields.io/codecov/c/github/fsadannn/jsonline.svg">\n\nJsonline is intend to use to explore and work with json lines files and avoid keep the entire data in memory or constantly read the whole file.This library handle json lines files as it was a read only list, but with `append` too. This library build and index with the position of the being and end of each json in the file. When an element is accessed we use the mentioned index to read only the line with the requested json. This index is efficient handled and store in gzip format with extension `.json.idx`.\n\n## Example\n\n```Python\nfrom jsonline impor jsonLine\n\n# the extension .json is\'t necessary\ndata = jsonLine(\'my_file\')\n\ndata.append({\'test\': 1})\n\n# extend is an efficient way to append several elements\ndata.extend([{\'test\': 1}, {\'another_test\': 2}])\n\nprint(data[1]) # random access\n\nfor i in data:\n    print(i)\n\ndata.close() # close whe finish using data\n\n# also support context manager\nwith jsonLine(\'my_file\') as data:\n    print(data[0])\n```\n',
    'author': 'fsadannn',
    'author_email': 'fsadannn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.0,<4',
}


setup(**setup_kwargs)
