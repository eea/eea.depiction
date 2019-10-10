""" AT Field
"""
from zope.interface import implements
from zope.publisher.interfaces import NotFound
from Products.Five.browser import BrowserView
from eea.depiction.browser.interfaces import IImageView


class ATFieldImageView(BrowserView):
    """ Image View
    """
    implements(IImageView)
    _field = False

    @property
    def field(self):
        """ self.field
        """
        if self._field is False:
            self._field = self.context.getField('image')
        return self._field

    def display(self, scalename='thumb'):
        """ Display
        """
        if not bool(self.field):
            return False

        scale = self.field.getScale(self.context, scale=scalename)
        if not scale:
            return False
        return True

    def __call__(self, scalename='thumb'):
        if not self.display(scalename):
            raise NotFound(self.request, scalename)

        scale = self.field.getScale(self.context, scale=scalename)
        if scale:
            return scale

        return self.field.get(self.context).__of__(self.context)
