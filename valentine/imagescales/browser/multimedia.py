import os.path
from zope.interface import implements
from zope.publisher.interfaces import NotFound
from Products.Five.browser import BrowserView
from p4a.video.interfaces import IVideo

import OFS.Image
import PIL.Image
from StringIO import StringIO

from interfaces import IImageView
import base


class ImageView(BrowserView):
    
    """Adapts a p4a video object and returns its album art image.

    This makes it possible to enter a URL like my_vid_file/image_thumb and have it return
    the p4a album art - no need for p4a's long and weird looking video art URLs.
    """

    implements(IImageView)

    # Copied from EEAContentTypes/content/ExternalHighlight.py 2009-02-18
    sizes = { 'large'   : (768, 768),
              'preview' : (400, 400),
              'mini'    : (180, 135),
              'thumb'   : (128, 128),
              'tile'    :  (64, 64),
              'icon'    :  (32, 32),
              'listing' :  (16, 16),
    }

    def __init__(self, context, request):
        self.context = context
        self.request = request
        path = os.path.dirname(__file__)
        path = os.path.join(path, 'images', 'play-button.png')
        self.button = open(path).read()
        self.img = IVideo(self.context).video_image

    def display(self, scalename='thumb'):
        return (self.img != None) and (scalename in ImageView.sizes)

    def __call__(self, scalename='thumb', fieldname='image'):
        if not self.display(scalename):
            raise NotFound(self.request, scalename)
        # XXX should be done once then cached
        return thumbnail(self.img.data, self.button, ImageView.sizes[scalename])


def thumbnail(thumb, button, size):
    """Scale and apply play-button and borders on an uploaded thumbnail.
    
    First two argument should be raw image data.
    """
    thumbfile = StringIO(thumb)
    buttonfile = StringIO(button)
    destfile = StringIO()

    thumb = PIL.Image.open(thumbfile)
    button = PIL.Image.open(buttonfile)

    origsize = thumb.size
    newsize = size
    aspect = float((newsize[0]) / float(origsize[0]))
    buttonsize = (newsize[0], origsize[1] * aspect)

    thumb = thumb.resize(buttonsize, PIL.Image.ANTIALIAS)
    button = button.resize(size, PIL.Image.ANTIALIAS)

    x, y = 0, (size[1]/2) - (thumb.size[1]/2)
    w, h = x + thumb.size[0], y + thumb.size[1]

    bg = PIL.Image.new('RGB', size, color=(0, 0, 0))
    bg.paste(thumb, (x, y, w, h))
    bg.paste(button, (0, 0), button)
    bg.save(destfile, 'PNG')

    destfile.seek(0)
    dest = OFS.Image.Image('tmp-video-thumb', 'tmp-video-thumb', destfile)
    dest.width = size[0]
    dest.height = size[1]
    return dest


class AlbumImageLink(base.AlbumImageLink):

    """ """

    def __init__(self, context, request):
        super(AlbumImageLink, self).__init__(context, request)
        self.classnames.append('thickbox')
        self.url = context.absolute_url() + '/view'


class SummaryImageLink(base.SummaryImageLink):

    """ """

    def __init__(self, context, request):
        super(SummaryImageLink, self).__init__(context, request)
        self.classnames.append('thickbox')
        self.url = context.absolute_url() + '/view'
