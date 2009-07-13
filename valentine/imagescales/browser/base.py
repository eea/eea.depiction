from elementtree import ElementTree as ET
from zope.component import adapts, queryMultiAdapter, getMultiAdapter
from zope.interface import implements
from interfaces import IImageTag, IImageLink


class ImageTag(object):

    """Adapts a p4a video object and returns an HTML img tag to its album art.
    """

    implements(IImageTag)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def tag(self, scalename='thumb'):
        """ """
        imgview = getMultiAdapter((self.context, self.request), name='imgview')
        if imgview.display(scalename):
            img = ET.Element('img')
            img.set('src', self.context.absolute_url() + '/image_' + scalename)
            img.set('title', self.context.Title().decode('utf-8'))
            img.set('alt', self.context.Title().decode('utf-8'))
            return ET.tostring(img, 'utf-8')

    __call__ = tag


class BaseImageLink(object):

    """Base class for generating full links."""

    implements(IImageLink)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.classnames = []
        self.title = context.Title()
        self.desc = self.context.Description()

        # This URL adapter is currently located in Products.EEAContentTypes.browser
        url_adapter = queryMultiAdapter((context, request), name='url')
        if url_adapter:
            self.url = url_adapter.listing_url()
        else:
            self.url = context.absolute_url()

    def link(self, imgtag):
        """Should be overridden to customzie link generation logic."""

    def nothumb(self):
        return None

    def __call__(self, scalename='thumb'):
        imgtag = getMultiAdapter((self.context, self.request), name='imgtag')(scalename)
        if imgtag != None:
            return self.link(imgtag)
        return self.nothumb()


class AlbumImageLink(BaseImageLink):

    """Generates thumbnail links designed for atct_album_view."""

    def link(self, imgtag):
        title_tag = '<span class="photoAlbumEntryTitle">%s</span>' % self.title
        classnames = ' '.join(self.classnames)
        return '<a title="%s" href="%s" class="%s">%s%s</a>' % (self.title, self.url, classnames, imgtag, title_tag)


class SummaryImageLink(BaseImageLink):

    """Generates thumbnail links designed for folder_summary_view."""

    def __init__(self, context, request):
        super(SummaryImageLink, self).__init__(context, request)
        self.classnames.append('tileImage')

    def link(self, imgtag):
        classnames = ' '.join(self.classnames)
        return '<a title="%s" href="%s" class="%s">%s</a>' % (self.title, self.url, classnames, imgtag)
