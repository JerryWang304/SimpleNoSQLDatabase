import os
import struct
from node import Node
import portalocker
try: 
    import cPickle as pickle 
except:
    import pickle

BLOCK_SIZE = 4*1024 # 4k for each node (it will be easy to locate every node and reduce IO time)
INTEGER_SIZE = 4 # 4 byte for the length of data

class Disk(object):
    def __init__(self,filename):
        self.filename = filename
        self.locked = False 
    # lock file
    def lock(self,file):
        if not self.locked:
            portalocker.lock(file, portalocker.LOCK_EX)
            self.locked = True
    # unlock file
    def unlock(self,file):
        if self.locked:
            #self.filename
            portalocker.unlock(file)
            self.locked = False 
    # write to disk
    def store(self, node):
        # if node.get_offset() == 0:
        #     store_root(node,count,filename)
        #     return 
        with open(self.filename, 'rb+') as f:
            self.lock(f)
            f.seek(BLOCK_SIZE*node.offset)
            data = self.convert_node_to_string(node)
            length_of_data = len(data)
            packed = self.convert_integer_to_bytes(length_of_data)
            f.write(packed)
            f.write(data)

            size = f.tell() # current location of file (bytes)
            # print "file size = %d bytes" % size 
            if size % BLOCK_SIZE != 0:
                #print "padding bits in normal nodes"
                f.write(b"\x00"*(BLOCK_SIZE - size%BLOCK_SIZE))
            #size = f.tell()
            #print "file size = %d bytes" % size 
            f.flush()
            self.unlock(f)

    def store_root(self,node, count):
        #print "\n store root ... "
        with open(self.filename, 'rb+') as f:
            self.lock(f)
            f.seek(0)
            data = self.convert_node_to_string(node)
            length_of_data = len(data)
            length_packed = self.convert_integer_to_bytes(length_of_data)
            count_packed = self.convert_integer_to_bytes(count) 
            f.write(count_packed)
            f.write(length_packed)
            f.write(data)

            size = f.tell() # current location of file (bytes)
            # print "file size = %d bytes" % size 
            if size % BLOCK_SIZE != 0:
                # print "padding bits in root... "
                f.write(b"\x00"*(BLOCK_SIZE - size%BLOCK_SIZE))
            #size = f.tell()
            #print "file size = %d bytes" % size 
            f.flush()
            self.unlock(f)
    # get the total number of nodes
    def get_count(self):
        with open(self.filename,'rb') as f:
            count = self.convert_bytes_to_integer(f.read(4))
        return count 

    def store_count(self, count):
        with open(self.filename, 'rb+') as f:
            self.lock(f)
            f.seek(0)
            
            count_packed = self.convert_integer_to_bytes(count) 
            f.write(count_packed)
            f.flush()
            self.unlock(f)
    # check if the file is new or old
    def is_file_exists(self):
        if os.path.exists(self.filename):
            return True
        else:
            return False

    def convert_node_to_string(self, node):
        return pickle.dumps(
            {
                'offset' : node.offset,
                'key' : node.key,
                'value': node.value,
                'left' : node.left,
                'right' : node.right,
                'valid' : node.valid,
                'father': node.father,
                'relative_position': node.relative_position,

            })

    def convert_string_to_node(self, data):
        dic = pickle.loads(data)
        #print "type of key = ",type(dic['key'])
        # return Node(
        #         int(dic['offset']),
        #         int(dic['key']),
        #         int(dic['value']),
        #         int(dic['left']),
        #         int(dic['right']),
        #     )
        return Node(
                dic['offset'],
                dic['key'],
                dic['value'],
                dic['left'],
                dic['right'],
                dic['valid'],
                dic['father'],
                dic['relative_position'],
            )
    # beginning location of a file
    def seek_to_beginning(self, f):
        f.seek(0)
    # move to the end of a file
    def seek_to_end(f):
        f.seek(0,2)
    # convert integer to bytes
    def convert_integer_to_bytes(self, number):
        # 'I' means unsigned int
        return struct.pack('I',number)

    def convert_bytes_to_integer(self, data):
        return struct.unpack('I',data)[0]

    def store_into_disk(self,node):
        data = self.convert_node_to_string(node)
        length_of_data = len(data)
        packed = self.convert_integer_to_bytes(length_of_data)
        with open(self.filename,'rb+') as f:
            #f = open(filename,'wb')
            self.lock(f) 
            # should seek to some location
            self.seek_to_end(f)
            
            f.write(packed)
            f.write(data)

            size = f.tell() # current location of file (bytes)
            #print "file size = %d bytes" % size 
            if size % BLOCK_SIZE != 0:
                f.write(b"\x00"*(BLOCK_SIZE - size%BLOCK_SIZE))
            #size = f.tell()
            f.flush()
            #print "file size = %d bytes" % size 
            self.unlock(f)
    # return a Node instance
    def read_from_the_beginning_of_disk(self):
        with open(self.filename,'rb+') as f:
            #f.seek(4,0)
            count = self.convert_bytes_to_integer(f.read(4))
            #print "count = ", count 
            length = self.convert_bytes_to_integer(f.read(4))
            #print "length = ",length 
            data = self.convert_string_to_node(f.read(length)) 
        return data

    # return a Node instance given offset
    def read_from_specific_address(self, offset):
        assert offset >= 1
        with open(self.filename,'rb+') as f:
            # seek to the offset-th block
            f.seek(BLOCK_SIZE*(offset))
            length = self.convert_bytes_to_integer(f.read(4))
            data = self.convert_string_to_node(f.read(length)) 
        return data 

# # test read and write to disk 
# def test_write(filename):
#     node = Node(0,100,100,-1,-1)
#     data = convert_node_to_string(node)
#     f = open(filename,'wb')
#     length_of_data = len(data)
#     # write data to file
#     print "length = ",length_of_data
    
#     packed = convert_integer_to_bytes(length_of_data)
#     # len(packed) == 4
#     print "length packed = ", packed
#     length = struct.unpack('I',packed) # which is a tuple
#     print "length unpacked = ", length[0]
#     print convert_string_to_node(data)
#     # store length+data into file 
#     # length is 4 bytes and data is 90 bytes
#     seek_to_beginning(f)
#     # firstly write the 4 Bytes length
#     f.write(packed)
#     # then write the actual data
#     f.write(data)
#     # fill in extra bytes to be 4KB size
#     seek_to_end(f) 
#     size = f.tell() # current location of file (bytes)
#     #print "file size = %d bytes" % size 
#     if size % BLOCK_SIZE != 0:
#         f.write(b"\x00"*(BLOCK_SIZE - size%BLOCK_SIZE))
#     size = f.tell()
#     print "file size = %d bytes" % size 
#     f.close()

# def test_read(filename):
#     assert is_file_exists(filename) == True
#     with open(filename,'rb') as f:
#         length = convert_bytes_to_integer(f.read(4))
#         data = convert_string_to_node(f.read(length))
#         print "\nlength = ",length
#         print "data = ",data
#         print "filesize = %dB" % os.path.getsize(filename)


# if __name__ == '__main__':
#     filename = 'test.db'
#     test_write(filename)
#     #test_read(filename)
#     print read_from_the_beginning_of_disk(filename)