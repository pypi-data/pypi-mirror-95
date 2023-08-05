# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['repo_peek']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.6.0,<0.7.0',
 'aiohttp[speedups]>=3.7.3,<4.0.0',
 'ciso8601>=2.1.3,<3.0.0',
 'loguru>=0.5.3,<0.6.0',
 'sh>=1.14.1,<2.0.0',
 'shellingham>=1.4.0,<2.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['repk = repo_peek.cli:app']}

setup_kwargs = {
    'name': 'repo-peek',
    'version': '0.2.0',
    'description': 'A command line tool to peek a remote repo locally.',
    'long_description': '## repo-peek\n\nA command line tool to peek a remote repo locally and view it in your favorite editor. The tool handles cleanup of the repo once you exit your editor. \n\n<a href="https://asciinema.org/a/3EyUeIwGTYxTJFceBbJNLln8t" target="_blank"><img src="https://asciinema.org/a/3EyUeIwGTYxTJFceBbJNLln8t.svg" /></a>\nDefault editor is chosen by looking at the `EDITOR` environment variable, if it is not set, vim is chosen as the default editor.\n\n### install repo-peek\n\n```bash\npip install repo-peek\n```\n\n### usage:\n\nrepo-peek only has only subcommand `peek`, which takes a repo as the argument.\n\n\ncommand usage:\n\n```bash\nghub peek <repo>\n```\n\nexample:\n\n```bash\nghub peek rahulunair/repo-peek\n```\n\n### todo\n\n- enable for gitlab\n\n### more information\n\nThe tool creates 2 files and a directory, a config file `~/.githubkeep.conf`, a log file `~/.githubkeep.log` and a directory `~/.githubkeep`. Github-peek downloads the tar:gz of the repo, extracts it and saves it to `~/.githubkeep`. There is a naive caching mechanism, where the tool deletes all repos after 5 times of using the app.\n\n\n',
    'author': 'unrahul',
    'author_email': 'rahulunair@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
