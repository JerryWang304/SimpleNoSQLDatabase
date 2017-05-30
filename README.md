### A simple nosql database

It is a toy version, and only supports integers now. I write the code after reading the tutorial in 500 lines, but mine implementation is different from it. However, I also use binary tree for simplicity. I don't have enough time.

#### Usage
##### Set : insert a pair (key,value)
``` python
python main.py test.db set 12 100
```
##### Get : return the associated value, which is 100 in this case
``` python
python main.py test.db get 12
```
##### Del : logical deletion
``` python
python main.py test.db del 12
```

#### Performance

slow…. it takes more than 2s to insert 10000 records