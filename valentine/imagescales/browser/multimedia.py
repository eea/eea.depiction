import os.path
from zope.interface import implements
from zope.publisher.interfaces import NotFound
from Products.Five.browser import BrowserView
from p4a.video.interfaces import IVideo

import OFS.Image
import PIL.Image
from StringIO import StringIO

from interfaces import IImageView


class ImageView(BrowserView):
    
    """Adapts a p4a video object and returns its album art image.

    This makes it possible to enter a URL like my_vid_file/image_thumb and have it return
    the p4a album art - no need for p4a's long and weird looking video art URLs.
    """

    implements(IImageView)

    # Copied from EEAContentTypes/content/ExternalHighlight.py 2009-02-18
    # Added 'wide' size
    sizes = {
        'large'   : (768, 768),
        'preview' : (400, 400),
        'mini'    : (180, 135),
        'thumb'   : (128, 128),
        'wide'    : (325, 183),
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
        # XXX This scaling should be done once and then cached
        if not self.display(scalename):
            raise NotFound(self.request, scalename)
        orig = PIL.Image.open(StringIO(self.img.data))
        button = PIL.Image.open(StringIO(self.button))
        thumb = thumbnail(orig, button, ImageView.sizes[scalename])

        destfile = StringIO()
        thumb.save(destfile, 'PNG')
        destfile.seek(0)

        dest = OFS.Image.Image('tmp-video-thumb', 'tmp-video-thumb', destfile)
        dest.width = thumb.size[0]
        dest.height = thumb.size[1]
        return dest


def thumbnail(orig, button, size):
    # Create an image with the requested size
    bg = PIL.Image.new('RGB', size, color=(0, 0, 0))

    # Scale the original image. If we're scaling a 4:3 to 16:9, we max the
    # height and scale the width as far as we can, and vice versa
    if ((float(size[0])/size[1]) > (float(orig.size[0])/orig.size[1])):
        aspect = float((size[1]) / float(orig.size[1]))
        thumb_size = (int(size[0] * aspect), orig.size[1])
    else:
        aspect = float((size[0]) / float(orig.size[0]))
        thumb_size = (size[0], int(orig.size[1] * aspect))
    thumb = orig.resize(thumb_size, PIL.Image.ANTIALIAS)

    # Paste it onto the background (centered)
    x = (bg.size[0]/2) - (thumb.size[0]/2)
    y = (bg.size[1]/2) - (thumb.size[1]/2)
    w = x + thumb.size[0]
    h = y + thumb.size[1]
    bg.paste(thumb, (x, y, w, h))

    # Apply the play button (centered)
    scale = float(size[1]) / button.size[1]
    new_button_size = (int(button.size[0]*scale), int(button.size[1]*scale))
    button = button.resize(new_button_size, PIL.Image.ANTIALIAS)
    x = (bg.size[0]/2) - (button.size[0]/2)
    y = (bg.size[1]/2) - (button.size[1]/2)
    bg.paste(button, (x, y), button)

    return bg

