""" ATFolder
"""
from zope.interface import implements
from zope.publisher.interfaces import NotFound
from Products.Five.browser import BrowserView
from eea.depiction.browser.interfaces import IImageView

class FolderImageView(BrowserView):
    """ This view takes the first published/visible image found in a folder
          and returns it in the requested size
    """
    implements(IImageView)

    img = None
    field = None

    def __init__(self, context, request):
        super(FolderImageView, self).__init__(context, request)

        here = '/'.join(self.context.getPhysicalPath())
        results = self.context.portal_catalog.queryCatalog(
                {
                    'portal_type':'Image',
                    'path': {
                        'query':here,
                        'depth':1,
                        },
                    'sort_on': 'getObjPositionInParent'
                    }, #show_all=1, show_inactive=1,
                )
        self.field = None
        self.has_images = False
        if len(results) > 0:
            self.has_images = True
            self.img = results[0].getObject()
            self.field = self.img.getField('image')

    def display(self, scalename='thumb'):
        """ Return a bool if the scale should be displayed
        """
        if not self.has_images:
            return False

        #in some cases the scale cannot be correctly retrieved.
        #We return the whole image then

        if self.field is None:
            return False

        return True

    def __call__(self, scalename='thumb'):
        if not self.display(scalename):
            raise NotFound(self.request, self.name)

        scale = self.field.getScale(self.img, scalename)
        if scale:
            return scale

        #returning the entire image
        return self.field.get(self.img).__of__(self.img)
