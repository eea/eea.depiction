====================
Valenine Imagescales
====================

Imagescales is a generic system for creating thumbnails/image representations
for content types, both those provided by Plone, and custom ones. To make it
work for a content type, three adapters need to be provided:

 1. ImageView that retrieves an image in the desired scale.
 2. ImageTag that returns the HTML tag for the image
 3. ImageLink that returns the HTML link to the image.

For the most part, only the ImageView (retrieval of image) is specific for the
content type and needs to be provided. For the other two, there are generic
ones in valentine.imagescales.browser.base.

Consider this example for an mp3-song content type:

  >>> from zope.interface import Interface, implements, Attribute
  >>> class IMp3File(Interface):
  ...     pass
  >>> from Products.ATContentTypes.content.file import ATFile
  >>> class Mp3File(ATFile):
  ...     implements(IMp3File)

Now we create an adapter to make an image representation of the file.  We
simply choose to display a generic icon for mp3-files. For now we're
happy with a generic mp3-icon, but the representation could be anything you
can think of, for example a graph of the songs bpm.

  >>> from valentine.imagescales.browser.interfaces import IImageView
  >>> from OFS.Image import Image
  >>> class ImageView(object):
  ...     implements(IImageView)
  ...     def __init__(self, context, request):
  ...         self.context = context
  ...         self.request = request
  ...     def display(self, scalename):
  ...         return True
  ...     def __call__(self, scalename='thumb'):
  ...         mp3_icon = open(mp3_icon_file_name)
  ...         return Image('tmp-mp3-image', 'tmp-mp3-image', mp3_icon)

The scalename is a hint of the wanted image size. It's up to the adapter to
deal with it. In this simple example, we choose to ignore it.

  >>> from zope.component import provideAdapter
  >>> from zope.publisher.interfaces import IRequest
  >>> provideAdapter(ImageView, adapts=(IMp3File, IRequest), name=u'imgview')

Ok, now we have both our content type and imgview adapter set up. So let's
create an mp3file and get the image for it:

  >>> self.portal.mp3file = Mp3File('test_mp3_file')
  >>> from zope.component import getMultiAdapter
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> imgview = getMultiAdapter((self.portal.mp3file, request), name=u'imgview')
  >>> imgview('icon')
  <Image at ...>


HTML Generation
---------------

We now have an adapter that retrieves the actual image, but for showing the
image inside a page we need something that generates the HTML img tag. That's
what the ImageTag adapters is for:

  >>> from valentine.imagescales.browser.base import ImageTag
  >>> provideAdapter(ImageTag, adapts=(IMp3File, IRequest), name=u'imgtag')
  >>> imgtag = getMultiAdapter((self.portal.mp3file, request), name=u'imgtag')

It spits out an imgtag with the 'src' attribute set to the image:

  >>> from elementtree import ElementTree as ET
  >>> html = ET.XML(imgtag('icon'))
  >>> html.tag
  'img'
  >>> html.get('src')
  'http://nohost/plone/test_mp3_file/image_icon'

