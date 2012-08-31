""" Valentine Image Scales installer
"""
from setuptools import setup, find_packages
import os

NAME = 'valentine.imagescales'
PATH = NAME.split('.') + ['version.txt']
VERSION = open(os.path.join(*PATH)).read().strip()

setup(name=NAME,
      version=VERSION,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
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
          'Pillow',
          'p4a.video',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
