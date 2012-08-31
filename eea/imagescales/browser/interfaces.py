""" Interfaces
"""
from zope.interface import Interface

class IImageView(Interface):
    """ Returns the image stream to the requested image
    """

    def display(scalename):
        """ Says if it's OK to display an image of requested size
        """
