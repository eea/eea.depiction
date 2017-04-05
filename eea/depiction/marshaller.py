""" eea.rdfmarshaller extensions for eea.depiction
"""

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.Expression import getExprContext
from eea.rdfmarshaller.interfaces import ISurfResourceModifier
from zope.interface import implements
import surf


class Depiction2SurfModifier(object):
    """Modifier for content types that want to publish info about
    their file mimetypes
    """

    implements(ISurfResourceModifier)

    def __init__(self, context):
        self.context = context

    def run(self, resource, *args, **kwds):
        """change the rdf resource

        We implement this type of output:
        <eea:Indicator rdf:about="http://example.com/indicatorA">
          <foaf:depiction>
            <schema:Image rdf:about="http://example.com/indicator-icon.png">
              <rdfs:label>type_icon</rdfs:label>
            </schema:Image>
          </foaf:depiction>
          <foaf:depiction>
            <schema:Image rdf:about="http://example.com/portal/example">
              <rdfs:label>depiction</rdfs:label>
              <schema:thumbnail
                rdf:resource="http://example.com/something/image_large"/>
              <schema:thumbnail
                rdf:resource="http://example.com/something-else/image_large"/>
            </schema:Image>
          </foaf:depiction>
        </eea:Indicator>
        <schema:Image rdf:about="http://example.com/something/image_large">
          <schema:width>400px</schema:width>
          <schema:height>200px</schema:height>
        </schema:Image>
        <schema:Image
          rdf:about="http://example.com/something-else/image_large">
          <schema:width>400px</schema:width>
          <schema:height>200px</schema:height>
        </schema:Image>
        """

        portal_types = getToolByName(self.context, 'portal_types')
        props = getToolByName(
            self.context,
            'portal_properties')['imaging_properties']
        sizes = props.getProperty('allowed_sizes')

        Image = resource.session.get_class(surf.ns.SCHEMA['Image'])

        img = Image(self.context.absolute_url() + '/image')
        img.rdfs_label = 'depiction'

        icon = None
        fti = portal_types[self.context.portal_type]

        if fti.icon_expr:
            iconexpr = fti.icon_expr_object
            ec = getExprContext(self.context)
            icon_url = iconexpr(ec)
            icon = Image(icon_url)
            icon.rdfs_label = 'type_icon'
            icon.update()

        img.schema_thumbnail = []

        for size in sizes:
            name, info = size.split(' ')
            w, h = info.split(':')

            t = Image(self.context.absolute_url() + '/image_' + name)
            t.schema_width = str(w) + 'px'
            t.schema_height = str(h) + 'px'
            t.update()

            img.schema_thumbnail.append(t)

        img.update()

        if icon is not None:
            resource.foaf_depiction = [img, icon]
        else:
            resource.foaf_depiction = [img]

        resource.update()
        resource.save()
