import uuid

from . import utils
from .api import Api


class Resource(object):
    """Base class for all REST services
    """
    convert_resources = {}

    def __init__(self, attributes=None):
        attributes = attributes or {}
        self.__dict__['api'] = Api.Default()

        super(Resource, self).__setattr__('__data__', {})
        super(Resource, self).__setattr__('error', None)
        super(Resource, self).__setattr__('headers', {})
        super(Resource, self).__setattr__('header', {})
        super(Resource, self).__setattr__('request_id', None)
        self.merge(attributes)

    def generate_request_id(self):
        """Generate unique request id
        """
        if self.request_id is None:
            self.request_id = str(uuid.uuid4())
        return self.request_id

    def http_headers(self):
        """Generate HTTP header
        """
        return utils.merge_dict(self.header, self.headers,
            {'Attract-Request-Id': self.generate_request_id()})

    def __str__(self):
        return self.__data__.__str__()

    def __repr__(self):
        return self.__data__.__str__()

    def __getattr__(self, name):
        return self.__data__.get(name)

    def __setattr__(self, name, value):
        try:
            # Handle attributes(error, header, request_id)
            super(Resource, self).__getattribute__(name)
            super(Resource, self).__setattr__(name, value)
        except AttributeError:
            self.__data__[name] = self.convert(name, value)

    def success(self):
        return self.error is None

    def merge(self, new_attributes):
        """Merge new attributes e.g. response from a post to Resource
        """
        for key, val in new_attributes.items():
            setattr(self, key, val)

    def convert(self, name, value):
        """Convert the attribute values to configured class
        """
        if isinstance(value, dict):
            cls = self.convert_resources.get(name, Resource)
            return cls(value)
        elif isinstance(value, list):
            new_list = []
            for obj in value:
                new_list.append(self.convert(name, obj))
            return new_list
        else:
            return value

    def __getitem__(self, key):
        return self.__data__[key]

    def __setitem__(self, key, value):
        self.__data__[key] = self.convert(key, value)

    def to_dict(self):

        def parse_object(value):
            if isinstance(value, Resource):
                return value.to_dict()
            elif isinstance(value, list):
                new_list = []
                for obj in value:
                    new_list.append(parse_object(obj))
                return new_list
            else:
                return value

        data = {}
        for key in self.__data__:
            data[key] = parse_object(self.__data__[key])
        return data


class Find(Resource):

    @classmethod
    def find(cls, resource_id, api=None):
        """Locate resource, usually using ObjectID

        Usage::

            >>> Node.find("507f1f77bcf86cd799439011")
        """

        api = api or Api.Default()

        url = utils.join_url(cls.path, str(resource_id))
        return cls(api.get(url))


class List(Resource):

    list_class = Resource

    @classmethod
    def all(cls, params=None, api=None):
        """Get list of resources, allowing some parameters such as:
        - count
        - start_time
        - sort_by
        - sort_order

        Usage::

            >>> shots = Nodes.all({'count': 2, 'type': 'shot'})
        """
        api = api or Api.Default()

        if params is None:
            url = cls.path
        else:
            url = utils.join_url_params(cls.path, params)

        try:
            response = api.get(url)
            return cls.list_class(response)
        except AttributeError:
            # To handle the case when response is JSON Array
            if isinstance(response, list):
                new_resp = [cls.list_class(elem) for elem in response]
                return new_resp


class Create(Resource):

    def create(self):
        """Create a resource

        Usage::

            >>> node = Node({})
            >>> node.create()
        """

        headers = self.http_headers()

        new_attributes = self.api.post(self.path, self.to_dict(), headers)
        self.error = None
        self.merge(new_attributes)
        return self.success()


class Update(Resource):
    """Update a resource
    """

    def update(self, attributes=None, api=None):
        api = api or self.api
        attributes = attributes or self.to_dict()
        etag = attributes['_etag']
        attributes.pop('_id')
        attributes.pop('_etag')
        attributes.pop('_created')
        attributes.pop('_updated')
        attributes.pop('_links')
        if 'parent' in attributes:
            attributes.pop('parent')
        url = utils.join_url(self.path, str(self['_id']))
        headers = utils.merge_dict(
            self.http_headers(),
            {'If-Match': str(etag)})
        new_attributes = api.put(url, attributes, headers)
        self.error = None
        self.merge(new_attributes)
        return self.success()


class Replace(Resource):
    """Partial update or modify resource
    see http://williamdurand.fr/2014/02/14/please-do-not-patch-like-an-idiot/

    Usage::

        >>> node = Node.find("507f1f77bcf86cd799439011")
        >>> node.replace([{'op': 'replace', 'path': '/name', 'value': 'Renamed Shot 2' }])
    """

    def replace(self, attributes=None):
        attributes = attributes or self.to_dict()
        url = utils.join_url(self.path, str(self['id']))
        new_attributes = self.api.patch(url, attributes, self.http_headers())
        self.error = None
        self.merge(new_attributes)
        return self.success()


class Delete(Resource):

    def delete(self, api=None):
        """Delete a resource

        Usage::

            >>> node = Node.find("507f1f77bcf86cd799439011")
            >>> node.delete()
        """
        api = api or self.api
        url = utils.join_url(self.path, str(self['_id']))
        etag = self['_etag']
        headers = {'If-Match': str(etag)}
        new_attributes = api.delete(url, headers)
        self.error = None
        self.merge(new_attributes)
        return self.success()


class Post(Resource):

    def post(self, attributes=None, api=None):
        """Constructs url with passed in headers and makes post request via
        post method in api class.
        """
        api = api or self.api
        attributes = attributes or {}
        url = utils.join_url(self.path)
        """if not isinstance(attributes, Resource):
            attributes = Resource(attributes, api=self.api)"""
        new_attributes = api.post(url, attributes, {})
        """if isinstance(cls, Resource):
            cls.error = None
            cls.merge(new_attributes)
            return self.success()
        else:
            return cls(new_attributes, api=self.api)"""
        return self.success()
