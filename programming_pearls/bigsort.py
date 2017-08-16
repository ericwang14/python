#! /usr/local/python
# this is bitmap sorting implement
# the alogrithm for this one is use bitmap to represent each number in the array# eg: [10, 2, 5, 8] the bitmap is 0 1 0 0 1 0 0 1 0 1
# the bit map size is base on the maximum number in the array 

BIT_SPERWORD = 32
SHIFT = 5
MASK = 0x1F

class BitSort:
    def __init__(self, size):
        self.a = [0]*(1 + size/BIT_SPERWORD)
    
    def set(self, i):
	if self.has(i):
	    raise ValueError(str(i) + " already exist")
        self.a[i>>SHIFT] |= 1<<(i & MASK)
  
    def clr(self, i):
        self.a[i>>SHIFT] &= ~(1<<(i & MASK))

    def has(self, i):
	return self.a[i>>SHIFT] & (1<<(i & MASK))


if __name__ == '__main__':
    arr = [23, 100, 25, 120, 22, 8, 12, 3, 21, 31, 50, 13, 15, 6, 2]
    bit_sort = BitSort(120)
    for i in arr:
        bit_sort.set(i)

    for i in range(120):
	if (bit_sort.has(i)):
	    print i
    
