""" Various setup
"""

import logging

from eea.depiction.interfaces import IDepictionTool
from plone.app.redirector.interfaces import IRedirectionStorage
from plone.namedfile.file import NamedBlobImage
from plone.namedfile.interfaces import IStorage
from Products.Archetypes.interfaces import IBaseObject
from Products.CMFCore.utils import getToolByName
from zope.component import provideUtility, queryUtility

logger = logging.getLogger('eea.depiction')


def setupGenericImage(site):
    """ Add generic image within portal_depiction if it doesn't exists
    """
    tool = queryUtility(IDepictionTool, context=site)
    tool = tool.__of__(site)

    if 'generic' in tool.objectIds():
        return

    img = site.restrictedTraverse(
        '++resource++eea.depiction.images/generic.jpg')
    data = img.GET()

    # needed for tests
    storage = queryUtility(IStorage, name="__builtin__.str")

    if storage is None:
        from plone.namedfile.storages import StringStorable
        provideUtility(StringStorable(), IStorage, name="__builtin__.str")

    image = NamedBlobImage(data=data, contentType="image/jpeg",
                           filename=u"generic.jpg")

    id = tool.invokeFactory('Image', id='generic', title='Generic')
    obj = tool._getOb(id)

    if IBaseObject.providedBy(obj):
        obj.edit(image=image)
    else:
        obj.image = image


def setupDefaultImages(site):
    """ Move images from valentine-imagescales
    """

    if ('valentine-imagescales' not in site.objectIds() or
            IDepictionTool.providedBy(site['valentine-imagescales'])):

        return setupGenericImage(site)

    valentine = site['valentine-imagescales']
    tool = queryUtility(IDepictionTool)

    for image in valentine.objectIds():
        if image not in tool.objectIds():
            cb = valentine.manage_cutObjects(image)
            tool.manage_pasteObjects(cb)

    oldUrl = "/".join(valentine.getPhysicalPath())
    site.manage_delObjects(['valentine-imagescales'])

    # Add alias
    storage = queryUtility(IRedirectionStorage)
    storage.add(oldUrl, '/'.join(tool.getPhysicalPath()))

    # Setup generic image
    setupGenericImage(site)


def importVarious(self):
    """ Various setup
    """

    if self.readDataFile('eea.depiction.txt') is None:
        return

    site = self.getSite()

    # Portal tool
    tool = getToolByName(site, 'portal_depiction')
    tool.title = 'Depiction Library'
    # remove from portal_catalog
    tool.unindexObject()

    # Setup fallback images for content-types
    setupDefaultImages(site)
