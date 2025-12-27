
import io
import cv2
import numpy as np
import streamlit as st
from PIL import Image

st.set_page_config(page_title="Lab-03: Image Enhancing", layout="wide")

st.title("🧪 Lab-03: Image Enhancing")
st.markdown(
    """
Upload a color image, then apply **Denoising/Smoothing**, **Sharpening**, and **Edge Detection**
with **Sobel, Prewitt, and Canny** filters.
"""
)

# ---------- Helper functions ----------
def to_cv2(img_pil: Image.Image) -> np.ndarray:
    """PIL RGB -> OpenCV BGR uint8"""
    arr = np.array(img_pil.convert("RGB"))
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

def to_pil(img_bgr: np.ndarray) -> Image.Image:
    """OpenCV BGR/GRAY -> PIL RGB"""
    if len(img_bgr.shape) == 2:
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_GRAY2RGB)
    else:
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img_rgb)

def ensure_odd(k: int) -> int:
    """Ensure kernel size is odd and >= 1."""
    k = int(k)
    if k < 1:
        k = 1
    if k % 2 == 0:
        k += 1
    return k

def prewitt_edges(gray: np.ndarray) -> np.ndarray:
    # Prewitt kernels
    kx = np.array([[-1, 0, 1],
                   [-1, 0, 1],
                   [-1, 0, 1]], dtype=np.float32)
    ky = np.array([[ 1,  1,  1],
                   [ 0,  0,  0],
                   [-1, -1, -1]], dtype=np.float32)
    gx = cv2.filter2D(gray, cv2.CV_32F, kx)
    gy = cv2.filter2D(gray, cv2.CV_32F, ky)
    mag = cv2.magnitude(gx, gy)
    mag = np.clip((mag / (mag.max() + 1e-6)) * 255, 0, 255).astype(np.uint8)
    return mag

def sharpen_image(img_bgr: np.ndarray, method: str, ksize: int, amount: float, sigma: float) -> np.ndarray:
    if method == "Unsharp Masking":
        ksize = ensure_odd(ksize)
        blurred = cv2.GaussianBlur(img_bgr, (ksize, ksize), sigmaX=sigma)
        # unsharp = (1 + amount) * img - amount * blurred
        unsharp = cv2.addWeighted(img_bgr, 1 + amount, blurred, -amount, 0)
        return np.clip(unsharp, 0, 255).astype(np.uint8)
    else:
        # Simple Laplacian kernel based sharpen
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]], dtype=np.float32)
        sharp = cv2.filter2D(img_bgr, -1, kernel)
        return np.clip(sharp, 0, 255).astype(np.uint8)

# ---------- Sidebar controls ----------
st.sidebar.header("⚙️ Controls")

# Smoothing controls
smooth_method = st.sidebar.selectbox(
    "Denoising / Smoothing method",
    ["Gaussian Blur", "Median Blur", "Bilateral Filter"],
    index=0
)

sm_ksize = st.sidebar.slider("Kernel size (odd)", min_value=1, max_value=31, value=5, step=2)
sm_sigma = st.sidebar.slider("Gaussian Sigma (for Gaussian)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
bilateral_sigma_color = st.sidebar.slider("Bilateral σColor", min_value=1, max_value=200, value=75, step=1)
bilateral_sigma_space = st.sidebar.slider("Bilateral σSpace", min_value=1, max_value=200, value=75, step=1)

# Sharpen controls
sh_method = st.sidebar.selectbox(
    "Sharpening method",
    ["Unsharp Masking", "Laplacian Kernel"],
    index=0
)
sh_ksize = st.sidebar.slider("Unsharp: Gaussian kernel size (odd)", min_value=1, max_value=31, value=5, step=2)
sh_sigma = st.sidebar.slider("Unsharp: Gaussian sigma", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
sh_amount = st.sidebar.slider("Unsharp: amount", min_value=0.0, max_value=3.0, value=1.0, step=0.05)

# Edge detection controls
sobel_ksize = st.sidebar.selectbox("Sobel kernel size", options=[1, 3, 5, 7], index=1)
canny_t1 = st.sidebar.slider("Canny threshold1", min_value=0, max_value=255, value=100, step=1)
canny_t2 = st.sidebar.slider("Canny threshold2", min_value=0, max_value=255, value=200, step=1)

uploaded = st.file_uploader("📤 Upload an image...", type=["png", "jpg", "jpeg", "bmp", "tiff"])

if uploaded is not None:
    # Read the uploaded file
    file_bytes = uploaded.read()
    pil_img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    img_bgr = to_cv2(pil_img)

    # ----- Smoothing -----
    if smooth_method == "Gaussian Blur":
        k = ensure_odd(sm_ksize)
        smoothed = cv2.GaussianBlur(img_bgr, (k, k), sigmaX=sm_sigma)
    elif smooth_method == "Median Blur":
        k = ensure_odd(sm_ksize)
        smoothed = cv2.medianBlur(img_bgr, k)
    else:
        # Bilateral
        d = ensure_odd(sm_ksize)
        smoothed = cv2.bilateralFilter(img_bgr, d=d, sigmaColor=bilateral_sigma_color, sigmaSpace=bilateral_sigma_space)

    # ----- Sharpening -----
    sharpened = sharpen_image(smoothed, sh_method, sh_ksize, sh_amount, sh_sigma)

    # ----- Grayscale for edges -----
    gray = cv2.cvtColor(sharpened, cv2.COLOR_BGR2GRAY)

    # ----- Sobel -----
    sobelx = cv2.Sobel(gray, cv2.CV_16S, 1, 0, ksize=sobel_ksize)
    sobely = cv2.Sobel(gray, cv2.CV_16S, 0, 1, ksize=sobel_ksize)
    sobel = cv2.addWeighted(cv2.convertScaleAbs(sobelx), 0.5, cv2.convertScaleAbs(sobely), 0.5, 0)

    # ----- Prewitt -----
    prew = prewitt_edges(gray)

    # ----- Canny -----
    canny = cv2.Canny(gray, canny_t1, canny_t2)

    # ----- Display layout -----
    st.subheader("📸 Inputs and Intermediate Results")
    c1, c2, c3 = st.columns(3, gap="small")
    with c1:
        st.caption("Original")
        st.image(pil_img, use_column_width=True)
    with c2:
        st.caption(f"Smoothing: {smooth_method}")
        st.image(to_pil(smoothed), use_column_width=True)
    with c3:
        st.caption(f"Sharpening: {sh_method}")
        st.image(to_pil(sharpened), use_column_width=True)

    st.subheader("🧭 Edge Detection Results")
    e1, e2, e3 = st.columns(3, gap="small")
    with e1:
        st.caption(f"Sobel (ksize={sobel_ksize})")
        st.image(to_pil(sobel), use_column_width=True)
    with e2:
        st.caption("Prewitt")
        st.image(to_pil(prew), use_column_width=True)
    with e3:
        st.caption(f"Canny (t1={canny_t1}, t2={canny_t2})")
        st.image(to_pil(canny), use_column_width=True)

    # ----- Downloads -----
    st.subheader("⬇️ Download Results")
    col_d1, col_d2, col_d3, col_d4 = st.columns(4)
    with col_d1:
        st.download_button("Download Smoothing", data=cv2.imencode(".png", smoothed)[1].tobytes(),
                           file_name="smoothed.png", mime="image/png")
    with col_d2:
        st.download_button("Download Sharpened", data=cv2.imencode(".png", sharpened)[1].tobytes(),
                           file_name="sharpened.png", mime="image/png")
    with col_d3:
        st.download_button("Download Edges (Sobel)", data=cv2.imencode(".png", sobel)[1].tobytes(),
                           file_name="edges_sobel.png", mime="image/png")
    with col_d4:
        st.download_button("Download Edges (Prewitt)", data=cv2.imencode(".png", prew)[1].tobytes(),
                           file_name="edges_prewitt.png", mime="image/png")

    st.download_button("Download Edges (Canny)", data=cv2.imencode(".png", canny)[1].tobytes(),
                       file_name="edges_canny.png", mime="image/png")

else:
    st.info("Upload an image to begin.")

st.markdown("---")
st.markdown("Developed for **Lab-03: Image Enhancing** · OpenCV + Streamlit")
