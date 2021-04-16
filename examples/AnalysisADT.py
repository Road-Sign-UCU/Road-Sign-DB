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
        props = file_line.split(",")
        props[1], props[2] = int(props[1]), int(props[2])
        (
            self.image_name, self.initial_size_x, self.initial_size_y,
            self.country, self.occlusions, self.sign_class, self.sign_type
        ) = props


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