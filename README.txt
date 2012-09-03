=============
EEA Depiction
=============
`EEA Depiction`_ (formerly valentine.imagescales) is a generic system for
creating thumbnails/image representations for content types,
both those provided by Plone, and custom ones. To make it work for a content
type, three adapters need to be provided:

1. ImageView that retrieves an image in the desired scale.
2. ImageTag that returns the HTML tag for the image
3. ImageLink that returns the HTML link to the image.


.. contents::


Installation
============

zc.buildout
-----------
If you are using `zc.buildout`_ and the `plone.recipe.zope2instance`_
recipe to manage your project, you can do this:

* Update your buildout.cfg file:

  * Add ``eea.depiction`` to the list of eggs to install
  * Tell the `plone.recipe.zope2instance`_ recipe to install a ZCML slug

  ::

    [instance]
    ...
    eggs =
      ...
      eea.depiction

    zcml =
      ...
      eea.depiction

* Re-run buildout, e.g. with::

  $ ./bin/buildout

You can skip the ZCML slug if you are going to explicitly include the package
from another package's configure.zcml file.


Dependencies
============

`EEA Depiction`_ has the following dependencies:
  - Plone 4+
  - Pillow
  - p4a.video


Source code
===========

Latest source code (Plone 4 compatible):
  - http://github.com/eea/eea.depiction
  - http://github.com/collective/eea.depiction


Copyright and license
=====================
The Initial Owner of the Original Code is European Environment Agency (EEA).
All Rights Reserved.

The EEA Exhibit (the Original Code) is free software;
you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later
version.

More details under docs/License.txt


Funding
=======

EEA_ - European Environment Agency (EU)

.. _EEA: http://www.eea.europa.eu/
.. _`EEA Depiction`: http://eea.github.com/docs/eea.depiction
.. _`plone.recipe.zope2instance`: http://pypi.python.org/pypi/plone.recipe.zope2instance
.. _`zc.buildout`: http://pypi.python.org/pypi/zc.buildout
