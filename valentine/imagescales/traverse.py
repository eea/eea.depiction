from zope.component import adapts, queryMultiAdapter, getMultiAdapter
from zope.interface import implements
from zope.app.traversing.interfaces import ITraversable
from Products.Five.traversable import FiveTraversable


class ScaleTraverser(FiveTraversable):

    implements(ITraversable)

    def traverse(self, name, furtherPath):
        if not 'image_' in name:
            return super(ScaleTraverser, self).traverse(name, furtherPath)
        context = self._subject
        request = context.REQUEST
        fieldname, scalename = name.split('_', 1)
        scaleview = getMultiAdapter((context, request), name='imgview')
        if scalename.endswith('.jpg') or scalename.endswith('.png'):
            scalename = scalename[:-4]
        return scaleview(scalename)
