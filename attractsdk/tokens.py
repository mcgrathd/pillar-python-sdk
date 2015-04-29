from .resource import List
from .resource import Find
from .resource import Create
from .resource import Post
from .resource import Update
from .resource import Delete


class Token(List, Find, Create, Post, Update, Delete):
    """Token class wrapping the REST tokens endpoint
    """
    path = "tokens"
