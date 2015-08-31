from .resource import List
from .resource import Find
from .resource import Create
from .resource import Post
from .resource import Update
from .resource import Delete


class Group(List, Find, Create, Post, Update, Delete):
    """Group class wrapping the REST nodes endpoint
    """
    path = "groups"
