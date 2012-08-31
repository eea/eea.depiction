""" Test Scale Traverser
"""
from App.Common import package_home
from eea.imagescales.tests.base import ImageScalesTestCase
import doctest
from os.path import join
import unittest
from Testing.ZopeTestCase import FunctionalDocFileSuite

optionflags =  (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE |
                doctest.REPORT_ONLY_FIRST_FAILURE)

def setUpImg(self):
    """ Setup an image
    """
    img_file = join(package_home(globals()), 'data', 'test.png')
    img = open(img_file, 'rb').read()
    globs = {}
    globs['img'] = img
    globs['imgfile'] = img_file

    img_file = join(package_home(globals()), 'data', 'test.tif')
    img = open(img_file, 'rb').read()
    globs['tiff'] = img
    globs['tiff_file'] = img_file

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

    return unittest.TestSuite((
        FunctionalDocFileSuite('README.txt',
                               setUp=setUpReadme,
                               test_class = ImageScalesTestCase,
                               optionflags=optionflags,
                               package = 'eea.imagescales'),
        FunctionalDocFileSuite('atfield.txt',
                               setUp=setUpImg,
                               test_class = ImageScalesTestCase,
                               optionflags=optionflags,
                               package = 'eea.imagescales.browser'),
        FunctionalDocFileSuite('atfolder.txt',
                               setUp=setUpImg,
                               test_class = ImageScalesTestCase,
                               optionflags=optionflags,
                               package = 'eea.imagescales.browser'),
        FunctionalDocFileSuite('attopic.txt',
                               setUp=setUpImg,
                               test_class = ImageScalesTestCase,
                               optionflags=optionflags,
                               package = 'eea.imagescales.browser'),
        FunctionalDocFileSuite('multimedia.txt',
                               setUp=setUpMultimedia,
                               test_class = ImageScalesTestCase,
                               optionflags=optionflags,
                               package = 'eea.imagescales.browser'), ))
