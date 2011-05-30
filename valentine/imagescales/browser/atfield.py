""" AT Field
"""
from zope.interface import implements
from zope.publisher.interfaces import NotFound
from Products.Five.browser import BrowserView
from valentine.imagescales.browser.interfaces import IImageView

class ImageView(BrowserView):
    """ Image View
    """
    implements(IImageView)

    def __init__(self, context, request):
        super(ImageView, self).__init__(context, request)
        self.field = context.getField('image')

    def display(self, scalename='thumb'):
        """ Display
        """
        return bool(self.field.getScale(self.context, scale=scalename))

        #this improves performance if you're missing the blobs
        #try:
            #return bool(self.field.getScale(self.context, scale=scalename))
        #except:
            #return False

    def __call__(self, scalename='thumb'):
        if not self.display(scalename):
            raise NotFound(self.request, scalename)
        return self.field.getScale(self.context, scale=scalename)
