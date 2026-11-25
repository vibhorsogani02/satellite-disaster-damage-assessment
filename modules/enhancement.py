import cv2

def enhance_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    normalized = cv2.normalize(
        gray, None, 0, 255, cv2.NORM_MINMAX
    )

    return {
        "normalized": normalized
    }