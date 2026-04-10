import numpy as np 

def noiseAnalCrop(im: np.ndarray, top: int, bottom: int, left: int, right: int) -> float:
    # accoridng to func def, im is expected to be an RGB image of shape (H, W, 3):
    # - H = image height (#rows)
    # - W = image width  (#cols)
    # - 3 = RGB channels
    H, W = im.shape[:2]  # We grab just height and width, rn we ignore the channel dimension
  
    #NEED TO MAKE SURE left < right and top < bottom since NumPy slices dont auto reverse and we dont wanna empty array
    if not (0 <= top < bottom <= H and 0 <= left < right <= W):
        raise ValueError("Invalid ROI bounds: ensure 0 <= top < bottom <= H and 0 <= left < right <= W.")

    # Creating a luminance image from RGB:
    # When we do axis=2 it literally means "take the mean across the RGB channel dimension"
    # so likefor each pixel (row, col), NumPy averages im[row, col, 0], im[row, col, 1], im[row, col, 2]
    # For Exmpl: lets say if pixel = [100,150,200], luminance = (100+150+200)/3 = 150
    # by doing dtype=np.float64 we ensure that we accumulate in float (avoids uint8 overflow)
    luminance_array = im.mean(axis=2, dtype=np.float64)

    # Croping the region of interest (ROI) from the luminance image
    ROI = luminance_array[top:bottom, left:right]

    # Computing the mean luminance in ROI
    n = ROI.size  # number of pixels in ROI
    mean = float(ROI.mean())

    # Computing standard deviation in ROI (population std: divide by n)
    standard_deviation = float(ROI.std(ddof=0))

    # Returning the standard deviation of this luminance image, normalized (divided) by the mean luminance.
    # but we need to Guard against mean ~ 0 to avoid division by zero
    eps = 1e-12
    if abs(mean) < eps:
        raise ValueError("Mean is 0 (or ~0); cannot normalize noise by mean luminance.")

    noise = standard_deviation / mean
    return float(noise)



