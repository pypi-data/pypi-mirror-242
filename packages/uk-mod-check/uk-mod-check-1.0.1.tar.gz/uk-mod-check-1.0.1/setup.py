#!/usr/bin/env python3

import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
      name='uk-mod-check',
      url='https://github.com/as207960/uk-mod-check',
      long_description_content_type='text/markdown',
      long_description=README,
      version='1.0.1',
      author='Q 🦄 (on behalf of AS207960)',
      author_email='q@as307960.net',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      package_data={
            '': ['data/*.txt']
      },
)
