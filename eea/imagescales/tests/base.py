""" Base
"""
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
from Products.Five import zcml
from Products.Five import fiveconfigure
import eea.depiction
import p4a.video

@onsetup
def setup_depiction():
    """ Setup
    """
    fiveconfigure.debug_mode = True
    zcml.load_config('test.zcml', p4a.video)
    zcml.load_config('configure.zcml', eea.depiction)
    zcml.load_config('overrides.zcml', eea.depiction)
    fiveconfigure.debug_mode = False

    PloneTestCase.installPackage('p4a.video')

setup_depiction()
PloneTestCase.setupPloneSite(extension_profiles=(
                                  'eea.depiction:default',))

class DepictionTestCase(PloneTestCase.FunctionalTestCase):
    """ Depiction Test Case
    """
    pass

class DepictionFunctionalTestCase(PloneTestCase.FunctionalTestCase):
    """ Depiction Functional Test Case
    """
    pass
