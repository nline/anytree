# -*- coding: utf-8 -*-

from .nodemixin import NodeMixin
from .util import _repr
import random
from shapely import wkt

class Node(NodeMixin, object):

    def __init__(self, name, parent=None, children=None, failrate=0, status=1, pos=None, **kwargs):
        u"""
        A simple tree node with a `name` and any `kwargs`.

        Args:
            name: A name or any other object this node can reference to as idendifier.

        Keyword Args:
            parent: Reference to parent node.
            children: Iterable with child nodes.
            failrate: P(failure) integer between 0 and 100; defaults to 0 if you only want nodes off when you tell them to.
            status: defaults to 1 (on).
            pos: lat/long in WKT format e.g. 'POINT(-58.66 -34.58)'
            *: Any other given attribute is just stored as object attribute.

        Other than :any:`AnyNode` this class has at least the `name` attribute,
        to distinguish between different instances.

        The `parent` attribute refers the parent node:

        >>> from anytree import Node, RenderTree
        >>> root = Node("root")
        >>> s0 = Node("sub0", parent=root)
        >>> s0b = Node("sub0B", parent=s0, foo=4, bar=109)
        >>> s0a = Node("sub0A", parent=s0)
        >>> s1 = Node("sub1", parent=root)
        >>> s1a = Node("sub1A", parent=s1)
        >>> s1b = Node("sub1B", parent=s1, bar=8)
        >>> s1c = Node("sub1C", parent=s1)
        >>> s1ca = Node("sub1Ca", parent=s1c)

        >>> print(RenderTree(root))
        Node('/root')
        ├── Node('/root/sub0')
        │   ├── Node('/root/sub0/sub0B', bar=109, foo=4)
        │   └── Node('/root/sub0/sub0A')
        └── Node('/root/sub1')
            ├── Node('/root/sub1/sub1A')
            ├── Node('/root/sub1/sub1B', bar=8)
            └── Node('/root/sub1/sub1C')
                └── Node('/root/sub1/sub1C/sub1Ca')

        The same tree can be constructed by using the `children` attribute:

        >>> root = Node("root", children=[
        ...     Node("sub0", children=[
        ...         Node("sub0B", bar=109, foo=4),
        ...         Node("sub0A", children=None),
        ...     ]),
        ...     Node("sub1", children=[
        ...         Node("sub1A"),
        ...         Node("sub1B", bar=8, children=[]),
        ...         Node("sub1C", children=[
        ...             Node("sub1Ca"),
        ...         ]),
        ...     ]),
        ... ])

        >>> print(RenderTree(root))
        Node('/root')
        ├── Node('/root/sub0')
        │   ├── Node('/root/sub0/sub0B', bar=109, foo=4)
        │   └── Node('/root/sub0/sub0A')
        └── Node('/root/sub1')
            ├── Node('/root/sub1/sub1A')
            ├── Node('/root/sub1/sub1B', bar=8)
            └── Node('/root/sub1/sub1C')
                └── Node('/root/sub1/sub1C/sub1Ca')

        """
        self.__dict__.update(kwargs)
        self.name = name
        self.parent = parent
        if children:
            self.children = children
        # added failrate (integer between 0 and 100) and status (1/0)
        self.failrate = failrate
        self.status = status
        self.pos = wkt.loads(pos)

    def __repr__(self):
        args = ["%r" % self.separator.join([""] + [str(node.name) for node in self.path])]
        return _repr(self, args=args, nameblacklist=["name"])

    def getstatus(self):
        return self.status

    def setstatus(self, new):
        if (new == 0) or (new == 1):
            self.status = new
            self.refresh()

    def onoff(self):
        randgen = random.seed()
        # if node has parent and parent is off, set node status to off
        if self.parent:
            if not self.parent.getstatus():
                self.status = 0
        # else, use failrate to set node status
        else:
            self.status = 0 if random.randrange(100) < self.failrate else 1

    def setfailrate(self, rate):
        self.failrate = rate

    def refresh(self):
        """
        Propagates OFF's down (sub)tree
        """
        #self.onoff()
        if self.children:
            for child in self.children:
                child.onoff()
                child.refresh()

    def reset(self):
        """
        Sets whole (sub)tree to ON
        """
        self.status = 1
        if self.children:
            for child in self.children:
                child.status = 1
                child.reset()

    def getdistance(self, other):
        """
        Distance from this to another asset
        """
        return self.pos.distance(other.pos)
