## Script (Python) "tag"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpat
##parameters=scale='thumb', height=None, width=None, css_class=None, **kwargs
##title=Tag attribute for items that do not have such an attribute
##

url = context.absolute_url()
src = '%s/image_%s' % (url, scale)
result = '<img src="%s"' % src

if height:
    result = '%s height="%s"' % (result, height)

if width:
    result = '%s width="%s"' % (result, width)

if css_class is not None:
    result = '%s class="%s"' % (result, css_class)

if kwargs:
    items = kwargs.items()
    items.sort()
    for key, value in items:
        if value:
            result = '%s %s="%s"' % (result, key, value)

return '%s />' % result
