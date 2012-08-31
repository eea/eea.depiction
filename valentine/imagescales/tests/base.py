""" Base
"""
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
from Products.Five import zcml
from Products.Five import fiveconfigure
import valentine.imagescales
import p4a.video

@onsetup
def setup_imagescales():
    """ Setup
    """
    fiveconfigure.debug_mode = True
    zcml.load_config('test.zcml', p4a.video)
    zcml.load_config('configure.zcml', valentine.imagescales)
    zcml.load_config('overrides.zcml', valentine.imagescales)
    fiveconfigure.debug_mode = False

    PloneTestCase.installPackage('p4a.video')

setup_imagescales()
PloneTestCase.setupPloneSite(extension_profiles=(
                                  'valentine.imagescales:default',))

class ImageScalesTestCase(PloneTestCase.FunctionalTestCase):
    """ Image Scales Test Case
    """
    pass

class ImageScalesFunctionalTestCase(PloneTestCase.FunctionalTestCase):
    """ Image Scales Functional Test Case
    """
    pass
