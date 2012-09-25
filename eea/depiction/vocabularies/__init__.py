""" Vocabularies
"""
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from eea.depiction.vocabularies.interfaces import IDepictionVocabulary

INTERFACES = {
    'Products.EEAContentTypes.content.interfaces.IInteractiveMap':
        'interactive-map',
    'Products.EEAContentTypes.content.interfaces.IInteractiveData':
        'interactive-data',
    'eea.app.visualization.subtypes.interfaces.IVisualizationEnabled':
        'daviz',
}

class DepictionVocabulary(object):
    """ Fallback images for eea context interfaces
    """

    implements(IDepictionVocabulary)

    def __call__(self, context):
        items = [SimpleTerm(key, key, value)
                 for key, value in INTERFACES.items()]
        return SimpleVocabulary(items)
