
import cv2
import numpy as np


def compare_images(before, after):

    # Check image dimensions
    if before.shape != after.shape:
        after = cv2.resize(
            after,
            (before.shape[1], before.shape[0])
        )

    # Convert images to grayscale
    before_gray = cv2.cvtColor(
        before, cv2.COLOR_RGB2GRAY
    )

    after_gray = cv2.cvtColor(
        after, cv2.COLOR_RGB2GRAY
    )

    # Calculate absolute difference
    difference = cv2.absdiff(
        before_gray, after_gray
    )

    # Apply threshold
    _, binary_difference = cv2.threshold(
        difference,
        30,
        255,
        cv2.THRESH_BINARY
    )

    # Calculate changed pixels
    changed_pixels = np.count_nonzero(
        binary_difference
    )

    total_pixels = binary_difference.size

    difference_percentage = (
        changed_pixels / total_pixels
    ) * 100

    # Create side-by-side comparison
    comparison = np.hstack((
        before,
        after
    ))

    return {
        "comparison": comparison,
        "difference": difference,
        "binary_difference": binary_difference,
        "difference_percentage": round(
            difference_percentage, 2
        )
    }
