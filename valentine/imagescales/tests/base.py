from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
from Products.Five import zcml
from Products.Five import fiveconfigure
import valentine.imagescales


@onsetup
def setup_thumbnailer():
    fiveconfigure.debug_mode = True
    import Products.Five
    import Products.FiveSite
    zcml.load_config('meta.zcml', Products.Five)
    zcml.load_config('configure.zcml', Products.FiveSite)
    fiveconfigure.debug_mode = False
    ztc.installProduct('Five')
    zcml.load_config('configure.zcml', valentine.imagescales)


setup_thumbnailer()
PloneTestCase.setupPloneSite(products='valentine.imagescales')


class ImageScalesTestCase(PloneTestCase.PloneTestCase):
    pass


class ImageScalesFunctionalTestCase(PloneTestCase.FunctionalTestCase):
    pass
