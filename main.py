#!usr/bin/python
# coding : utf-8
# A simple NoSQL database
# author: Jerry Wang
import sys
from database import Database # Fix
def check(args):
    length = len(args)
    if length >= 5 or length <= 4:
        print "invalid input"

def main():
    args_len = len(sys.argv) # length of input
    #print args_len
    if args_len > 5 or args_len < 4:
        print "invalid input"
        return
    filename = sys.argv[1]
    command = sys.argv[2]
    key = int(sys.argv[3])
    value = int(sys.argv[4]) if args_len == 5 else None
    # print "type of input key = ",type(key)
    #print filename,command,key,value
    assert command in {'get','del','set'}
    # open the database
    db = Database(filename)
    if command == "get":

        db.get(key)

    elif command == "del":
        db.delete(key)
        print "command = ", command
    elif command == "set":
        assert value != None
        db.set(key,value)

if __name__ == '__main__':
    main()
