from resource import List
from resource import Find
from resource import Create
from resource import Post
from resource import Update
from resource import Delete


class Node(List, Find, Create, Post, Update, Delete):
    """Node class wrapping the REST nodes endpoint
    """
    path = "nodes"


class NodeType(List, Find, Create, Post, Delete):
    """NodeType class wrapping the REST node_types endpoint
    """
    path = "node_types"
