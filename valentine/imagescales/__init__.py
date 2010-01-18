from os.path import dirname
from Globals import package_home
from Products.CMFCore import utils as cmfutils
from Products.CMFCore.DirectoryView import registerDirectory

ppath = cmfutils.ProductsPath
cmfutils.ProductsPath.append(dirname(package_home(globals())))
cmfutils.ProductsPath = ppath

import patches

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

