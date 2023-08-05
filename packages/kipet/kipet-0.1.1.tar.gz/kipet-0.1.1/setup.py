# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kipet',
 'kipet.examples',
 'kipet.library',
 'kipet.library.common',
 'kipet.library.core_methods',
 'kipet.library.dev_tools',
 'kipet.library.mixins',
 'kipet.library.model_components',
 'kipet.library.nsd_funs',
 'kipet.library.post_model_build',
 'kipet.library.spectra_methods',
 'kipet.library.top_level',
 'kipet.library.variance_methods',
 'kipet.library.visuals',
 'kipet.new_examples',
 'kipet.validation',
 'kipet.validation.test_problems.Paper',
 'kipet.validation.test_problems.case51a.casadi',
 'kipet.validation.test_problems.case51a.pyomo',
 'kipet.validation.test_problems.case51a.pyomo.sipopt',
 'kipet.validation.test_problems.case51b.casadi',
 'kipet.validation.test_problems.case51b.pyomo',
 'kipet.validation.test_problems.case51b.pyomo.sipopt',
 'kipet.validation.test_problems.case51c.casadi',
 'kipet.validation.test_problems.case51c.pyomo',
 'kipet.validation.test_problems.case52b.casadi',
 'kipet.validation.test_problems.case52b.pyomo',
 'kipet.validation.test_problems.complementary_states.casadi',
 'kipet.validation.test_problems.complementary_states.pyomo',
 'kipet.validation.test_problems.plain_pyomo',
 'kipet.validation.test_problems.sawall.casadi',
 'kipet.validation.test_problems.sawall.pyomo']

package_data = \
{'': ['*'],
 'kipet': ['data/example_data/*', 'data/example_data_new/*'],
 'kipet.validation': ['test_problems/data_sets/*']}

install_requires = \
['Pint>=0.16.1,<0.17.0',
 'Pyomo>=5.7.3,<6.0.0',
 'ipopt>=0.3.0,<0.4.0',
 'matplotlib>=3.3.4,<4.0.0',
 'numpy>=1.20.1,<2.0.0',
 'pandas>=1.2.2,<2.0.0',
 'plotly>=4.14.3,<5.0.0',
 'scipy>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'kipet',
    'version': '0.1.1',
    'description': 'An all-in-one tool for fitting kinetic models using spectral and other state data',
    'long_description': None,
    'author': 'Kevin McBride',
    'author_email': 'kevin.w.mcbride.86@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
