""" Test Scale Traverser
"""
import doctest
from os.path import join
import unittest
from App.Common import package_home
from eea.depiction.tests.base import DepictionTestCase
from eea.depiction.tests.base import P_VIDEO
from Testing.ZopeTestCase import FunctionalDocFileSuite

TEST_PNG_PATH = join(package_home(globals()), 'data', 'test.png')
TEST_TIF_PATH = join(package_home(globals()), 'data', 'test.tif')
DATA_TMP_DIR = join(package_home(globals()), 'data', 'tmp')

optionflags = (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE |
                doctest.REPORT_ONLY_FIRST_FAILURE)

def setUpImg(self):
    """ Setup an image
    """
    img = open(TEST_PNG_PATH, 'rb').read()
    globs = {}
    globs['img'] = img
    globs['imgfile'] = TEST_PNG_PATH

    img = open(TEST_TIF_PATH, 'rb').read()
    globs['tiff'] = img
    globs['tiff_file'] = TEST_TIF_PATH

    self.globs.update(globs)

def setUpMultimedia(self):
    """ Setup multimedia
    """
    setUpImg(self)
    globs = {}
    globs['samplefilename'] = 'barsandtone.flv'
    globs['samplefile'] = join(package_home(globals()),
                               'data',
                               'barsandtone.flv')
    globs['sampledata'] = open(globs['samplefile'], 'rb').read()
    globs['mimetype'] = 'video/x-flv'
    self.globs.update(globs)

def setUpReadme(self):
    """ Setup readme
    """
    img_file = join(package_home(globals()), 'data', 'test.png')
    globs = {}
    globs['mp3_icon_file_name'] = img_file
    self.globs.update(globs)

def test_suite():
    """ Test suite
    """

    suite = unittest.TestSuite((
        FunctionalDocFileSuite('README.txt',
                               setUp=setUpReadme,
                               test_class=DepictionTestCase,
                               optionflags=optionflags,
                               package='eea.depiction'),
        FunctionalDocFileSuite('atfield.txt',
                               setUp=setUpImg,
                               test_class=DepictionTestCase,
                               optionflags=optionflags,
                               package='eea.depiction.browser'),
        FunctionalDocFileSuite('atfolder.txt',
                               setUp=setUpImg,
                               test_class=DepictionTestCase,
                               optionflags=optionflags,
                               package='eea.depiction.browser'),
        FunctionalDocFileSuite('attopic.txt',
                               setUp=setUpImg,
                               test_class=DepictionTestCase,
                               optionflags=optionflags,
                               package='eea.depiction.browser'),
        FunctionalDocFileSuite('marshaller.txt',
                               setUp=setUpImg,
                               test_class=DepictionTestCase,
                               optionflags=optionflags,
                               package='eea.depiction'), ))

    if P_VIDEO:
        suite.addTest(
            FunctionalDocFileSuite('multimedia.txt',
                                   setUp=setUpMultimedia,
                                   test_class=DepictionTestCase,
                                   optionflags=optionflags,
                                   package='eea.depiction.browser')
        )
    return suite
