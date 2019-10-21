""" Public Depiction Interfaces
"""
from eea.depiction.content.interfaces import IDepictionTool
from eea.depiction.vocabularies.interfaces import IDepictionVocabulary
from eea.depiction.browser.interfaces import IRecreateScales

__all__ = (
    IDepictionTool.__name__,
    IDepictionVocabulary.__name__,
    IRecreateScales.__name__,
)
