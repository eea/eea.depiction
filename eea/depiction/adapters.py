from plone.app.blob.field import ReuseBlob
from plone.app.blob.interfaces import IBlobbable
from plone.namedfile.interfaces import INamedBlobFile
from zope.component import adapts
from zope.interface import implements


class BlobbableNamedBlobFile(object):
    """ adapter for BlobWrapper objects to work with blobs """

    implements(IBlobbable)
    adapts(INamedBlobFile)

    def __init__(self, context):
        self.context = context

    def feed(self, blob):
        """ see interface ... """
        raise ReuseBlob(self.context._blob)

    def filename(self):
        """ see interface ... """

        return self.context.filename

    def mimetype(self):
        """ see interface ... """

        return self.context.contentType
