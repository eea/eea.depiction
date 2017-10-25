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

    def __init__(self, context, request):
        super(DexterityImageView, self).__init__(context, request)
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

        scaleview = queryMultiAdapter((self.context, self.request),
                                      name='images')
        scale = scaleview.scale('image', scale=scalename)

        if scale:
            return scale

        return self.context
