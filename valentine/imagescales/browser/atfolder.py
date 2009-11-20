from zope.interface import implements
from zope.publisher.interfaces import NotFound
from Products.Five.browser import BrowserView
from interfaces import IImageView


class ImageView(BrowserView):

    """This view takes the first published/visible image found in a folder and returns it in
    the requested size."""

    implements(IImageView)

    def __init__(self, context, request):
        super(ImageView, self).__init__(context, request)
        results = context.getFolderContents(contentFilter={
            'portal_type': 'Image',
            'review_state': ['published','visible'],
        })
        self.field = None
        self.has_images = False
        if len(results) > 0:
            self.has_images = True
            self.img = results[0].getObject()
            self.field = self.img.getField('image')

    def display(self, scalename='thumb'):
        if not self.has_images:
            return False
        return (self.field != None) and bool(self.field.getScale(self.img, scalename))

    def __call__(self, scalename='thumb'):
        if not self.display(scalename):
            raise NotFound(self.request, self.name)
        return self.field.getScale(self.img, scale=scalename)
