import re
from matrix import *
from decimal import Decimal

# 20216913 - Nguyễn Thị Linh Chi

# Tính số chữ số thập phân
def count_decimal(num):
    decimal_count = -Decimal(str(num)).as_tuple().exponent
    return decimal_count

def is_zero(x):
    return abs(x) < 1e-7

# Check input từ bàn phím
def is_matrix(data, rows, cols):
    return len(data) == rows and all(len(m) == cols for m in data)


# Nhập ma trận từ bàn phím
def read_Matrix():
    while True:
        rows = int(input("Nhập số hàng: "))
        if rows < 1:             
            print("Nhập lại số hàng: ")
        else:
            break

    while True:
        cols = int(input("Nhập số cột: "))
        if cols < 1:
            print("Nhập lại số cột: ")
        else:
            break

    data = []
    print("Nhập ma trận:")
    for i in range(rows):
        data.append(list(map(float, input().strip().split())))
    if is_matrix(data, rows, cols):
        return Matrix(data)
    else:
        raise ValueError("Incorrect input")    


# Ghi ra file kết quả
def to_file(obj_str, header=''):    
    if not isinstance(obj_str, str):
        print('obj_str must be string!')
        return
    try:
        fout = open("matrix.out", mode='a', encoding='utf-8')
        fout.write('\n')    
        fout.write(header + '\n')
        fout.write(obj_str)
    finally:
        fout.close() 


# Đọc ma trận từ file
def load_matrix_from_file(path):
    with open(path) as f:
        lines = f.readlines()
        
    data = []
    for line in lines:
        row = list(map(float, line.strip().split()))
        data.append(row)
    rows = len(data)
    cols = len(data[0])
    if is_matrix(data, rows, cols):
        return Matrix(data)
    else:
        print("The file does not contain a matrix.")


# Nhân 1 ma trận với 1 số
def multiply_with_scalar(A,k):
    m,n = A.shape
    result= zeros(m, n)
    for i in range(m):
        for j in range(n):
            # Làm tròn đến số chữ số thập phân bằng tổng số chữ số thập phân của k và A[i][j]
            result[i][j] = round(k*A[i][j], count_decimal(k)+count_decimal(A[i][j]))
    return Matrix(result)


# Cộng 2 ma trận A + B
def sum_matrix(A,B):
    m1,n1 = A.shape
    m2,n2 = B.shape
    if m1 == m2 and n1 == n2:
        result= zeros(m1, n1)
        for i in range(m1):
            for j in range(n1):
                result[i][j] = round(A[i][j] + B[i][j],max(count_decimal(B[i][j]),count_decimal(A[i][j])))
        return Matrix(result)
    else:
        raise ValueError("Matrix size mismatch.")


# Trừ 2 ma trận A - B
def subtraction_matrix(A,B):
    m1,n1 = A.shape
    m2,n2 = B.shape
    if m1 == m2 and n1 == n2:
        result= zeros(m1, n1)
        for i in range(m1):
            for j in range(n1):
                result[i][j] = round(A[i][j] - B[i][j],max(count_decimal(B[i][j]),count_decimal(A[i][j])))
        return Matrix(result)
    else:
        raise ValueError("Matrix size mismatch.")
    

# Nhân 2 ma trận A*B
def multiply_matrix(A,B):   
    m1,n1 = A.shape
    m2,n2 = B.shape
    if n1 == m2:
        result = zeros(m1, n2)            
        for i in range(m1):
            for j in range(n2):
                sum = 0
                for k in range(n1):
                    sum = round(sum + A[i][k]*B[k][j],max(count_decimal(sum),count_decimal(A[i][j])+count_decimal(B[i][j])))
                result[i][j] = sum
        return Matrix(result)
    else:
        raise ValueError("Dimension mismatch. Two matrices have incompatible sizes.")


# Tính định thức của ma trận 
def det_matrix(A):
    m,n = A.shape
    if m != n:
        raise ValueError("The matrix is not square.")

    A = A.copy()
    memory = [0]*n
    det = 1

    for i in range(n):
        swap_index = i 
        while(swap_index < n and A[swap_index, i] == 0):
            swap_index += 1
        if(swap_index == n):
            return 0.0
 
        if(swap_index != i):
            temp = A[swap_index]
            A[swap_index] = A[i]
            A[i] = temp
            det = -det
 
        for j in range(n):
            memory[j] = A[i][j]
 
        for j in range(i+1, n):
            p =  A[j][i]/A[i][i]
            for k in range(n):
                A[j][k] = A[j][k] - p*memory[k]
                
    for i in range(n):
        det = det*A[i][i]
    return det

# Nối 2 ma trận A, B
def concat(A, B, axis):
    m1, n1 = A.shape
    m2, n2 = B.shape
    if not isinstance(axis, int) or (axis > 1 or axis < 0):
        raise ValueError("Axis must be 0 or 1")
    if axis == 1:
        if m1 != m2:
            raise ValueError("Dimension mismatch")
        m = m1
        n = n1 + n2
    else:
        if n1 != n2:
            raise ValueError("Dimension mismatch")
        m = m1 + m2
        n = n1

    result = zeros(m, n)
    for i in range(m):
        for j in range(n):
            if i < m1 and j < n1:
                result[i][ j] = A[i][ j]
            else:
                if i >= m1:
                    bi = i - m1
                    bj = j
                else:
                    bi = i
                    bj = j - n1
                result[i][j] = B[bi][bj]
    return result



# Chọn phần tử khử và khử ma trận
def reduce_matrix(aug_A, mask_row, mask_col):
    m, n = aug_A.shape             
    found = False
    temp_max = 0
    
    # Ma trận aug_A là ma trận [A/I](mxn). Phép chọn phần tử khử chỉ thực hiện trên A(mxm).
    for i in range(m): # Ưu tiên chọn phần tử khử +-1
        if mask_row[i]:
            continue
        for j in range(m):
            if mask_col[j]:
                continue
            if(is_zero(abs(aug_A[i][j]) - 1)):
                row, col = i, j
                found = True

    if not found: # Ưu tiên phần tử có trị tuyệt đối max
        for i in range(m):
            if mask_row[i]:
                continue
            for j in range(m):
                if mask_col[j]: 
                    continue
                if abs(aug_A[i, j]) > temp_max:
                    temp_max = aug_A[i][j]
                    row = i
                    col = j
        if temp_max == 0:
            print("The matrix is not invertible.")
            return None

    mask_row[row] = True
    mask_col[col] = True

    for i in range(m): #Phép khử thực hiện trên [A/I](mxn)
        if i != row:
            p = aug_A[i][col] / aug_A[row][col]
            for j in range(n):
                    aug_A[i][j] = aug_A[i][j] - aug_A[row][j] * p
                      
    aug_A[row] = [val / aug_A[row][col] for val in aug_A[row]]
    return aug_A

# Tìm ma trận nghịch đảo
def inverse_matrix(A):
    m, n = A.shape
    
    if m != n:
        raise ValueError("The matrix is not square.")

    if det_matrix(A) == 0:
        raise ValueError("The matrix is not invertible.") 

    mask_row = [False]*m
    mask_col = [False]*m    
    aug_matrix = Matrix(concat(A.copy(), identity(m), axis=1))    
    dem = 0

    while dem < n:
        aug_matrix = reduce_matrix(aug_matrix, mask_row, mask_col)
        dem +=1            
    
    temp = zeros(1,2*n)
    for i in range(n): # Đưa ma trận A về ma trận đường chéo
        for j in range(n):
            if aug_matrix[j][i] == 1:
                temp[0] = aug_matrix[i]
                aug_matrix[i] = aug_matrix[j]
                aug_matrix[j] = temp[0]                
    
    inv_matrix = []
    for row in aug_matrix:
        inv_matrix.append(list(map(lambda x: round(x, 10), row[n:])))                                                 
    return Matrix(inv_matrix)
   

#Tìm ma trận chuyển vị 
def transpose_matrix(A):
    return A.T
