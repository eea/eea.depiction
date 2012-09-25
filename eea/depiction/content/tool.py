""" Depiction tools
"""
from zope.interface import implements
from Products.CMFCore.utils import UniqueObject
from Products.Archetypes.atapi import OrderedBaseFolder
from Products.Archetypes.atapi import OrderedBaseFolderSchema
from Products.Archetypes.atapi import Schema
from eea.depiction.content.interfaces import IDepictionTool

class DepictionTool(UniqueObject, OrderedBaseFolder):
    """ Local utility to store and customize content-types generic thumbnails
    """
    implements(IDepictionTool)

    meta_type = portal_type = 'DepictionTool'

    id_field = OrderedBaseFolderSchema['id'].copy()
    id_field.mode = 'r'
    title_field = OrderedBaseFolderSchema['title'].copy()
    title_field.mode = 'r'

    manage_options = OrderedBaseFolder.manage_options

    schema = OrderedBaseFolderSchema  + Schema((
        id_field,
        title_field,
        ),
    )
