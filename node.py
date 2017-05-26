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
    # get value
    def get_value(self):
        return self.value 
    # is leaf ?
    def is_leaf(self):
        return self.left == -1 and self.right == -1
    # is root ?
    def is_root(self):
        return self.offset == 0
