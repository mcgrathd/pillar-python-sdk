from .resource import List
from .resource import Find
from .resource import Create
from .resource import Post
from .resource import Update
from .resource import Delete
from .resource import Replace

from . import utils

class File(List, Find, Create, Post, Update, Delete, Replace):
    """Node class wrapping the REST nodes endpoint
    """
    path = "files"
    file_server_path = "file_server/file"
    build_previews_server_path = "file_server/build_previews"

    def post_file(self, file_path, name=None, api=None):
        """Stores a file on the database or static folder.
        :param file: A file object
        """
        api = api or self.api
        url = utils.join_url(self.file_server_path)
        file_ = open(file_path, 'rb')
        files = {'data': file_}
        api.post(url, {"name": name}, {}, files)
        file_.close()
        # self.error = None
        # self.merge(new_attributes)
        return self.success()

    def build_previews(self, path, api=None):
        """Stores a file on the database or static folder.
        :param path: A file path
        """
        api = api or self.api
        url = utils.join_url(self.build_previews_server_path, path)
        api.get(url)
        return self.success()

    def children(self, api=None):
        """Collect children (variations) of the current file. Used to connect
        different resolutions of the same picture, or multiple versions of the
        same video in different formats/containers.

        TODO: add params to support pagination.
        """
        api = api or self.api
        files = self.all({'where': '{"parent": "%s"}' % self._id}, api=api)
        print files._items
        if not files._items:
            return None
        return files
