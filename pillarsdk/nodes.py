from .resource import List
from .resource import Find
from .resource import Create
from .resource import Post
from .resource import Update
from .resource import Delete
from .resource import Replace
from .exceptions import ResourceNotFound

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

    @classmethod
    def find_one(cls, params, api=None):
        """Get one resource starting from parameters different than the resource
        id. TODO if more than one match for the query is found, raise exception.
        """
        api = api or Api.Default()

        # Force delivery of only 1 result
        params['max_results'] = 1
        url = utils.join_url_params(cls.path, params)

        response = api.get(url)
        # Keep the response a dictionary, and cast it later into an object.
        if response['_items']:
            return cls(response['_items'][0])
        else:
            raise ResourceNotFound(response)


    def update(self, attributes=None, api=None):
        api = api or self.api
        attributes = attributes or self.to_dict()
        etag = attributes['_etag']
        attributes.pop('_id')
        attributes.pop('_etag')
        attributes.pop('_created')
        attributes.pop('_updated')
        attributes.pop('_links')
        attributes.pop('allowed_methods')
        url = utils.join_url(self.path, str(self['_id']))
        headers = utils.merge_dict(
            self.http_headers(),
            {'If-Match': str(etag)})
        new_attributes = api.put(url, attributes, headers)
        self.error = None
        self.merge(new_attributes)
        return self.success()

    def has_method(self, method):
        if method in self.allowed_methods:
            return True
        return False


class NodeType(List, Find, Create, Post, Delete):
    """NodeType class wrapping the REST node_types endpoint
    """
    path = "node_types"
