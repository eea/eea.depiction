""" EEA Depiction package
"""
def initialize(context):
    """ Zope 2 """
    from eea.depiction import content
    content.initialize(context)
