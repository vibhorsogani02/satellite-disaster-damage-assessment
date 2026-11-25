
import cv2
import numpy as np


def detect_changes(
    before,
    after,
    threshold_value=30,
    min_area=100
):
    """
    Detect changed regions between two enhanced grayscale images.
    """

    # Ensure both images have same dimensions
    if before.shape != after.shape:
        raise ValueError("Both images must have the same dimensions.")

    # 1. Calculate absolute difference
    difference = cv2.absdiff(before, after)

    # 2. Apply binary thresholding
    _, binary_map = cv2.threshold(
        difference,
        threshold_value,
        255,
        cv2.THRESH_BINARY
    )

    # 3. Remove small noise
    kernel = np.ones((3, 3), np.uint8)

    cleaned_map = cv2.morphologyEx(
        binary_map,
        cv2.MORPH_OPEN,
        kernel
    )

    # 4. Connect nearby changed regions
    cleaned_map = cv2.morphologyEx(
        cleaned_map,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=2
    )

    # 5. Find changed regions
    contours, _ = cv2.findContours(
        cleaned_map,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    final_map = np.zeros_like(cleaned_map)
    detected_regions = []

    for contour in contours:

        area = cv2.contourArea(contour)

        if area >= min_area:

            cv2.drawContours(
                final_map,
                [contour],
                -1,
                255,
                thickness=cv2.FILLED
            )

            x, y, w, h = cv2.boundingRect(contour)

            detected_regions.append({
                "x": int(x),
                "y": int(y),
                "width": int(w),
                "height": int(h),
                "area_pixels": int(area)
            })

    # 6. Calculate changed pixel percentage
    changed_pixels = np.count_nonzero(final_map)
    total_pixels = final_map.size

    changed_percentage = (
        changed_pixels / total_pixels
    ) * 100

    return {
        "difference": difference,
        "change_map": final_map,
        "regions": detected_regions,
        "changed_pixels": int(changed_pixels),
        "changed_percentage": float(changed_percentage)
    }
