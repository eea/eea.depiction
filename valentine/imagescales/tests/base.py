#from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
from Products.Five import zcml
from Products.Five import fiveconfigure
import valentine.imagescales
import p4a.video


@onsetup
def setup_thumbnailer():
    fiveconfigure.debug_mode = True
    zcml.load_site()
    zcml.load_config('configure.zcml', p4a.video)
    zcml.load_config('test.zcml', p4a.video)
    zcml.load_config('configure.zcml', valentine.imagescales)
    zcml.load_config('overrides.zcml', valentine.imagescales)
    fiveconfigure.debug_mode = False


setup_thumbnailer()
PloneTestCase.setupPloneSite(
        products='valentine.imagescales',
        extension_profiles=['plone.app.imaging:default'],
        )


class ImageScalesTestCase(PloneTestCase.FunctionalTestCase):    #PloneTestCase
    pass


class ImageScalesFunctionalTestCase(PloneTestCase.FunctionalTestCase):
    pass
