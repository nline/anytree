from anytree import Node, RenderTree
import pytest

class TestSetup:
    def __init__(self):
        self.a = Node("a")
        self.b = Node("b", parent=self.a)
        self.c = Node("c", parent=self.b)
        self.d = Node("d", parent=self.b)
        self.e = Node("e", parent=self.a)
        self.f = Node("f", parent=self.e)

@pytest.fixture()
def setup():
    """
    Tree look like this:
    a
    |-- b
    |   |-- c
    |   +-- d
    +-- e
        +-- f

    """
    return TestSetup()

def testGetStatus(setup):
    """
    By default, every node should be ON since we didn't specify fail rate
    """
    for pre, fill, node in RenderTree(setup.a):
        assert node.getstatus() == 1

def testSetStatus(setup):
    """
    Do changes propagate through tree
    """
    setup.a.setstatus(0)
    assert setup.a.getstatus() == 0 
    assert setup.b.getstatus() == 0 
    assert setup.c.getstatus() == 0 
    assert setup.d.getstatus() == 0 
    assert setup.e.getstatus() == 0 
    assert setup.f.getstatus() == 0 


def testSetStatus(setup):
    """
    Does setting b status affect b subtree and ONLY b subtree
    """
    setup.b.setstatus(0)
    for pre, fill, node in RenderTree(setup.b):
        assert node.getstatus() == 0

    # that should only have affected the b subtree
    for pre, fill, node in RenderTree(setup.e):
        assert node.getstatus() == 1

def testOnOff(setup):
    """

    """
    setup.a.onoff()
    assert setup.a.getstatus() == 1

def testReset(setup):
    setup.c.status = 0
    setup.e.status = 0

    setup.a.reset()
    assert setup.a.getstatus() == 1
    assert setup.b.getstatus() == 1
    assert setup.c.getstatus() == 1
    assert setup.d.getstatus() == 1
    assert setup.e.getstatus() == 1
    assert setup.f.getstatus() == 1

def testOnOff2(setup):
    setup.a.status = 0
    setup.b.onoff()
    assert setup.b.getstatus() == 0

def testRefresh(setup):
    setup.b.status = 0
    setup.a.refresh()
    assert setup.c.getstatus() == 0
    assert setup.a.getstatus() == 1
    assert setup.b.getstatus() == 0
