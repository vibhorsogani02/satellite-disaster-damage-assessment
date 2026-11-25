
import cv2
import numpy as np


def segment_affected_areas(change_map, min_area=100):

    # Ensure grayscale image
    if len(change_map.shape) == 3:
        gray = cv2.cvtColor(
            change_map,
            cv2.COLOR_RGB2GRAY
        )
    else:
        gray = change_map.copy()

    # Binary segmentation
    _, binary = cv2.threshold(
        gray,
        127,
        255,
        cv2.THRESH_BINARY
    )

    # Remove small noise
    kernel = np.ones((3, 3), np.uint8)

    opened = cv2.morphologyEx(
        binary,
        cv2.MORPH_OPEN,
        kernel,
        iterations=1
    )

    # Fill small gaps
    cleaned = cv2.morphologyEx(
        opened,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=2
    )

    # Find separate affected regions
    contours, _ = cv2.findContours(
        cleaned,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # Create final segmentation mask
    mask = np.zeros_like(cleaned)

    regions = []

    for contour in contours:

        area = cv2.contourArea(contour)

        if area >= min_area:

            cv2.drawContours(
                mask,
                [contour],
                -1,
                255,
                cv2.FILLED
            )

            x, y, w, h = cv2.boundingRect(contour)

            regions.append({
                "x": int(x),
                "y": int(y),
                "width": int(w),
                "height": int(h),
                "area_pixels": int(area)
            })

    total_pixels = mask.size
    affected_pixels = np.count_nonzero(mask)

    affected_percentage = (
        affected_pixels / total_pixels
    ) * 100

    return {
        "mask": mask,
        "regions": regions,
        "affected_pixels": int(affected_pixels),
        "affected_percentage": float(affected_percentage)
    }
