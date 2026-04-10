import numpy as np


def LSPointLines(L: np.ndarray) -> np.ndarray:
 
    a_i = L[0, :].astype(float)  #Array of all a_i
    b_i = L[1, :].astype(float)  #Array of all b_i
    c_i = L[2, :].astype(float)  #Array of all c_i

    n = len(a_i)
    p_i = [0] * n #each index i of p_i will be = sqrt(a_i^2 + b_i^2)

    for i in range(n): #calculating the pi to then normalize
        p_i[i] = (a_i[i] ** 2 + b_i[i] ** 2) ** 0.5
 
        
    for i in range(n):
        a_i[i] = a_i[i] / p_i[i]

        b_i[i] = b_i[i] / p_i[i]

        c_i[i] = c_i[i] / p_i[i]

    #after normalization the distance formula simply becomes the formula bellow 
    #di(p) = ai * x + bi * y + ci
    
    matrix_A = np.column_stack((a_i, b_i))

    #r(p) = Ap + c
    #and the thing we minimize is exaclty the Euclidean norm squared, basically the distances sqyared
    #f(p) = ||Ap + c||^2
    ##taking the standar matrix derivative in terms of p, we get the gradient of f(p) = 2A^T(AP+c)
    ##setting the gradient to zero (A^T A)p = -A^T c

    #(A^T A)p = -A^T c
    ## Let S = A^T A, t = A^T C
    
    S = np.dot(matrix_A.T, matrix_A)
    T = np.dot(matrix_A.T, c_i)

    ## p = -S^-1 T  
    inverse_S = np.linalg.inv(S)
    neg_inverse_S = -1 * inverse_S

    p = np.dot(neg_inverse_S, T) 

    p = p.reshape(2, 1)

    return p




n = 3  # number of columns
arr = np.ones((3, n), dtype=int)   # 3×n array of ones

arr = np.array([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 10]])   # not proportional to the others



print("this is point p")
print(LSPointLines(arr))

