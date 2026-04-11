import numpy as np

##Does same thing as Version 1 just written a little differently
def LSPointLines(L: np.ndarray) -> np.ndarray:
 
    a_i = L[0, :].astype(float)  #Array of all a_i
    b_i = L[1, :].astype(float)  #Array of all b_i
    c_i = L[2, :].astype(float)  #Array of all c_i

    n = len(a_i)
    p_i = [0] * n #each index i of p_i will be = sqrt(a_i^2 + b_i^2)

    #Calculating p_i to then normalize. Could us a loop but dont have too
    p_i = (a_i ** 2 + b_i ** 2) ** 0.5
    
    
    # guard against degenerate lines (zero-length normal)
    eps = 1e-12
    for i in range(n):
        if abs(a_i[i]) < eps and abs(b_i[i]) < eps and abs(c_i[i]) < eps:
            raise ValueError("Invalid line (0,0,0) found.")
        if p_i[i] <= eps:
            raise ValueError("Found a degenerate line with zero normal length.")
        
    
    #normalizing with the pi. Again could use a loop but dont have too
    a_i = a_i / p_i
    b_i = b_i / p_i
    c_i = c_i / p_i

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
    # Using a stable solve to find the inverse instead of explicit inverse which was used in the previous code version
    try:
        p = -np.linalg.solve(S, T)
    except np.linalg.LinAlgError:
        # fallback: minimum-norm LS if S is singular/ill-conditioned
       raise ValueError("Degenerate configuration: closest point not unique.")
        

    p = p.reshape(2, 1)

    return p


