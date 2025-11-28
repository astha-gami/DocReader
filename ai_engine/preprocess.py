import cv2
import numpy as np

# --------- Convert to Grayscale ---------
def to_gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# --------- Denoise ---------
def denoise(image):
    return cv2.GaussianBlur(image, (3, 3), 0)  # Reduced kernel for speed

# --------- Thresholding (clean black & white) ---------
def threshold(image):
    return cv2.threshold(image, 0, 255,
                         cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# --------- Deskew scanned documents ---------
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    return cv2.warpAffine(image, M, (w, h),
                          flags=cv2.INTER_CUBIC,
                          borderMode=cv2.BORDER_REPLICATE)

# --------- Full Preprocessing Pipeline ---------
def preprocess_image_for_ocr(image):
    gray = to_gray(image)
    clean = denoise(gray)
    thresh = threshold(clean)
    fixed = deskew(thresh)
    return fixed
