# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['catflow',
 'catflow.atomic',
 'catflow.cmdline',
 'catflow.graph',
 'catflow.metad',
 'catflow.structure',
 'catflow.tesla',
 'catflow.tesla.ai2_kit',
 'catflow.tesla.base',
 'catflow.tesla.dpgen',
 'catflow.utils']

package_data = \
{'': ['*']}

install_requires = \
['ai2-kit>=0.9.0',
 'ase>=3.21.1,<4.0.0',
 'dscribe>=1.2.2,<2.0.0',
 'matplotlib>=3.7.1,<4.0.0',
 'mdanalysis>=2.2,<3.0',
 'numpy>=1.18,<1.24',
 'pandas>=1.3.3,<2.0.0',
 'pymatgen>=2023.5.10,<2024.0.0',
 'scipy>=1.10.1,<2.0.0',
 'seaborn>=0.12.2,<0.13.0']

entry_points = \
{'console_scripts': ['catflow = catflow.cmdline.base:cli']}

setup_kwargs = {
    'name': 'catflow',
    'version': '0.4.0',
    'description': 'Analyzing tool for deep learning based chemical research.',
    'long_description': '# CatFlow\n\n[![Python package](https://github.com/Cloudac7/CatFlow/actions/workflows/ci.yml/badge.svg)](https://github.com/Cloudac7/CatFlow/actions/workflows/ci.yml)\n[![Coverage Status](https://coveralls.io/repos/github/Cloudac7/CatFlow/badge.svg?branch=master)](https://coveralls.io/github/Cloudac7/CatFlow?branch=master)\n\n\nMachine learning aided catalysis reaction free energy calculation and post-analysis workflow, thus, analyzer for catalysis.\n\nAs is known to all, cat is fluid and thus cat flows. 🐱\n\n> Former Miko-Analyzer\n\n## Installation\n\nTo install, clone the repository:\n\n```\ngit clone https://github.com/cloudac7/catflow.git\n```\n\nand then install with `pip`:\n\n```\ncd catflow\npip install .\n```\n\n## Acknowledgement\nThis project is inspired by and built upon the following projects:\n- [ai2-kit](https://github.com/chenggroup/ai2-kit): A toolkit featured artificial intelligence × ab initio for computational chemistry research.\n- [DP-GEN](https://github.com/deepmodeling/dpgen): A concurrent learning platform for the generation of reliable deep learning based potential energy models.\n- [ASE](https://wiki.fysik.dtu.dk/ase/): Atomic Simulation Environment.\n- [DPDispatcher](https://github.com/deepmodeling/dpdispatcher): Generate and submit HPC jobs.\n- [Metadynminer](https://github.com/spiwokv/metadynminer): Reading, analysis and visualization of metadynamics HILLS files produced by Plumed. As well as its Python implementation [Metadynminer.py](https://github.com/Jan8be/metadynminer.py).\n- [stringmethod](https://github.com/apallath/stringmethod): Python implementation of the string method to compute the minimum energy path.\n',
    'author': 'Cloudac7',
    'author_email': 'scottryuu@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/cloudac7/catflow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
