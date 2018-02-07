""" Dexterity
"""

from eea.depiction.browser.interfaces import IImageView
from Products.Five.browser import BrowserView
from zope.component import queryMultiAdapter
from zope.interface import implements
from zope.publisher.interfaces import NotFound


class DexterityImageView(BrowserView):
    """ Image View
    """
    implements(IImageView)
    field = None
    img = None

    def __init__(self, context, request):
        super(DexterityImageView, self).__init__(context, request)
        self.img = context
        self.field = getattr(context, 'image', None)

    def display(self, scalename='thumb'):
        """ Display
        """

        if not bool(self.field):
            return False

        scaleview = queryMultiAdapter((self.context, self.request),
                                      name='images')
        scale = scaleview.scale('image', scale=scalename)

        if not scale:
            return False

        return True

    def __call__(self, scalename='thumb'):
        if not self.display(scalename):
            raise NotFound(self.request, scalename)

        scaleview = queryMultiAdapter((self.img, self.request), name='images')
        scale = scaleview.scale('image', scale=scalename)

        return scale or ""


class DexterityContainerImageView(DexterityImageView):
    """ Image View for Dexterity containers
    """

    implements(IImageView)
    field = None
    img = None

    def __init__(self, context, request):
        super(DexterityContainerImageView, self).__init__(context, request)

        here = '/'.join(self.context.getPhysicalPath())
        results = self.context.portal_catalog.queryCatalog(
            {
                'portal_type': 'Image',
                'path': {
                    'query': here,
                    'depth': 1,
                },
                'sort_on': 'getObjPositionInParent'
            },  # show_all=1, show_inactive=1,
        )
        self.field = None
        self.has_images = False

        if results:
            self.has_images = True
            self.img = results[0].getObject()
            self.field = getattr(self.img, 'image', None)

    def display(self, scalename='thumb'):
        """ Return a bool if the scale should be displayed
        """

        if not self.has_images:
            return False

        if self.field is None:
            return False

        return True
