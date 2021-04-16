'''
Contains an ADT for daa analysis
'''
import sys
import ctypes


class SignPoint(ctypes.Structure):
    """
    Contains all into about a point taken from the database.
    """
    _fields_ = [
        ('image_name', ctypes.py_object),
        ('initial_size_x', ctypes.c_int),
        ('initial_size_y', ctypes.c_int),
        ('country', ctypes.py_object),
        ('occlusions', ctypes.py_object),
        ('sign_class', ctypes.py_object),
        ('sign_type', ctypes.py_object),
    ]

    def __repr__(self):
        return ','.join(map(str, (
            self.image_name, self.initial_size_x, self.initial_size_y,
            self.country, self.occlusions, self.sign_class, self.sign_type
        )))

    def from_repr(self, file_line):
        """
        >>> sp = SignPoint()
        >>> sp.from_repr("img.jpg,100,50,GERMANY,VISIBLE,PROHIBITORY,120_SIGN")
        >>> print(sp.image_name)
        img.jpg
        """
        props = file_line.strip('\n').split(",")
        props[1], props[2] = int(props[1]), int(props[2])
        (
            self.image_name, self.initial_size_x, self.initial_size_y,
            self.country, self.occlusions, self.sign_class, self.sign_type
        ) = props

    def __sizeof__(self):
        return ctypes.sizeof(self) + sys.getsizeof(self)


# create from line in file:
sp = SignPoint()
sp.from_repr("img.jpg,100,50,GERMANY,VISIBLE,PROHIBITORY,120_SIGN")
# print()
# print(sp)
# create from constructor
p = SignPoint("img.jpg", 100, 50, "GERMANY", 'VISIBLE', 'PROHIBITORY', '120_SIGN')
print()
print("Put this into CSV:")
print(p)
print()
print("Access properties:")
print(p.image_name, p.initial_size_x, p.initial_size_y)
print()
print("Struct size in bytes: ", ctypes.sizeof(p) + sys.getsizeof(p))


####  ARRAY CODE BEGINS HERE


# Implements the Array ADT using array capabilities of the ctypes module.
class Array:
    # Creates an array with size elements.
    def __init__(self, size, el_ctype=ctypes.py_object):
        assert size > 0, "Array size must be > 0"
        self._size = size
        self._el_ctype = el_ctype
        self._none_type = None if el_ctype == ctypes.py_object else el_ctype(0)
        # Create the array structure using the ctypes module.
        py_array_type = el_ctype * size
        self._elements = py_array_type()
        # Initialize each element.
        self.clear(self._none_type)

    # Returns the size of the array.
    def __len__(self):
        return self._size

    # Gets the contents of the index element.
    def __getitem__(self, index):
        assert 0 <= index < len(self), "Array subscript out of range"
        return self._elements[index]

    # Puts the value in the array element at index position.
    def __setitem__(self, index, value):
        assert 0 <= index < len(self), "Array subscript out of range"
        self._elements[index] = value

    # Clears the array by setting each element to the given value.
    def clear(self, value=None):
        if value is None:
            value = self._none_type
        for i in range(len(self)):
            self._elements[i] = value

    # Returns the array's iterator for traversing the elements.
    def __iter__(self):
        return _ArrayIterator(self._elements)

    # Calculates array's size in bytes.
    def __sizeof__(self):
        size = ctypes.sizeof(self._elements)
        size += sum(
            sys.getsizeof(elem)
            for elem in self.__dict__.values()
        )
        return size


# An iterator for the Array ADT.
class _ArrayIterator:
    def __init__(self, the_array):
        self._array_ref = the_array
        self._cur_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._cur_index < len(self._array_ref):
            entry = self._array_ref[self._cur_index]
            self._cur_index += 1
            return entry
        else:
            raise StopIteration


# this will read the whole file into structs (EXAMPLE CODE)
class SignPointArray:
    def __init__(self, num_rows=1, el_ctype=ctypes.py_object):
        self._el_ctype = el_ctype
        self._none_type = None if el_ctype == ctypes.py_object else el_ctype(0)

        # Create a 1-D array to store an array reference for each row.
        self.rows = Array(num_rows)

        # Create the 1-D arrays for each row of the 2-D array.
        for i in range(num_rows):
            self.rows[i] = SignPoint()

    def from_file(self, filename):
        for row, line in enumerate(open(filename, 'r')):
            self.rows[row].from_repr(line)

    def num_rows(self):
        return len(self.rows)

    # Gets the contents of the element at position [i, j]
    def __getitem__(self, index):
        return self.rows[index]

    # Sets the contents of the element at position [i,j] to value.
    def __setitem__(self, index, value):
        self.rows[index] = value

    # Returns the array's iterator for traversing the elements.
    def __iter__(self):
        return _ArrayIterator(self.rows)

    # Calculates array's size in bytes.
    def __sizeof__(self):
        size = sum(
            sys.getsizeof(self.rows[row])
            for row in range(self.num_rows())
        )
        size += sum(
            sys.getsizeof(elem)
            for elem in self.__dict__.values()
        )
        return size