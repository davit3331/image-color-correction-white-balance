# Image Color Correction using White Balance

This project implements an image color correction pipeline using a white reference region (ROI) to remove color cast from images.

## Overview

Images often appear with unwanted color tint due to lighting conditions:
- Indoor images → yellow/orange tint
- Outdoor images → blue/green tint

This project corrects these distortions by computing per-channel gains based on a selected white reference region.

---

## Method

1. Select a region of interest (ROI) that should be white
2. Compute average RGB values in the ROI
3. Calculate scaling factors for each color channel
4. Apply gains to the entire image
5. Preserve global brightness using normalization

---

## Features

- White balance correction using reference-based scaling
- Noise analysis:
  - Crop-based noise estimation
  - Difference-based noise estimation
- Least squares computation for geometric problems
- End-to-end pipeline with before/after comparison

---

## Results

### Indoor Image
![Indoor Before](preview/indoor_before.jpg)
![Indoor After](preview/indoor_after.jpg)

### Outdoor Image
![Outdoor Before](preview/outdoor_before.jpg)
![Outdoor After](preview/outdoor_after.jpg)

---

## Project Structure
