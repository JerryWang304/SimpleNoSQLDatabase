#!usr/bin/python
# coding: utf-8
from binarytree import BinaryTree
class Database(object):
    def __init__(self, filename):
        self.file = filename
        self.tree = BinaryTree(filename)

    #set a (key, value)
    #(key, value) may already exists in the database
    # actually insert it into the tree
    # won'y commit yet
    def set(self,k,v):
        self.tree.set(k,v)
    # def commit():
    #     self.tree.store_to_disk()

    

