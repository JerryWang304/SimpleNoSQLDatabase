#!usr/bin/python
#coding: utf-8
import os
import random
import time
import datetime
MIN = -1000
MAX = 3000
def test():
    t = 1
    total_time = 0
    keys = []
    while t<= 10000:
        t += 1
        key = random.randint(MIN,MAX)
        keys.append(key)
        value = random.randint(-100,100)
        begin = time.clock()
        cmd = 'python main.py first.txt set %d %d' % (key, value)
        os.system(cmd)
        end = time.clock()
        total_time += end-begin
    print "**** keys = ",keys
    return total_time
if __name__ == '__main__':
    print "total time = ", test()
