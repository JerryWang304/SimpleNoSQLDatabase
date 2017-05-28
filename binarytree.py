#!usr/bin/python
# coding: utf-8

from disk_operations import *

from node import Node



class BinaryTree(object):
    #count = 0 # total nodes in this tree
    # the new node's offset is (self.count)
    def __init__(self, filename):
        self.filename = filename
        # if the filename does not exist then create a new one
        # else return the first one 
        if not is_file_exists(self.filename):
            self.root = None # note that the disk is still empty
            #self.count += 1
            self.count = 0
            # create the file
            f = open(filename,'wb')
            f.close()
            #print "already exists %d nodes " % self.count
        else:
            # read from disk
            #with open(filename,'rb') as f:
            self.count = get_count(self.filename)
            #print "already exists %d nodes " % self.count
            self.root = read_from_the_beginning_of_disk(self.filename)
            
        #print "root: ", self.root
    # return the associated value 
    def get(self, k):
        assert type(k) == int
        if self.root == None:
            raise KeyError
        node = self.root
        # find the leaf node 
        # if the root node is a leaf then the while-loop will be passed
        while not node.is_leaf():
            # print "hi"
            if k > node.key:
                if node.right != -1:
                    node = read_from_specific_address(node.right, self.filename)
            elif k < node.key:
                if node.left != -1:
                    node = read_from_specific_address(node.left, self.filename)
            else:
                if node.valid == 1:
                    return node.value 
        # the node must be the root 
        if node.key == k and node.valid == 1:
            return node.value
        
        raise KeyError

    # delete a node
    # but actually the node is not deleted from disk
    def delete(self,k):
        # first find the node
        try:
            node = self.get(k)
            node.valid = 0
            # save this node to disk 

        except KeyError as e:
            print "node not found!"

    # insert (k,v) if it does not exist
    # else doesn't change anything    
    def set(self,k,v):
        assert type(k) == int and type(v) == int 
        node  =  self.root  # the current node
        
        # if (k,v) is the first pair
        if self.root == None:
            new_node = Node(0,k,v,-1,-1)
            self.root = new_node
            self.count += 1 # now we have the first node 
            store_root(self.root, 1,  self.filename)
            print "new root = ",
            print self.root
            #store_count(self.count, self.filename)
        #elif self.root
        else:
            # now we should do binary search
            while True:
                print "k = ",k
                print "node.key = ",node.key
                # k is str !!!
                #if k> node.key: 
                #    print "{%d} > {%d}" % (int(k),int(node.key))
                print "current node to compare :", node 
                if k > node.key:
                    print "****** right ******"
                    if node.right != -1:
                        print "move further (right)"
                        node = read_from_specific_address(node.right, self.filename)
                    else: # insert it here
                        #print "start to insert a new node"
                        offset = self.count
                        new_node = Node(offset,k,v,-1,-1)
                        node.right = offset
                        #print "node = ", node 
                        
                        #print "root before stored = ",
                        #print self.root
                        # node is modified so we re-write it into disk
                        # if the node is root ?
                        if node.offset == 0:
                            store_root(node, self.count+1, self.filename) # already store the count
                        else:
                            store(node, self.filename) # not root 
                            store_count(self.count+1, self.filename) 
                        
                        store(new_node, self.filename)
                        
                        #print "root after ", 
                        #print self.root
                        #print read_from_the_beginning_of_disk(self.filename)
                        #print "Insert a new node :",
                        #print new_node

                        break
                elif node.key > k:
                    print "****** left ******"
                    if node.left != -1:
                        node = read_from_specific_address(node.left, self.filename)
                    else:
                        # insert
                        offset = self.count
                        new_node = Node(offset,k,v,-1,-1)
                        node.left = offset
                        self.count += 1
                        # node is modified so we re-write it into disk
                        if node.offset == 0:
                            store_root(node, self.count, self.filename)
                        else:
                            store(node, self.filename)
                            store_count(self.count, self.filename)

                        store(new_node, self.filename)
                        #print "Insert a new node :",
                        #print new_node
                        break
                else:
                    # k is the same
                    if node.value != v:
                        node.set_value(v)
                        if node.get_offset() > 0:
                            store(node, self.filename)
                        else:
                            # it is the root node
                            store_root(node, self.count, self.filename)
                    break




    