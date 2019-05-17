import ctypes


class Array:
    def __init__(self, size, fill_with=None):
        self.size = size
        self.data = (ctypes.py_object*self.size)()
        for i in range(self.size):
            self[i] = fill_with

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        if index < 0:
            index = self.size + index
        if index > self.size-1:
            raise IndexError('index out of range')
        return self.data[index]

    def __setitem__(self, index, value):
        if index < 0:
            index = self.size + index
        if index > self.size-1:
            temp = (ctypes.py_object*(self.size*2))()
            for i in range(self.size):
                temp[i] = self.data[i]
            self.data = temp
            self.size *= 2
            self[index] = value
            return
        self.data[index] = value

    def __iter__(self):
        return ArrayIterator(self.data)

class ArrayIterator:
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            res = self.data[self.pos]
            self.pos += 1
            return res
        except IndexError:
            raise StopIteration


class TwoDimArray:
    def __init__(self, h, w, fill_with=None):
        self.height = h
        self.width = w
        self.data = Array(h)
        for i in range(self.height):
            self.data[i] = Array(w, fill_with)

    def __len__(self):
        return self.height

    def __getitem__(self, index_tuple):
        if type(index_tuple) == int:
            return self.data[index_tuple]
        return self.data[index_tuple[0]][index_tuple[1]]

    def __setitem__(self, index_tuple, value):
        if type(index_tuple) == int:
            raise TypeError
        self.data[index_tuple[0]][index_tuple[1]] = value
