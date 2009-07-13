from base import ImageLink


class AlbumThumbnailView(ImageLink):

    """Generates thumbnail links designed for atct_album_view."""

    def nothumb(self):
        return self.link('')

    def link(self, imgtag):
        url = self.context.absolute_url()
        title = '<span class="photoAlbumEntryTitle">%s</span>' % self.context.Title()
        return '<a href="%s">%s%s</a>' % (url, imgtag, title)


class FolderThumbnailView(ImageLink):
    
    """Generates thumbnail links designed for folder_summary_view."""

    def link(self, imgtag):
        url = self.context.absolute_url()
        return '<a class="tileImage" href="%s">%s</a>' % (url, imgtag)
