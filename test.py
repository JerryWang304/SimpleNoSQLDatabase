#!usr/bin/python
#coding: utf-8
import os
import random
import time
import datetime
MIN = -5000
MAX = 10000
def test():
    t = 1
    total_time = 0
    while t<=10000:
        t += 1
        key = random.randint(MIN,MAX)
        value = random.randint(-100,100)
        begin = time.clock()
        cmd = 'python main.py test.db set %d %d' % (key, value)
        os.system(cmd)
        end = time.clock()
        total_time += end-begin
    return total_time
if __name__ == '__main__':
    print "total time = ", test()
