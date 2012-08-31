""" Traverse
"""
from Products.CMFCore.utils import getToolByName
from ZPublisher.BaseRequest import DefaultPublishTraverse
from plone.app.imaging.interfaces import IBaseObject
from zope.component import adapts
from zope.component import queryMultiAdapter, getMultiAdapter
from zope.interface import providedBy
from zope.publisher.interfaces import IRequest
from plone.app.imaging.traverse import ImageTraverser
import logging

logger = logging.getLogger("eea.imagescales")

# In some cases we want to fallback on a different image than the one used
# for the portal type. In this dictionary we can specify images that should
# be used if the context provides a certain interface. TODO: move to vocabulary
# outside eea.imagescales.
overrides = {
    'Products.EEAContentTypes.content.interfaces.IInteractiveMap':
                                                        'interactive-map',
    'Products.EEAContentTypes.content.interfaces.IInteractiveData':
                                                        'interactive-data',
    'eea.daviz.subtypes.interfaces.IExhibitJson': 'daviz',
}

class ScaleTraverser(ImageTraverser):
    """ Scale traverser for content types

    Taken from
    https://svn.eionet.europa.eu/projects/Zope/wiki/HowToSpecifyFallbackImages

    eea.imagescales v0.3 introduces the concept of fallback images when
    the regular image traversal fails. The logic works like this:

    * Look for an image returned by the context's 'imgview' adapter
    * If the imgview crashes, isn't found or can not locate/generate an image,
      we continue by checking if there's an image specified for any of the
      contexts interfaces.
    * If there's no fallback image, we look for an image for the context portal
      type, e.g. article, news-item, document. This should be placed in the
      'valentine-imagescales' folder.
    * Uses the generic content type image, i.e. valentine-imagescales/generic

    So:

    * There should be a folder under the site root called 'valentine-imagescales'
    * In that folder there should be an image called 'generic'.
    * To map a fallback image to a portal type, place it in this folder and
      name it after the portal type.
    * To map a fallback image to an interface, edit the dictionary found in
      eea.imagescales.traversal.py
    """

    adapts(IBaseObject, IRequest)

    def fallback(self, request, name):
        """ Fallback
        """

        #because the following methods of getting a thumbnail are not
        #based on real image fields, we'll look for a fake thumbnail
        #only when the name looks like a thumbnail request

        if (not name.startswith('image_')) or (name.startswith('image_view')):
            return DefaultPublishTraverse.publishTraverse(self, request, name)

        context = self.context
        _fieldname, scale = name.split('_', 1)
        if scale and (scale.lower().endswith('.jpg') or
                      scale.lower().endswith('.png')):
            scale = scale[:-4]

        # Regular imgview
        imgview = queryMultiAdapter((context, request), name='imgview')

        # Fallback imgview
        if (imgview == None) or (imgview.display(scale) == False):
            portal = getToolByName(context, 'portal_url').getPortalObject()
            image_obj_id = None
            provided_interfaces = [i.__identifier__
                            for i in providedBy(context).flattened()]
            for k, v in overrides.items():
                if k in provided_interfaces:
                    image_obj_id = v
                    break

            if image_obj_id == None:
                image_obj_id = context.portal_type.replace(' ', '-').lower()

            #This will raise NotFound if no portal['valentine-imagescales']
            image_obj = getattr(portal['valentine-imagescales'],
                                image_obj_id, None)
            if image_obj == None:
                image_obj = portal['valentine-imagescales']['generic']
            imgview = getMultiAdapter((image_obj, request), name='imgview')

        return imgview(scale)
