Introduction
============

Imagescales is a generic system for creating thumbnails/image representations
for content types, both those provided by Plone, and custom ones. To make it
work for a content type, three adapters need to be provided:

 1. ImageView that retrieves an image in the desired scale.
 2. ImageTag that returns the HTML tag for the image
 3. ImageLink that returns the HTML link to the image.

see valentine/imagescales/README.txt for more info
