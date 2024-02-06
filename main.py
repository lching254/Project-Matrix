
# 20216913 - Nguyễn Thị Linh Chi

from my_math import *


prompt = \
"""
***************************************************************************************
**                                      MENU                                         **
***************************************************************************************
*       1. Nhập ma trận từ bàn phím                                                  **
*       2. Nhập ma trận từ file                                                      **
*       3. Nhân ma trận với số thực                                                  **
*       4. Cộng 2 ma trận                                                            **
*       5. Trừ 2 ma trận                                                             **
*       6. Nhân 2 ma trận                                                            **
*       7. Tính định thức                                                            **
*       8. Tìm ma trận nghịch đảo                                                    **
*       9. Tìm ma trận chuyển vị                                                     **
*       0. Thoát chương trình                                                        **
***************************************************************************************
"""

matrices = {}


if __name__ == "__main__":
    while True:
        print(prompt)
        choice = input("Chọn chức năng: ")

        match choice:
            case '0':
                print("Đã thoát.")
                break

            case '1':
                name_matrix = input("Nhập tên của ma trận: ")
                
                try:
                    matrix = read_Matrix()   
                    matrices[name_matrix] = matrix
                    print(matrix)
                except Exception as err:
                    print("Error:", err)
                
                
            case '2':
                name_matrix = input("Nhập tên ma trận: ")        
                filename = input("Nhập tên file: ")

                try:
                    matrix = load_matrix_from_file(filename)       
                    matrices[name_matrix] = matrix
                    print(matrix)
                except Exception as err:
                    print("Error:", err)

                
            case '3':    
                name_matrix = input("Nhập tên của ma trận: ")
                k = float(input("Nhập số thực k: "))
                matrix = matrices.get(name_matrix)

                if matrix is None:
                    print("Error: Matrix does not exist")
                    continue
                result = multiply_with_scalar(matrix, k)
                to_file(str(result), f"Kết quả {k}*{name_matrix}:") 
                
                
            case '4':
                name_matrix1 = input("Nhập tên của ma trận 1: ")
                name_matrix2 = input("Nhập tên của ma trận 2: ")
                matrix1 = matrices.get(name_matrix1)
                matrix2 = matrices.get(name_matrix2)

                if matrix1 is None or matrix2 is None :
                    print("Error: Input is invalid.")
                    continue
                else: 
                    try: 
                        result = sum_matrix(matrix1,matrix2)
                        to_file(str(result), f"Kết quả {name_matrix1} + {name_matrix2}:") 
                    except Exception as err:
                        print("Error:", err)
                

            case '5':
                name_matrix1 = input("Nhập tên của ma trận 1: ")
                name_matrix2 = input("Nhập tên của ma trận 2: ")
                matrix1 = matrices.get(name_matrix1)
                matrix2 = matrices.get(name_matrix2)

                if matrix1 is None or matrix2 is None :
                    print("Error: Input is invalid.")
                    continue 
                else:
                    try: 
                        result = subtraction_matrix(matrix1,matrix2)
                        to_file(str(result), f"Kết quả {name_matrix1} - {name_matrix2}:") 
                    except Exception as err:
                        print("Error:", err)


            case '6': 
                name_matrix1 = input("Nhập tên của ma trận 1: ")
                name_matrix2 = input("Nhập tên của ma trận 2: ")
                matrix1 = matrices.get(name_matrix1)
                matrix2 = matrices.get(name_matrix2)

                if matrix1 is None or matrix2 is None :
                    print("Error: Input is invalid.")
                    continue
                else:
                    try: 
                        result = multiply_matrix(matrix1,matrix2)
                        to_file(str(result), f"Kết quả {name_matrix1} * {name_matrix2}:") 
                    except Exception as err:
                        print("Error:", err)
                    

            case '7':
                name_matrix = input("Nhập tên của ma trận: ")
                matrix = matrices.get(name_matrix)

                if matrix is None:
                    print("Error: Matrix does not exist")
                    continue
                else:
                    try:
                        result = det_matrix(matrix)  
                        to_file(str(result), f"Định thức của ma trận {str(name_matrix)} là:")
                    except Exception as err:
                        print("Error:", err)    
                   

            case '8':
                name_matrix = input("Nhập tên của ma trận: ")
                matrix = matrices.get(name_matrix)
                
                if matrix is None:
                    print("Error: Matrix does not exist")
                    continue
                else:
                    try:
                        result =  inverse_matrix(matrix)
                        to_file(str(result), f"Ma trận nghịch đảo của {str(name_matrix)} là : ")
                    except Exception as err:
                        print("Error:", err)


            case '9':  
                name_matrix = input("Nhập tên của ma trận: ")
                matrix = matrices.get(name_matrix)  
                
                if matrix is None:
                    print("Error: Matrix does not exist")
                    continue
                else:
                    result = transpose_matrix(matrix)
                    to_file(str(result), f"Ma trận chuyển vị của {str(name_matrix)} là :")

                    
            case other:
                print('No match found')