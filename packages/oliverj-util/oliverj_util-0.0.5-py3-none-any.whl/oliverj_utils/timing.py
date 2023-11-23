import time


class Tree:
    def __init__(self):
        self.nodes = {}
        self.stack = []

    def add_node(self, node):
        self.nodes[node.func_name] = node

    def stack_add(self, data):
        self.stack.append(data)

    def stack_remove(self):
        self.stack.pop()


class Node:
    time: list = []

    def __init__(self, func_name: str = ""):
        self.func_name = func_name
        self.count = 0
        self.time = []
        self.parents = []
        self.children = []

    def __repr__(self):
        return str(self.func_name)

    def add_parent(self, parent):
        self.parents.append(parent)

    def add_child(self, child):
        self.children.append(child)

    def add_time(self, time: float):
        self.time.append(time)


class Timing():
    def __init__(self, tree: Tree = Tree()):
        self.tree = tree
        self.tree.stack_add(Node())

    def time(self, func):
        def wrapper(*args, **kwargs):
            node = Node(func.__name__)
            if func.__name__ in self.tree.nodes.keys():
                node = self.tree.nodes[func.__name__]
            node.add_parent(self.tree.stack[-1])
            self.tree.stack_add(node)
            begin = time.time_ns() / 1_000_000
            ret = func(*args, **kwargs)
            end = time.time_ns() / 1_000_000
            node.add_time(end-begin)
            if func.__name__ not in self.tree.nodes.keys():
                self.tree.add_node(node)
            self.tree.stack_remove()
            return ret
        return wrapper
