""" Traverse
"""
import logging
from zope.publisher.interfaces import NotFound
from Products.CMFCore.utils import getToolByName
from ZPublisher.BaseRequest import DefaultPublishTraverse
from plone.app.imaging.interfaces import IBaseObject
from zope.component import adapts, getAllUtilitiesRegisteredFor
from zope.component import queryMultiAdapter, getMultiAdapter, queryUtility
from zope.interface import providedBy
from zope.publisher.interfaces import IRequest
from plone.app.imaging.traverse import ImageTraverser
from Products.Five.browser import BrowserView
from eea.depiction.interfaces import IDepictionTool
from eea.depiction.interfaces import IDepictionVocabulary

logger = logging.getLogger("eea.depiction")

class ScaleTraverser(ImageTraverser):
    """ Scale traverser for content types

    Taken from
    http://taskman.eionet.europa.eu/projects/zope/wiki/HowToSpecifyFallbackImages

    eea.depiction v0.3 introduces the concept of fallback images when
    the regular image traversal fails. The logic works like this:

    * Look for an image returned by the context's 'imgview' adapter
    * If the imgview crashes, isn't found or can not locate/generate an image,
      we continue by checking if there's an image specified for any of the
      contexts interfaces.
    * If there's no fallback image, we look for an image for the context portal
      type, e.g. article, news-item, document. This should be placed in the
      'portal_depiction' folder.
    * Uses the generic content type image, i.e. portal_depiction/generic

    So:

    * There should be a folder under the site root called 'portal_depiction'
    * In that folder there should be an image called 'generic'.
    * To map a fallback image to a portal type, place it in this folder and
      name it after the portal type.
    * To map a fallback image to an interface, edit the dictionary found in
      eea.depiction.traversal.py
    """

    adapts(IBaseObject, IRequest)

    def fallback(self, request, name):
        """ Fallback
        """
        # Because the following methods of getting a thumbnail are not
        # based on real image fields, we'll look for a fake thumbnail
        # only when the name looks like a thumbnail request
        if (not name.startswith('image_')) or (name.startswith('image_view')):
            return DefaultPublishTraverse.publishTraverse(self, request, name)

        # In some cases we want to fallback on a different image
        # than the one used for the portal type. In this dictionary we can
        # specify images that should be used if the context provides a certain
        # interface. All you have to do is to register a named-utility for
        # IDepictionVocabulary
        overrides = {}
        for voc in getAllUtilitiesRegisteredFor(IDepictionVocabulary):
            overrides.update(
                dict((term.value, term.title) for term in voc(self.context))
            )

        context = self.context
        _fieldname, scale = name.split('_', 1)
        if scale and (scale.lower().endswith('.jpg') or
                      scale.lower().endswith('.png')):
            scale = scale[:-4]

        # Regular imgview
        imgview = queryMultiAdapter((context, request), name='imgview')

        # Fallback imgview
        if (imgview is None) or (not imgview.display(scale)):
            portal = getToolByName(context, 'portal_url').getPortalObject()
            image_obj_id = None
            provided_interfaces = [i.__identifier__
                                   for i in providedBy(context).flattened()]
            for k, v in overrides.items():
                if k in provided_interfaces:
                    image_obj_id = v
                    break

            if image_obj_id is None:
                image_obj_id = context.portal_type.replace(' ', '-').lower()

            tool = queryUtility(IDepictionTool)
            if not tool:
                raise NotFound(portal, 'portal_depiction', request)

            if image_obj_id in tool.objectIds():
                image_obj = tool[image_obj_id]
            else:
                image_obj = tool['generic']
            imgview = getMultiAdapter((image_obj, request), name='imgview')
        return imgview(scale)

class Tag(BrowserView):
    """ /@@tag
    """
    def tag(self, fieldname=None, scale='thumb', height=None, width=None,
            css_class=None, direction='keep', **args):
        """
        Generate an HTML IMG tag for this image, with customization.
        Arguments to self.tag() can be any valid attributes of an IMG
        tag.  'src' will always be an absolute pathname, to prevent
        redundant downloading of images. Defaults are applied
        intelligently for 'height' and 'width'. If specified, the
        'scale' argument will be used to automatically adjust the
        output height and width values of the image tag.

        Since 'class' is a Python reserved word, it cannot be passed in
        directly in keyword arguments which is a problem if you are
        trying to use 'tag()' to include a CSS class. The tag() method
        will accept a 'css_class' argument that will be converted to
        'class' in the output tag to work around this.
        """
        url = self.context.absolute_url()
        src = '%s/image_%s' % (url, scale)
        result = '<img src="%s"' % src

        if height:
            result = '%s height="%s"' % (result, height)

        if width:
            result = '%s width="%s"' % (result, width)

        if css_class is not None:
            result = '%s class="%s"' % (result, css_class)

        if args:
            for key, value in sorted(args.items()):
                if value:
                    result = '%s %s="%s"' % (result, key, value)

        return '%s />' % result

    def __call__(self, **kwargs):
        return self.tag(**kwargs)
