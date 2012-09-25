""" Upgrade steps to version 5.0
"""
from eea.depiction.setuphandlers import setupDefaultImages

def migrateOldImages(context):
    """ Migrate old images
    """
    site = context.portal_url.getPortalObject()
    return setupDefaultImages(site)
