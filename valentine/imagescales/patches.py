from cStringIO import StringIO
from collective.monkey.monkey import Patcher

from Products.Archetypes import Field
try:
    import PIL.Image
except ImportError:
    HAS_PIL=False
    PIL_ALGO = None
else:
    HAS_PIL=True
    PIL_ALGO = PIL.Image.ANTIALIAS


atpatcher = Patcher('Archetypes')

def scale(self, data, w, h, default_format = 'PNG'):
    """ scale image (with material from ImageTag_Hotfix)"""
    #make sure we have valid int's
    size = int(w), int(h)

    original_file=StringIO(data)
    image = PIL.Image.open(original_file)
    # consider image mode when scaling
    # source images can be mode '1','L,','P','RGB(A)'
    # convert to greyscale or RGBA before scaling
    # preserve palletted mode (but not pallette)
    # for palletted-only image formats, e.g. GIF
    # PNG compression is OK for RGBA thumbnails
    original_mode = image.mode
    if original_mode == '1':
        image = image.convert('L')
    elif original_mode == 'P':
        image = image.convert('RGBA')
    image.thumbnail(size, self.pil_resize_algo)
    # XXX: tweak to make the unit test
    #      test_fields.ProcessingTest.test_processing_fieldset run
    format = image.format in ('PNG', 'GIF', 'JPG') and image.format or default_format
    # decided to only preserve palletted mode
    # for GIF, could also use image.format in ('GIF','PNG')
    if original_mode == 'P' and format == 'GIF':
        image = image.convert('P')
    thumbnail_file = StringIO()
    # quality parameter doesn't affect lossless formats
    image.save(thumbnail_file, format, quality=self.pil_quality)
    thumbnail_file.seek(0)
    return thumbnail_file, format.lower()

atpatcher.wrap_method(Field.ImageField, 'scale', scale)
