""" Dexterity
"""

from zope.component import queryMultiAdapter
from zope.interface import implements
from zope.publisher.interfaces import NotFound

from eea.depiction.browser.interfaces import IImageView
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView


class DexterityImageView(BrowserView):
    """ Image View
    """
    implements(IImageView)
    _field = False
    _img = False
    fieldname = 'image'

    @property
    def field(self):
        """ Image field
        """
        if self._field is False:
            self._field = getattr(self.img, self.fieldname, None)
        return self._field

    @property
    def img(self):
        """ Img
        """
        return self.context

    def display(self, scalename='thumb'):
        """ Display
        """

        if not bool(self.field):
            return False

        scaleview = queryMultiAdapter((self.context, self.request),
                                      name='images')

        scale = scaleview.scale(str(self.fieldname), scale=scalename)

        if not scale:
            return False
        return True

    def __call__(self, scalename='thumb'):
        if not self.display(scalename):
            raise NotFound(self.request, scalename)

        scaleview = queryMultiAdapter((self.img, self.request), name='images')
        scale = scaleview.scale(str(self.fieldname), scale=scalename)

        return scale or ""


class DexterityContainerImageView(DexterityImageView):
    """ Image View for Dexterity containers
    """
    implements(IImageView)
    _field = False
    _img = False

    @property
    def img(self):
        """ Img
        """
        if self._img is False:
            here = '/'.join(self.context.getPhysicalPath())
            query = {
                'portal_type': 'Image',
                'path': {
                    'query': here,
                    'depth': 1
                },
                'sort_on': 'getObjPositionInParent'
            }
            ctool = getToolByName(self.context, 'portal_catalog')
            if 'Language' in ctool.indexes():
                query['Language'] = 'all'

            self._img = None
            brains = ctool(**query)
            for idx, brain in enumerate(brains):
                if idx == 0:
                    self._img = brain.getObject()
                if 'cover' in brain.getId:
                    self._img = brain.getObject()
                    break
        return self._img

    def display(self, scalename='thumb'):
        """ Return a bool if the scale should be displayed
        """

        if not self.img:
            return False

        if not self.field:
            return False

        return True
