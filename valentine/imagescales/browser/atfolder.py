from zope.interface import implements
from zope.publisher.interfaces import NotFound
from Products.Five.browser import BrowserView
from interfaces import IImageView


class ImageView(BrowserView):

    """This view takes the first published/visible image found in a folder
    and returns it in the requested size."""

    implements(IImageView)

    img = None

    def display(self, scalename='thumb'):
        """return a bool if the scale should be displayed
        """
        here = '/'.join(self.context.getPhysicalPath())
        results = self.context.portal_catalog.queryCatalog(
                {
                    'portal_type':'Image',
                    'path': {
                        'query':here,
                        'depth':1,
                        },
                    }, #show_all=1, show_inactive=1,
                )
        self.field = None
        self.has_images = False
        if len(results) > 0:
            self.has_images = True
            self.img = results[0].getObject()
            self.field = self.img.getField('image')
        if not self.has_images:
            return False
        return (self.field != None) and \
                    bool(self.field.getScale(self.img, scalename))

    def __call__(self, scalename='thumb'):
        if not self.display(scalename):
            raise NotFound(self.request, self.name)
        return self.field.getScale(self.img, scale=scalename)
