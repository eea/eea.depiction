""" Utilities
"""
import logging
import transaction
from zope.component import queryMultiAdapter, queryUtility
from zope.schema.interfaces import IVocabularyFactory
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
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

    def _migrate(self, form):
        """ Run rescale
        """
        types = form.get('types', ())
        if not types:
            msg = 'You have to select at least one Portal type to rescale'
            return self._redirect(msg)

        ctool = getToolByName(self.context, 'portal_catalog')
        brains = ctool(portal_type=types, Language='all')

        length = len(brains)
        logger.info("Recreating scales for %s documents."
                    "Selected Types: %s", length, ', '.join(types))

        count = 0
        for brain in brains:
            doc = brain.getObject()
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
        for term in vocab:
            yield term

    def __call__(self, **kwargs):
        if self.request:
            kwargs.update(self.request.form)

        submitting = kwargs.get('action.submit', None)
        if not submitting:
            return self.index()
        return self._migrate(kwargs)
