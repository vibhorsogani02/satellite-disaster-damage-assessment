
import cv2
import numpy as np


def create_damage_map(image, segmentation_result):

    # Copy original satellite image
    output = image.copy()

    # Get segmentation mask
    mask = segmentation_result["mask"]

    # Find separate affected regions
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    region_details = []

    for index, contour in enumerate(contours):

        area = cv2.contourArea(contour)

        if area < 100:
            continue

        x, y, w, h = cv2.boundingRect(contour)

        # Region size-based visual priority
        if area < 500:
            color = (0, 255, 255)  # Yellow
            priority = "Small Region"

        elif area < 2000:
            color = (0, 165, 255)  # Orange
            priority = "Medium Region"

        else:
            color = (0, 0, 255)  # Red
            priority = "Large Region"

        # Draw affected region
        cv2.drawContours(
            output,
            [contour],
            -1,
            color,
            2
        )

        # Add region number
        cv2.putText(
            output,
            str(index + 1),
            (x, max(y - 5, 15)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

        region_details.append({
            "region": index + 1,
            "area_pixels": int(area),
            "priority": priority,
            "x": int(x),
            "y": int(y),
            "width": int(w),
            "height": int(h)
        })

    return output, region_details
