""" Utilities
"""
import logging
import transaction
from zope.component import queryMultiAdapter, queryUtility
from zope.schema.interfaces import IVocabularyFactory
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from eea.depiction.async import IAsyncService
logger = logging.getLogger('eea.depiction')


def recreate_scales(obj, fieldname='image'):
    """ recreate_scales
    """
    field = obj.getField(fieldname)
    if not field:
        raise AttributeError(fieldname)
    field.removeScales(obj)
    field.createScales(obj)


class RecreateImageScales(BrowserView):
    """ Recreate image scales """

    def __call__(self, **kwargs):
        form = getattr(self.request, 'form', None) or {}
        kwargs.update(form)
        fieldname = kwargs.get('field', 'image')

        url = self.context.absolute_url()
        try:
            recreate_scales(self.context, fieldname)
        except AttributeError:
            msg = 'ERROR: no "%s" field found for %s' % (fieldname, url)
        else:
            msg = 'Done'

        logger.info(msg)
        return msg


class RecreateDepictionScales(BrowserView):
    """ Recreate image scales for all content-types
    """

    def _redirect(self, msg='', to='recreate-scales'):
        """ Return or redirect
        """
        logger.info(msg)

        if not to:
            return msg

        if not self.request:
            return msg

        if msg:
            IStatusMessage(self.request).addStatusMessage(
                str(msg), type='info')
        self.request.response.redirect(to)
        return msg

    def _rescale(self, form):
        """ Run rescale
        """
        types = form.get('types', ())
        if not types:
            msg = 'You have to select at least one Portal type to rescale'
            return self._redirect(msg)
        fieldname = form.get('fieldname', 'image')

        ctool = getToolByName(self.context, 'portal_catalog')
        brains = ctool(portal_type=types, Language='all')

        length = len(brains)
        logger.info("Recreating scales for %s documents."
                    "Selected Types: %s", length, ', '.join(types))

        count = 0
        for brain in brains:
            doc = brain.getObject()

            # Recreate scales asynchronously via zc.async
            async_service = queryUtility(IAsyncService)
            if async_service:
                async_queue = async_service.getQueues()['']
                async_service.queueJobInQueue(
                    async_queue, ('depiction',),
                    recreate_scales,
                    doc,
                    fieldname
                )
                continue

            rescale = queryMultiAdapter((doc, self.request),
                name=u'recreate-scales')
            rescale()

            count += 1
            if count % 25 == 0:
                logger.info('Transaction commit: %s', count)
                transaction.commit()

        msg = 'Rescale complete. Check the Zope log for more details.'
        return self._redirect(msg)

    @property
    def content_types(self):
        """ Return Content-Types to rescale
        """
        vocab = queryUtility(IVocabularyFactory,
            'plone.app.vocabularies.UserFriendlyTypes')
        for term in vocab(self.context):
            yield term

    def __call__(self, **kwargs):
        if self.request:
            kwargs.update(self.request.form)

        submitting = kwargs.get('action.submit', None)
        if not submitting:
            return self.index()
        return self._rescale(kwargs)
