## Script (Python) "atctListAlbum"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=images=0, folders=0, subimages=0, others=0
##title=Helper method for photo album view
##
result = {}
is_topic = context.portal_type == 'Topic'

# customized python script to return all results as part of the images result
if images:
    if is_topic:
        result['images'] = context.queryCatalog(full_objects=True)
    else:
        result['images'] = context.getFolderContents(full_objects=True)

if folders:
    # We don't need the folders since they will be listed with the images
    result['folders'] = ()

if subimages:
    # Handle brains or objects
    if getattr(context, 'getPath', None) is not None:
        path = context.getPath()
    else:
        path = '/'.join(context.getPhysicalPath())
    # Explicitly set path to remove default depth
    if is_topic:
        result['subimages'] = context.queryCatalog(path=path)
    else:
        result['subimages'] = context.getFolderContents({'path': path})

if others:
    # We don't to fill in this since every item be listed with the images
        result['others'] = ()

return result

