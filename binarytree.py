#!usr/bin/python
# coding: utf-8

from disk_operations import Disk

from node import Node



class BinaryTree(object):
    #count = 0 # total nodes in this tree
    # the new node's offset is (self.count)
    def __init__(self, filename):
        self.filename = filename
        self.operate = Disk(filename)
        # if the filename does not exist then create a new one
        # else return the first one 
        if not self.operate.is_file_exists():
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
            self.count = self.operate.get_count()
            #print "already exists %d nodes " % self.count
            self.root = self.operate.read_from_the_beginning_of_disk()
            
        print "count: ", self.count
    # print all the nodes
    def show(self):
        print "root = ",self.root 
        for i in range(1,self.count):
            node = self.operate.read_from_specific_address(i)
            print "node %d = " % i ,
            print node 
    # return the associated node 
    def get(self, k):
        assert type(k) == int
        if self.root == None:
            raise KeyError
        node = self.root
        # find the leaf node 

        # if the root node is a leaf then the while-loop will be passed
        while not node.is_leaf():
            # print "hi"
            print "node = ",node 
            if k > node.key:
                if node.right != -1:
                    node = self.operate.read_from_specific_address(node.right)
                else:
                    raise KeyError
            elif k < node.key:
                if node.left != -1:
                    node = self.operate.read_from_specific_address(node.left)
                else:
                    raise KeyError 
            else:
                if node.valid == 1:
                   return node
                else:
                    raise KeyError
                #return node 
        # the node must be the root 
        if node.key == k and node.valid == 1:
            #return node.value
            return node 
        # test
        #self.show()
        raise KeyError

    def new_delete(self,k):
        try:
            node = self.get(k)
            node.valid = 0

            if node.get_offset() > 0:
                self.operate.store(node)
            else:
                # it is the root node
                self.operate.store_root(node, self.count)

        except KeyError:
            print "node doesn't exist!"
    # delete a node
    # but actually the node is not deleted from disk
    # **** update root's value, don't reserve it for simpilicity
    def delete(self,k):
        # first find the node
        try:
            node = self.get(k)
            # I delete the node from disk, it is wrong but it is simple to implement...need more time
            # One: if the node is a leaf then just remove it 
            # not the root node 
            if node.is_leaf():
                self.delete_leaf(node)
            # Two: if the node has exactly one child, then
            # update its father's child 
            elif node.only_has_left() or node.only_has_right():
                self.delete_two(node)
            # Three: if the node has two children, we can choose to find the minimum 
            # right node of this node, and use it to update this node
            else:
                self.delete_three(node)

        except KeyError as e:
            print "node not found!"
    # One delete
    def delete_leaf(self,node):
        #father_offset = node.father

        father_node = self.operate.read_from_specific_address(node.father)
        if node.relative_position == -1:
            # in the left
            father_node.left = -1
        elif node.relative_position == 1:
            father_node.right = -1
        else:
            raise AttributeError
        # now update father node in the disk
        if father_node.get_offset() > 0:
            self.operate.store(father_node)
        else:
            # it is the root node
            self.operate.store_root(father_node, self.count)
    # Two delete
    def delete_two(self, node):
        # node has left child
        father_node = self.operate.read_from_specific_address(node.father)
        if node.only_has_left():
            update = node.left
        # node has right child 
        elif node.only_has_right():
            update = node.right 
        # update father's children
        if node.relative_position == -1:
            father_node.left = update
        elif node.relative_position == 1:
            father_node.right = update
        else:
            print "wrong"
        # now update father node in the disk
        if father_node.get_offset() > 0:
            self.operate.store(father_node)
        else:
            # it is the root node
            self.operate.store_root(father_node, self.count)
    # Three delete: find the minimum node in its right
    def delete_three(self, node):
        changed_node = []
        min_node = self.find_right_min(node)
        father_of_min_node = self.operate.read_from_specific_address(min_node.father)
        father_of_node = self.operate.read_from_specific_address(node.father)
        if node.is_root():
            # update its value
            if min_node.father == 0:
                node.right = min_node.right
                node.value = min_node.value
                #changed_node.push(node)
                if min_node.right != -1:
                    min_node_child = self.operate.read_from_specific_address(min_node.right)
                    min_node_child.father = 0
                    changed_node.push(min_node_child)
            else:
                node.value = min_node.value 
                if min_node.relative_position == -1:
                    father_of_min_node.left = -1
                else:
                    father_of_min_node.right = -1 
        else:
            # update min_node's father
            if min_node.relative_position == -1:
                father_of_min_node.left = -1
            else:
                father_of_min_node.right = -1 
            # update node's father
            if node.relative_position == -1:
                father_of_node.left = min_node.offset 
            else:
                father_of_node.right = min_node.offset 
            # update node
            min_node.left = node.left
            min_node.right = node.right 
            min_node.father = node.father 
        # not finished 


        # father_of_min_node may be this very node

        # step one: update father_of_min_node
        # if min_node.relative_position == -1:
        #     father_of_min_node.left = -1
        # elif min_node.relative_position == 1:
        #     father_of_min_node.right = 1

        # if father_node.get_offset() > 0:
        #     store(father_node, self.filename)
        # else:
        #     # it is the root node
        #     store_root(father_node, self.count, self.filename)

    # find the minimum node in its right
    def find_right_min(self, node):
        assert node.right > 0
        first_node = self.operate.read_from_specific_address(node.right)
        # if first node has no left child, then it is the smallest
        if first_node.left == -1:
            return first_node
        else:
            # run along the left
            while first_node.left != -1:
                first_node = self.operate.read_from_specific_address(first_node.left)
            return first_node 


    # insert (k,v) if it does not exist
    # else doesn't change anything    
    def set(self,k,v):
        assert type(k) == int and type(v) == int 
        node  =  self.root  # the current node
        print "in set, count = ",self.count
        # if (k,v) is the first pair
        if self.root == None:
            new_node = Node(0,k,v,-1,-1,father=-1)
            self.root = new_node
            self.count += 1 # now we have the first node 
            self.operate.store_root(self.root, 1)
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
                        node = self.operate.read_from_specific_address(node.right)
                    else: # insert it here
                        #print "start to insert a new node"
                        offset = self.count
                        new_node = Node(offset,k,v,-1,-1,father=node.offset,relative_position=1)
                        node.right = offset
                        #print "node = ", node 
                        
                        #print "root before stored = ",
                        #print self.root
                        # node is modified so we re-write it into disk
                        # if the node is root ?
                        if node.offset == 0:
                            self.operate.store_root(node, self.count+1) # already store the count
                        else:
                            self.operate.store(node) # not root 
                            self.operate.store_count(self.count+1) 
                        
                        self.operate.store(new_node)
                        
                        #print "root after ", 
                        #print self.root
                        #print read_from_the_beginning_of_disk(self.filename)
                        #print "Insert a new node :",
                        #print new_node

                        break
                elif node.key > k:
                    print "****** left ******"
                    if node.left != -1:
                        node = self.operate.read_from_specific_address(node.left)
                    else:
                        # insert
                        offset = self.count
                        new_node = Node(offset,k,v,-1,-1,father=node.offset,relative_position=-1)
                        node.left = offset
                        self.count += 1
                        # node is modified so we re-write it into disk
                        if node.offset == 0:
                            self.operate.store_root(node, self.count)
                        else:
                            self.operate.store(node)
                            self.operate.store_count(self.count)

                        self.operate.store(new_node)
                        #print "Insert a new node :",
                        #print new_node
                        break
                else:
                    # k is the same and this node is deleted 
                    if node.valid == 0:
                        node.valid = 1
                        node.set_value(v)
                        if node.get_offset() > 0:
                            self.operate.store(node)
                        else:
                            # it is the root node
                            self.operate.store_root(node, self.count)
                    # the node is not deleted
                    elif node.valid == 1 and node.value != v:
                        node.set_value(v)

                        if node.get_offset() > 0:
                            self.operate.store(node)
                        else:
                            # it is the root node
                            self.operate.store_root(node, self.count)
                    break




    