__author__ = 'Akshay'


class Node:
    initial_time = 0
    finish_time = 0
    name = None
    child_nodes = None
    parent_nodes = None
    conditional_probability_table = {}

    def __init__(self, nm):
        self.name = nm
        self.parent_distance = 0
        self.child_nodes = []
        self.parent_nodes = []

    def add_child(self, node=None, weight=None):
        self.child_nodes.append((node, weight))
        node.parent_nodes.append(self)

    def has_child(self, node=None):
        return node in self.child_nodes

