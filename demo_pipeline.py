# Q3b_make_pdf.py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages


from whiteBalance import whiteBalance   # <-- change if your function lives elsewhere

def read_rgb(path):
    im = mpimg.imread(path)
    # Drop alpha if present
    if im.ndim == 3 and im.shape[2] == 4:
        im = im[:, :, :3]
    # Ensure float64
    im = im.astype(np.float64, copy=False)
    # Normalize if looks like 8/16-bit
    if im.max() > 1.0:
        denom = 255.0 if im.max() <= 255.0 else 65535.0
        im = im / denom
    return im

def pick_roi(img, title="Click top-left then bottom-right of the paper"):
    plt.figure()
    plt.imshow(img)
    plt.title(title)
    plt.axis('image')
    pts = plt.ginput(2, timeout=0)  # unlimited time
    plt.close()
    if len(pts) != 2:
        raise RuntimeError("Need exactly two clicks (top-left and bottom-right).")
    (x1, y1), (x2, y2) = pts
    top, bottom  = int(min(y1, y2)), int(max(y1, y2))
    left, right  = int(min(x1, x2)), int(max(x1, x2))
    # quick visual confirm box (optional)
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.add_patch(plt.Rectangle((left, top), right-left, bottom-top,
                               fill=False, linewidth=2))
    ax.set_title(f"ROI: top={top}, bottom={bottom}, left={left}, right={right}")
    plt.show(block=False); plt.pause(1.0); plt.close(fig)
    return top, bottom, left, right

def make_pdf(indoor_before, indoor_after, outdoor_before, outdoor_after, pdf_path="Q3b.pdf"):
    with PdfPages(pdf_path) as pdf:
        fig = plt.figure(figsize=(8.5, 11))  # US Letter portrait
        # 2x2 grid of images
        axes = [fig.add_subplot(2,2,i+1) for i in range(4)]
        for ax, im, title in zip(
            axes,
            [indoor_before, indoor_after, outdoor_before, outdoor_after],
            ["Indoor - Before", "Indoor - After", "Outdoor - Before", "Outdoor - After"]
        ):
            ax.imshow(np.clip(im, 0, 1))
            ax.set_title(title, fontsize=10)
            ax.axis('off')

        # Comment 
        comment = (
            ""
            "The white-paper ROI gray-balancing markedly reduces color casts. For the outdoor image," 
            "it corrects the sky and grass tint, making the overall scene appear whiter. For the indoor image,"
            "it removes the yellowish light from the paper. I think the algorithm is very useful since it"
            " successfully makes the images look whiter. However, the reference is crucial for the algorithm to"
            "work; it can be unreliable if the reference is not truly white or is unevenly lit."
        )
        fig.text(0.05, 0.02, comment, ha='left', va='bottom', fontsize=10, wrap=True)
        fig.tight_layout(rect=[0.03, 0.1, 0.97, 0.97])
        pdf.savefig(fig, dpi=250)
        plt.close(fig)

def main():
    # ---- filenames ----
    indoor_path  = "indoor.png"
    outdoor_path = "outdoor.png"

    indoor = read_rgb(indoor_path)
    outdoor = read_rgb(outdoor_path)

    # ---- pick ROIs by clicking on the white paper in each image ----
    print("Select ROI for OUTDOOR image...")
    top_out, bottom_out, left_out, right_out = pick_roi(outdoor, "OUTDOOR: click top-left, then bottom-right")

    print("Select ROI for INDOOR image...")
    top_in, bottom_in, left_in, right_in = pick_roi(indoor, "INDOOR: click top-left, then bottom-right")

    # ---- run white balance ----
    indoor_after  = whiteBalance(indoor,  top_in,  bottom_in,  left_in,  right_in)
    outdoor_after = whiteBalance(outdoor, top_out, bottom_out, left_out, right_out)

    # ---- save quick PNGs (optional, for your records) ----
    plt.imsave("indoor_before.png",  np.clip(indoor, 0, 1))
    plt.imsave("indoor_after.png",   np.clip(indoor_after, 0, 1))
    plt.imsave("outdoor_before.png", np.clip(outdoor, 0, 1))
    plt.imsave("outdoor_after.png",  np.clip(outdoor_after, 0, 1))

    # ---- building the one-page PDF ----
    make_pdf(indoor, indoor_after, outdoor, outdoor_after, pdf_path="Q3b.pdf")
    print("Wrote Q3b.pdf")

if __name__ == "__main__":
    # If ginput doesn't pop up in VS Code, run from the terminal:
    #   demo_pipeline.py
    # If your backend complains, you can uncomment the next two lines:
    # import matplotlib
    # matplotlib.use("TkAgg")
    main()
