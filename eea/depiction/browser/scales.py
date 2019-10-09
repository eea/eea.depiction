""" Utilities
"""
import logging
from Products.Five.browser import BrowserView
logger = logging.getLogger('eea.depiction')


class RecreateImageScales(BrowserView):
    """ Recreate image scales """

    def __call__(self, **kwargs):
        form = getattr(self.request, 'form', None) or {}
        kwargs.update(form)
        fieldname = kwargs.get('field', 'image')

        getField = getattr(self.context, 'getField', lambda x: None)
        field = getField(fieldname)

        url = self.context.absolute_url()
        if field is not None:
            logger.info('INFO: updating scales for %s', url)
            field.removeScales(self.context)
            field.createScales(self.context)
            msg = 'Done'
        else:
            msg = 'ERROR: no "%s" field found for %s' % (fieldname, url)

        logger.info(msg)
        return msg
