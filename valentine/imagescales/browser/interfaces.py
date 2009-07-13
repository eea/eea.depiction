from zope.interface import Interface


class IImageTag(Interface):

    """Provides the HTML img tag to the image in the requested size."""

    def tag(scalename='thumb'):
        """Provides an HTML img tag."""


class IImageView(Interface):
    
    """Returns the image stream to the requested image."""

    def display(scalename):
        """Says if it's OK to display an image of requested size."""


class IImageLink(Interface):

    """Returns the full anchor-linked thumbnail image."""

    def link(imgtag):
        pass
