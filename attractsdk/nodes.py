from .resource import List
from .resource import Find
from .resource import Create
from .resource import Post
from .resource import Update
from .resource import Delete
from .resource import Replace

from . import utils
from .api import Api


class Node(List, Find, Create, Post, Update, Delete, Replace):
    """Node class wrapping the REST nodes endpoint
    """
    path = "nodes"

    @classmethod
    def find(cls, resource_id, params=None, api=None):
        """Locate resource, usually using ObjectID

        Usage::

            >>> Node.find("507f1f77bcf86cd799439011")
        """

        api = api or Api.Default()

        url = utils.join_url(cls.path, str(resource_id))
        if params:
            url = utils.join_url_params(url, params)
        return cls(api.get(url))


class NodeType(List, Find, Create, Post, Delete):
    """NodeType class wrapping the REST node_types endpoint
    """
    path = "node_types"
