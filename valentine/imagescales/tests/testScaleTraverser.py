import os
import os.path
from Globals import package_home
import unittest
import doctest
from base import ImageScalesTestCase


def setUpImg(self):
    img_file = os.path.join(package_home(globals()), 'data', 'test.png')
    img = open(img_file, 'rb').read()
    globs = {}
    globs['img'] = img
    globs['imgfile'] = img_file

    img_file = os.path.join(package_home(globals()), 'data', 'test.tif')
    img = open(img_file, 'rb').read()
    globs['tiff'] = img
    globs['tiff_file'] = img_file

    self.globs.update(globs)


def setUpMultimedia(self):
    setUpImg(self)
    globs = {}
    globs['samplefilename'] = 'barsandtone.flv'
    globs['samplefile'] = os.path.join(package_home(globals()), 'data', 'barsandtone.flv')
    globs['sampledata'] = open(globs['samplefile'], 'rb').read()
    globs['mimetype'] = 'video/x-flv'
    self.globs.update(globs)


def setUpReadme(self):
    img_file = os.path.join(package_home(globals()), 'data', 'test.png')
    globs = {}
    globs['mp3_icon_file_name'] = img_file
    self.globs.update(globs)


def test_suite():
    from Testing.ZopeTestCase import FunctionalDocFileSuite

    return unittest.TestSuite((
        FunctionalDocFileSuite('README.txt',
                     setUp=setUpReadme,
                     test_class = ImageScalesTestCase,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
                     package = 'valentine.imagescales'),
        FunctionalDocFileSuite('atfield.txt',
                     setUp=setUpImg,
                     test_class = ImageScalesTestCase,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
                     package = 'valentine.imagescales.browser'),
        FunctionalDocFileSuite('atfolder.txt',
                     setUp=setUpImg,
                     test_class = ImageScalesTestCase,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
                     package = 'valentine.imagescales.browser'),
        FunctionalDocFileSuite('attopic.txt',
                     setUp=setUpImg,
                     test_class = ImageScalesTestCase,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
                     package = 'valentine.imagescales.browser'),
        FunctionalDocFileSuite('multimedia.txt',
                     setUp=setUpMultimedia,
                     test_class = ImageScalesTestCase,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
                     package = 'valentine.imagescales.browser'),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
