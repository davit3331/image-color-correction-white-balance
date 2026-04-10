import numpy as np 

def noiseAnalDiff(im1: np.ndarray, im2: np.ndarray) -> float:
    
    if im1.shape != im2.shape:
        raise ValueError("Input images must have the same dimensions")

    H, W = im1.shape[:2]  # rn we grab just height and width, we ignore the channel dimension

    # Creating luminance images directly:
    # axis=2 literally again just means "average across the 3 RGB channels" at each pixel
    # So basicaly, luminance_array1[row,col] = (R+G+B)/3 for that pixel
    luminance_array1 = im1.mean(axis=2, dtype=np.float64)
    luminance_array2 = im2.mean(axis=2, dtype=np.float64)

    # Computing the difference luminance map
    difference_luminance = luminance_array1 - luminance_array2

    # Computing the standard deviation of the difference map
    std_deviation_of_difference = difference_luminance.std(ddof=0)

    # Computeing the mean luminance of the first image
    mean_of_luminance_array1 = luminance_array1.mean()

    # Guarding against division by zero (in case we have mean luminance aprox ~ 0)
    eps = 1e-12
    if abs(mean_of_luminance_array1) < eps:
        raise ValueError("Mean luminance of first image is zero or too small")

    # Noise = std of difference / mean luminance of first image
    noise = std_deviation_of_difference / mean_of_luminance_array1
    
    return float(noise)

