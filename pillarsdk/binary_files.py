from .resource import List
from .resource import Find
from .resource import Create
from .resource import Post
from .resource import Update
from .resource import Delete
from .resource import Replace

from . import utils


class binaryFile(List, Find, Create, Post, Update, Delete, Replace):
    """binaryFile class wrapping the REST binary_files endpoint
    """
    path = "binary_files"

    def post_file(self, file_,  api=None):
        """Stores a file on the database or static folder.
        :param file: A file object
        """
        api = api or self.api
        url = utils.join_url(self.path)
        files = {'data': file_}
        new_attributes = api.post(url, {}, {}, files)
        # self.error = None
        self.merge(new_attributes)
        return self.success()
