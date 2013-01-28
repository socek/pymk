# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages
import sys

install_requires = [
    'jinja2',
]

dependency_links = [
]

if __name__ == '__main__':
    setup(name='Pymk',
          version='0.2.0',
          description="Make like program, which reads python script as makefile.",
          author='Dominik "Socek" Długajczyk',
          author_email='msocek@gmail.com',
          packages=find_packages(),
          install_requires=install_requires,
          dependency_links=dependency_links,
          test_suite='pymk.tests.get_all_test_suite',
          package_data={'Pymk': [
                        'pymk/tests/tmpl/*.tpl',
                        ]},

          entry_points="""\
            [console_scripts]
                pymk = pymk.script:run
""",
          )
