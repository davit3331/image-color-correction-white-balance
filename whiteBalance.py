import numpy as np

def whiteBalance(imin, top, bottom, left, right) -> np.ndarray:

    # --- 0) Convert to float (double) immediately to avoid overflow/rounding ---
    im = imin.astype(np.float64, copy=True)
    
    H, W = imin.shape[0:2]

    if not (0 <= top < bottom <= H and 0 <= left < right <= W):
        raise ValueError("Invalid ROI bounds: ensure 0 <= top < bottom <= H and 0 <= left < right <= W.")

    ###Finding Lo - the old luminance - in the entire image. Could do it by loop but this way is faster
    eps = 1e-12
    L0 = (im[:,:, 0].mean() + im[:,:, 1].mean() + im[:,:, 2].mean()) / 3.0
    if abs(L0) < eps:
        raise ValueError("Global mean luminance is aprox 0; brightness preserving step is ill-defined.")
    
    ## the region of interest
    ROI = im[top:bottom, left:right, :]

    ##average red, green and blue in region of interest
    avg_R_in_ROI = ROI[:, :, 0].mean()
    avg_G_in_ROI = ROI[:, :, 1].mean() 
    avg_B_in_ROI = ROI[:, :, 2].mean() 

    if abs(avg_R_in_ROI) < eps or abs(avg_G_in_ROI) < eps or abs(avg_B_in_ROI) < eps:
        raise ValueError("ROI channel mean is aprox 0; cannot compute stable white balance gains.")

    avg_luminance_t = (avg_G_in_ROI + avg_R_in_ROI + avg_B_in_ROI) / 3.0

    #calculating the gains for each color
    gains_Ro = avg_luminance_t / avg_R_in_ROI
    gains_Go = avg_luminance_t / avg_G_in_ROI
    gains_Bo = avg_luminance_t / avg_B_in_ROI

    # new global luminance if the gains were applied 
    avg_R_in_im = im[:,:, 0].mean()
    avg_G_in_im = im[:,:, 1].mean()
    avg_B_in_im = im[:, :, 2].mean()
    L1 = (gains_Ro * avg_R_in_im + gains_Go * avg_G_in_im + gains_Bo * avg_B_in_im) / 3.0

    if abs(L1) < eps:
        raise ValueError("Predicted post-gain luminance is aprox 0; cannot rescale to preserve brightness.")

    #the question specifies that the birghtness should not be changed, so we need an s factor to restor the brightness
    s = L0 / L1

    gains_R = gains_Ro * s
    gains_B = gains_Bo * s
    gains_G = gains_Go * s

    im[:, :, 0] = im[:, :, 0] * gains_R
    im[:, :, 1] = im[:, :, 1] * gains_G
    im[:, :, 2] = im[:, :, 2] * gains_B

    return im




