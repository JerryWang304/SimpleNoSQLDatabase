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
    def get(self,k):
        try:
            node = self.tree.get(k)
            #print self.tree.find_right_min(node)
            print "value = ", node.get_value()

        except KeyError as e:
            print "node not found !"
    def delete(self,k):
        self.tree.delete(k)
        

    

