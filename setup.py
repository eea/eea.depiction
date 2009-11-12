from setuptools import setup, find_packages
import os
from os.path import join

name = 'valentine.imagescales'
path = name.split('.') + ['version.txt']
version = open(join(*path)).read().strip()

setup(name='valentine.imagescales',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Per Thulin',
      author_email='per.thulin at valentinewebsystems dot se',
      url='https://svn.plone.org/svn/collective/valentine.imagescales/trunk',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['valentine'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
