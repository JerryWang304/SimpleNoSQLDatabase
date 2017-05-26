#!usr/bin/python
# coding: utf-8
import os
import struct
try: 
    import cPickle as pickle 
except:
    import pickle

class Node(object):
    # the block is offset-th 4KB block
    def __init__(self,offset,k,v,left,right):
        self.offset = offset     # in which block ?
        self.key = k        # key stored in the node
        self.value = v      # value stored in the node
        self.left = left    # integer type: the offset of left node
        self.right = right  # integer type
    # formated string
    def __str__(self):
        ret  = ''
        return 'Node(' + "location: "+str(self.offset) + ', key: '+ str(self.key) + ', value: '\
            + str(self.value) + ', left: ' + str(self.left) + ', right: ' + str(self.right) \
            + ')'
    # change key
    def set_key(self,k):
        self.key = k
    # change value
    def set_value(self,v):
        self.value = v
    # change left
    def set_left(self,left):
        self.left = left
    # change right
    def set_right(self,right):
        self.right = right
    # get address
    def get_offset(self):
        return self.offset 
    # is leaf ?
    def is_leaf(self):
        return self.left == -1 and self.right == -1
    # write to disk
def store(node, filename):
    # if node.get_offset() == 0:
    #     store_root(node,count,filename)
    #     return 
    with open(filename, 'rb+') as f:
        f.seek(BLOCK_SIZE*node.offset)
        data = convert_node_to_string(node)
        length_of_data = len(data)
        packed = convert_integer_to_bytes(length_of_data)
        f.write(packed)
        f.write(data)

        size = f.tell() # current location of file (bytes)
        # print "file size = %d bytes" % size 
        if size % BLOCK_SIZE != 0:
            print "padding bits in normal nodes"
            f.write(b"\x00"*(BLOCK_SIZE - size%BLOCK_SIZE))
        #size = f.tell()
        #print "file size = %d bytes" % size 

def store_root(node, count, filename):
    print "\n store root ... "
    with open(filename, 'rb+') as f:
        f.seek(0)
        data = convert_node_to_string(node)
        length_of_data = len(data)
        length_packed = convert_integer_to_bytes(length_of_data)
        count_packed = convert_integer_to_bytes(count) 
        f.write(count_packed)
        f.write(length_packed)
        f.write(data)

        size = f.tell() # current location of file (bytes)
        # print "file size = %d bytes" % size 
        if size % BLOCK_SIZE != 0:
            print "padding bits in root... "
            f.write(b"\x00"*(BLOCK_SIZE - size%BLOCK_SIZE))
        #size = f.tell()
        #print "file size = %d bytes" % size 
# get the total number of nodes
def get_count(filename):
    with open(filename,'rb') as f:
        count = convert_bytes_to_integer(f.read(4))
    return count 

def store_count(count, filename):
    with open(filename, 'rb+') as f:
        f.seek(0)
        
        count_packed = convert_integer_to_bytes(count) 
        f.write(count_packed)
        
# check if the file is new or old
def is_file_exists(filename):
    if os.path.exists(filename):
        return True
    else:
        return False

BLOCK_SIZE = 4*1024 # 4k for each node (it will be easy to locate every node and reduce IO time)
INTEGER_SIZE = 4 # 4 byte for the length of data
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
            print "already exists %d nodes " % self.count
        else:
            # read from disk
            #with open(filename,'rb') as f:
            self.count = get_count(self.filename)
            print "already exists %d nodes " % self.count
            self.root = read_from_the_beginning_of_disk(self.filename)
            
        # print "root: ", self.root
        
    # insert (k,v) if it does not exist
    # else doesn't change anything    
    def set(self,k,v):
        
        node  =  self.root  # the current node
        
        # if (k,v) is the first pair
        if self.root == None:
            new_node = Node(0,k,v,-1,-1)
            self.root = new_node
            self.count += 1 # now we have the first node 
            store_root(self.root, 1,  self.filename)
            #store_count(self.count, self.filename)
        #elif self.root
        else:
            offset = self.count
            new_node = Node(offset,k,v,-1,-1)
            
            # now we should do binary search
            while True:
                if k > node.key:
                    print "move to right"
                    if node.right != -1:
                        node = read_from_specific_address(node.right, self.filename)
                    else: # insert it here
                        node.right = offset
                        self.count += 1
                        # node is modified so we re-write it into disk
                        # if the node is root ?
                        if node.offset == 0:
                            store_root(node, self.count, self.filename) # already store the count
                        else:
                            store(node, self.filename) # not root 
                            store_count(self.count, self.filename) 
                        
                        store(new_node, self.filename)
                        
                        print "root: ", read_from_the_beginning_of_disk(self.filename)
                        print "Insert a new node :",
                        print new_node

                        break
                elif k < node.key:
                    print "move to left"
                    if node.left != -1:
                        node = read_from_specific_address(node.left, self.filename)
                    else:
                        # insert
                        node.left = offset
                        self.count += 1
                        # node is modified so we re-write it into disk
                        if node.offset == 0:
                            store_root(node, self.count, self.filename)
                        else:
                            store(node, self.filename)
                            store_count(self.count, self.filename)

                        store(new_node, self.filename)
                        print "Insert a new node :",
                        print new_node
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


    # 
    #def store_to_disk(self):
        # traverse the whole tree


    
    # def create_database(self):
        
    #         new_node = Node(None, None, None, None, 0)
    #         return new_node 
    #     else:
    #         # read from file and create the associated node
    #         with open(self.file, 'wb') as f:

def convert_node_to_string(node):
    return pickle.dumps(
        {
            'offset' : node.offset,
            'key' : node.key,
            'value': node.value,
            'right' : node.right,
            'left' : node.left,

        })

def convert_string_to_node(data):
    dic = pickle.loads(data)
    return Node(
            dic['offset'],
            dic['key'],
            dic['value'],
            dic['right'],
            dic['left']
        )
# beginning location of a file
def seek_to_beginning(f):
    f.seek(0)
# move to the end of a file
def seek_to_end(f):
    f.seek(0,2)
# convert integer to bytes
def convert_integer_to_bytes(number):
    # 'I' means unsigned int
    return struct.pack('I',number)

def convert_bytes_to_integer(data):
    return struct.unpack('I',data)[0]

def store_into_disk(filename,node):
    data = convert_node_to_string(node)
    length_of_data = len(data)
    packed = convert_integer_to_bytes(length_of_data)
    with open(filename,'rb+') as f:
        #f = open(filename,'wb')

        # should seek to some location
        seek_to_end(f)
        
        f.write(packed)
        f.write(data)

        size = f.tell() # current location of file (bytes)
        print "file size = %d bytes" % size 
        if size % BLOCK_SIZE != 0:
            f.write(b"\x00"*(BLOCK_SIZE - size%BLOCK_SIZE))
        size = f.tell()
        print "file size = %d bytes" % size 

# return a Node instance
def read_from_the_beginning_of_disk(filename):
    with open(filename,'rb+') as f:
        #f.seek(4,0)
        count = convert_bytes_to_integer(f.read(4))
        print "count = ", count 
        length = convert_bytes_to_integer(f.read(4))
        print "length = ",length 
        data = convert_string_to_node(f.read(length)) 
    return data

# return a Node instance given offset
def read_from_specific_address(offset,filename):
    assert offset >= 1
    with open(filename,'rb+') as f:
        # seek to the offset-th block
        f.seek(BLOCK_SIZE*(offset))
        length = convert_bytes_to_integer(f.read(4))
        data = convert_string_to_node(f.read(length)) 
    return data 

# test read and write to disk 
def test_write(filename):
    node = Node(0,100,100,-1,-1)
    data = convert_node_to_string(node)
    f = open(filename,'wb')
    length_of_data = len(data)
    # write data to file
    print "length = ",length_of_data
    
    packed = convert_integer_to_bytes(length_of_data)
    # len(packed) == 4
    print "length packed = ", packed
    length = struct.unpack('I',packed) # which is a tuple
    print "length unpacked = ", length[0]
    print convert_string_to_node(data)
    # store length+data into file 
    # length is 4 bytes and data is 90 bytes
    seek_to_beginning(f)
    # firstly write the 4 Bytes length
    f.write(packed)
    # then write the actual data
    f.write(data)
    # fill in extra bytes to be 4KB size
    seek_to_end(f) 
    size = f.tell() # current location of file (bytes)
    #print "file size = %d bytes" % size 
    if size % BLOCK_SIZE != 0:
        f.write(b"\x00"*(BLOCK_SIZE - size%BLOCK_SIZE))
    size = f.tell()
    print "file size = %d bytes" % size 
    f.close()

def test_read(filename):
    assert is_file_exists(filename) == True
    with open(filename,'rb') as f:
        length = convert_bytes_to_integer(f.read(4))
        data = convert_string_to_node(f.read(length))
        print "\nlength = ",length
        print "data = ",data
        print "filesize = %dB" % os.path.getsize(filename)


if __name__ == '__main__':
    filename = 'test.db'
    test_write(filename)
    #test_read(filename)
    print read_from_the_beginning_of_disk(filename)

    