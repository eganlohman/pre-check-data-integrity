# Package setup for Concordance script
import os
from setuptools import setup, find_packages

setup(
      name='concordance test script',
      version='1.0.0',
      py_modules = ['concordance'],
      description='Data integrity pre-check to ensure concordance of two folders',
      install_requires=[
            'argparse',
            'logging'
      ],
      packages=find_packages(),
      include_package_data=True,
      scripts=[],
      requires=[],
      zip_safe=False
)