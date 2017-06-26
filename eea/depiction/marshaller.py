""" eea.rdfmarshaller extensions for eea.depiction
"""

from Products.CMFCore.Expression import getExprContext
from Products.CMFCore.utils import getToolByName
from eea.depiction.traverse import ScaleTraverser
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
          <eea:Article rdf:about="http://example.com/articleA">
            <foaf:depiction>
              <schema:Image rdf:about="http://example.com/article-icon.png">
                <rdfs:label>type_icon</rdfs:label>
              </schema:Image>
            </foaf:depiction>
            <foaf:depiction>
              <schema:Image rdf:about="http://example.com/articleA/image">
                <schema:thumbnail
                  rdf:resource="http://example.com/articleA/image_large"/>
                <schema:thumbnail
                  rdf:resource="http://example.com/articleA/image_preview"/>
                <rdfs:label>depiction</rdfs:label>
                <eea:fileInfo
                  rdf:resource="http://example.com/articleA/image#fileInfo"/>
                <schema:contentSize>1234</schema:contentSize>
              </schema:Image>
            </foaf:depiction>
            <article:image rdf:resource="http://example.com/articleA/image"/>
          </eea:Article>
          <schema:Image rdf:about="http://example.com/articleA/image_preview">
            <schema:width>300px</schema:width>
            <schema:height>100px</schema:height>
          </schema:Image>
          <dcat:Distribution
            rdf:about="http://example.com/articleA/image#fileInfo">
            <dcat:downloadURL
              rdf:resource="http://example.com/articleA/at_download/image"/>
            <dcat:sizeInBytes>1234</dcat:sizeInBytes>
          </dcat:Distribution>
          <schema:Image rdf:about="http://example.com/articleA/image_large">
            <schema:width>400px</schema:width>
            <schema:height>200px</schema:height>
          </schema:Image>
        """
        req = self.context.REQUEST

        base_url = self.context.absolute_url()
        img_url = base_url + '/image_large'

        portal_types = getToolByName(self.context, 'portal_types')
        props = getToolByName(
            self.context,
            'portal_properties')['imaging_properties']
        sizes = props.getProperty('allowed_sizes')

        Image = resource.session.get_class(surf.ns.SCHEMA['Image'])

        img = Image(img_url)
        img.rdfs_label = 'depiction'
        # img.eea_fileInfo = img_url + "#fileInfo"

        st = ScaleTraverser(self.context, req)

        blob = st.fallback(req, 'image_large')
        size = blob.get_size()
        img.schema_contentSize = size

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
