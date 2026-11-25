
import cv2
import numpy as np


def assess_image_quality(image):

    # Convert RGB image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # 1. Brightness
    brightness = float(np.mean(gray))

    # 2. Contrast
    contrast = float(np.std(gray))

    # 3. Sharpness
    sharpness = float(
        cv2.Laplacian(gray, cv2.CV_64F).var()
    )

    # Quality warnings
    warnings = []

    if brightness < 40:
        warnings.append("Image is too dark.")

    elif brightness > 220:
        warnings.append("Image is too bright.")

    if contrast < 25:
        warnings.append("Image has low contrast.")

    if sharpness < 50:
        warnings.append("Image may be blurry.")

    quality = "Good" if not warnings else "Needs Review"

    return {
        "brightness": round(brightness, 2),
        "contrast": round(contrast, 2),
        "sharpness": round(sharpness, 2),
        "quality": quality,
        "warnings": warnings
    }
