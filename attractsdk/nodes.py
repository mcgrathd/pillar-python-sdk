from .resource import List
from .resource import Find
from .resource import Create
from .resource import Post
from .resource import Update
from .resource import Delete
from .resource import Replace

from . import utils


class Node(List, Find, Create, Post, Update, Delete, Replace):
    """Node class wrapping the REST nodes endpoint
    """
    path = "nodes"

    def replace_picture(self, picture_file, api=None):
        """Replaces the picture field in the node.
        :param picture_file: A file object
        """
        api = api or self.api
        attributes = self.to_dict()
        etag = attributes['_etag']
        attributes.pop('_id')
        attributes.pop('_etag')
        attributes.pop('_created')
        attributes.pop('_updated')
        attributes.pop('_links')
        if 'parent' in attributes:
            attributes.pop('parent')
        if 'properties' not in attributes:
            attributes['properties'] = {}
        url = utils.join_url(self.path, str(self['_id']))
        headers = utils.merge_dict(
            self.http_headers(),
            {'If-Match': str(etag)})
        files = {'picture': picture_file}
        new_attributes = api.patch(url, attributes, headers, files)
        self.error = None
        self.merge(new_attributes)
        return self.success()


class NodeType(List, Find, Create, Post, Delete):
    """NodeType class wrapping the REST node_types endpoint
    """
    path = "node_types"
