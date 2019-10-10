""" ATFolder
"""
from zope.interface import implements
from zope.publisher.interfaces import NotFound
from eea.depiction.browser.interfaces import IImageView
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName


class FolderImageView(BrowserView):
    """ This view takes the first published/visible image found in a folder
          and returns it in the requested size
    """
    implements(IImageView)

    _img = False
    _field = False

    @property
    def img(self):
        """ img
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

    @property
    def field(self):
        """ Field
        """
        if self._field is False:
            if self.img:
                self._field = self.img.getField('image')
            else:
                self._field = None
        return self._field

    def display(self, scalename='thumb'):
        """ Return a bool if the scale should be displayed
        """

        if not self.img:
            return False

        if not self.field:
            return False

        return True

    def __call__(self, scalename='thumb'):
        if not self.display(scalename):
            raise NotFound(self.request, self.name)

        scale = self.field.getScale(self.img, scalename)

        if scale:
            return scale

        # returning the entire image

        return self.field.get(self.img).__of__(self.img)
