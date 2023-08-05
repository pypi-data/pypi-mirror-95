# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cltk',
 'cltk.alphabet',
 'cltk.alphabet.grc',
 'cltk.core',
 'cltk.data',
 'cltk.dependency',
 'cltk.embeddings',
 'cltk.languages',
 'cltk.lemmatize',
 'cltk.morphology',
 'cltk.ner',
 'cltk.phonology',
 'cltk.phonology.ang',
 'cltk.phonology.arb',
 'cltk.phonology.arb.utils',
 'cltk.phonology.arb.utils.pyarabic',
 'cltk.phonology.enm',
 'cltk.phonology.gmh',
 'cltk.phonology.got',
 'cltk.phonology.grc',
 'cltk.phonology.lat',
 'cltk.phonology.non',
 'cltk.phonology.non.old_swedish',
 'cltk.prosody',
 'cltk.prosody.lat',
 'cltk.readers',
 'cltk.sentence',
 'cltk.stem',
 'cltk.stops',
 'cltk.tag',
 'cltk.text',
 'cltk.tokenizers',
 'cltk.tokenizers.lat',
 'cltk.utils',
 'cltk.wordnet']

package_data = \
{'': ['*']}

install_requires = \
['boltons>=20.0.0,<21.0.0',
 'fasttext>=0.9.1,<0.10.0',
 'gensim>=3.8.1,<4.0.0',
 'gitpython>=3.0,<4.0',
 'greek-accentuation>=1.2.0,<2.0.0',
 'nltk>=3.5,<4.0',
 'python-Levenshtein>=0.12.0,<0.13.0',
 'requests>=2.22.0,<3.0.0',
 'spacy>=2.3.5,<3.0.0',
 'stanza>=1.0.0,<2.0.0',
 'stringcase>=1.2,<2.0',
 'tqdm>=4.41.1,<5.0.0']

setup_kwargs = {
    'name': 'cltk',
    'version': '1.0.0b4',
    'description': 'The Classical Language Toolkit',
    'long_description': "**Notice**: This Git branch (``dev``) contains the CLTK's upcoming major release (v. 1.0.0). See `<https://github.com/cltk/cltk/tree/master>`_ and `<https://docs.cltk.org/>`_ for the legacy code and docs.\n\n\n|travis| |rtd| |codecov| |pypi| |zenodo| |binder|\n\n\n.. |travis| image:: https://travis-ci.org/cltk/cltk.svg?branch=dev\n   :target: https://travis-ci.org/cltk/cltk\n\n.. |rtd| image:: https://img.shields.io/readthedocs/cltk\n   :target: http://dev.cltk.org/\n\n.. |codecov| image:: https://codecov.io/gh/cltk/cltk/branch/dev/graph/badge.svg\n   :target: https://codecov.io/gh/cltk/cltk\n\n.. |pypi| image:: https://img.shields.io/pypi/v/cltk\n   :target: https://pypi.org/project/cltk/\n\n.. |zenodo| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3445585.svg\n   :target: https://doi.org/10.5281/zenodo.3445585\n\n.. |binder| image:: https://mybinder.org/badge_logo.svg\n   :target: https://mybinder.org/v2/gh/cltk/tutorials/dev\n\n\nThe Classical Language Toolkit (CLTK) is a Python library offering natural language processing (NLP) for the languages of pre–modern Eurasia.\n\n\nInstallation\n============\n\nFor the CLTK's latest pre-release version:\n\n.. code-block:: bash\n\n   $ pip install --pre cltk\n\nRequirements:\n   - Python version 3.7 or above\n   - A Unix-like OS\n   - To install from source, see `Development <https://dev.cltk.org/en/latest/includes/development.html>`_ in the docs.\n\n\nDocumentation\n=============\n\nDocumentation at `<https://dev.cltk.org>`_.\n\n\nCitation\n========\n\n.. code-block:: bibtex\n\n   @Misc{johnsonetal2014,\n    author = {Johnson, Kyle P. and Patrick Burns and John Stewart and Todd Cook},\n    title = {CLTK: The Classical Language Toolkit},\n    url = {https://github.com/cltk/cltk},\n    year = {2014--2021},\n   }\n\n\nLicense\n=======\n\n.. |year| date:: %Y\n\nCopyright (c) 2014-|year| Kyle P. Johnson under the `MIT License <https://github.com/cltk/cltk/blob/master/LICENSE>`_.\n",
    'author': 'Kyle P. Johnson',
    'author_email': 'kyle@kyle-p-johnson.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://cltk.org',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
