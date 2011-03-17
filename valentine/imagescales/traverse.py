from zope.component import adapts, queryMultiAdapter, getMultiAdapter
from zope.interface import implements
from zope.interface import providedBy
from zope.app.traversing.interfaces import ITraversable
from Products.CMFCore.utils import getToolByName
from Products.Five.traversable import FiveTraversable


# In some cases we want to fallback on a different image than the one used
# for the portal type. In this dictionary we can specify images that should
# be used if the context provides a certain interface. TODO: move to vocabulary
# outside valentine.imagescales.
overrides = {
    'Products.EEAContentTypes.content.interfaces.IInteractiveMap': 'interactive-map',
    'Products.EEAContentTypes.content.interfaces.IInteractiveData': 'interactive-data',
}

import logging
logger = logging.getLogger("valentine.imagescales")

class ScaleTraverser(FiveTraversable):

    """ https://svn.eionet.europa.eu/projects/Zope/wiki/HowtoSpecifyFallbackImages """

    implements(ITraversable)

    def traverse(self, name, furtherPath):
        context = self._subject

        #logger.info("Doing traverse from v.i on %s  with name %s" % (context, name))
        
        if name == "image":
            field = context.getField('image')
            res = field.get(context)
            return res

        if not 'image_' in name:
            return super(ScaleTraverser, self).traverse(name, furtherPath)

        request = context.REQUEST
        fieldname, scalename = name.split('_', 1)
        if scalename.endswith('.jpg') or scalename.endswith('.png'):
            scalename = scalename[:-4]

        # Regular imgview
        imgview = queryMultiAdapter((context, request), name='imgview')

        # Fallback imgview
        if (imgview == None) or (imgview.display(scalename) == False):
            portal = getToolByName(context, 'portal_url').getPortalObject()
            image_obj_id = None
            provided_interfaces = [i.__identifier__ for i in providedBy(context).flattened()]
            for k, v in overrides.items():
                if k in provided_interfaces:
                    image_obj_id = v
                    break
            if image_obj_id == None:
                image_obj_id = context.portal_type.replace(' ', '-').lower()
            image_obj = getattr(portal['valentine-imagescales'], image_obj_id, None)
            if image_obj == None:
                image_obj = portal['valentine-imagescales']['generic']
            imgview = getMultiAdapter((image_obj, request), name='imgview')

        return imgview(scalename)
