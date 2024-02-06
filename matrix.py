import copy
import io

# 20216913 - Nguyễn Thị Linh Chi

__all__ = ['Matrix', 'zeros', 'identity']

class Matrix:
    __data = None
    __n_rows = None
    __n_cols = None
    __max_width = 0
    
    def __init__(self, data):
        self.__data = copy.deepcopy(data)
        self.__n_rows = len(data)
        self.__n_cols = len(data[0])
        for r in range(self.__n_rows):
            for c in range(self.__n_cols):
                self.__max_width = max(self.__max_width, len(str(data[r][c])))
        
        self.__max_width += 2

    
    # Get number of rows of the matrix
    @property
    def m(self):
        return self.__n_rows

    
    # Get number of columns of the matrix
    @property
    def n(self):
        return self.__n_cols

    
    # Return the transpose matrix of the this matrix
    @property
    def T(self):
        new_data = []
        for c in range(self.__n_cols):
            new_row = []
            for r in range(self.__n_rows):
                new_row.append(self.__data[r][c])
            new_data.append(new_row)

        return Matrix(new_data)


    def __getitem__(self, key):
        if isinstance(key, int) or isinstance(key, slice):
            return self.__data[key]
        if not isinstance(key, tuple) and not isinstance(key, list) :
            raise ValueError('Matrix indices must be tuple of ins or list of ints')
        if len(key) != 2:
            raise ValueError(f"Number of indices ({len(key)}) don't match the dimensions (2)")
        i1, i2 = key
        return self.__data[i1][i2]
    
    def __setitem__(self, key, value):
        if isinstance(key, int) or isinstance(key, slice):
            self.__data[key] = value
            for i in value:
                self.__max_width = max(len(str(i)) + 2, self.__max_width)
            return
        if not isinstance(key, tuple) and not isinstance(key, list) :
            raise ValueError('Matrix indices must be tuple of ins or list of ints')
        if len(key) != 2:
            raise ValueError(f"Number of indices ({len(key)}) don't match the dimensions (2)")
        i1, i2 = key
        self.__data[i1][i2] = value
        self.__max_width = max(len(str(value)) + 2, self.__max_width)

    
    @property
    def shape(self):
        return self.__n_rows, self.__n_cols
    
    def copy(self):
        return Matrix(copy.deepcopy(self.__data))
    
    def __iter__(self):
        for _, value in enumerate(self.__data):
            yield value
    def __str__(self):
        residual = '   '
        padding = ' '*(self.__max_width*self.__n_cols ) + residual
        string_data = [u'\u250c' + padding + u'\u2510']
        for r in range(self.__n_rows):
            string_buffer = io.StringIO()
            string_buffer.write(u'\u2502')
            for c in range(self.__n_cols):
                string_buffer.write("{:>{width}}".format(self.__data[r][c], width=self.__max_width))
            string_buffer.write(residual + u'\u2502')
            string_data.append(string_buffer.getvalue())
        string_data.append(u'\u2514' + padding + u'\u2518')
        return '\n'.join(string_data)

# Tạo data ma trận không.
def zeros(m, n):
    data = []
    for _ in range(m):
        data.append([0.]*n)
    return data

# Tạo ma trận đơn vị cấp n
def identity(n):
    data = []
    for i in range(n):
        data.append([0.]*n)
        data[i][i] = 1.
    return Matrix(data)   