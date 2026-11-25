import cv2
import numpy as np


def register_images(before, after):

    # Convert RGB images into grayscale
    gray_before = cv2.cvtColor(
        before, cv2.COLOR_RGB2GRAY
    )

    gray_after = cv2.cvtColor(
        after, cv2.COLOR_RGB2GRAY
    )

    # ORB feature detector
    orb = cv2.ORB_create(nfeatures=3000)

    kp1, des1 = orb.detectAndCompute(gray_before, None)
    kp2, des2 = orb.detectAndCompute(gray_after, None)

    if des1 is None or des2 is None:
        return None, False, "Features not detected."

    # Feature matching
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)

    matches = matcher.knnMatch(des1, des2, k=2)

    # Lowe's ratio test
    good_matches = []

    for pair in matches:
        if len(pair) == 2:
            m, n = pair
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)

    if len(good_matches) < 10:
        return None, False, "Not enough matching features."

    # Find matching coordinates
    points_before = np.float32([
        kp1[m.queryIdx].pt for m in good_matches
    ]).reshape(-1, 1, 2)

    points_after = np.float32([
        kp2[m.trainIdx].pt for m in good_matches
    ]).reshape(-1, 1, 2)

    # Calculate Homography
    H, mask = cv2.findHomography(
        points_after,
        points_before,
        cv2.RANSAC,
        5.0
    )

    if H is None:
        return None, False, "Image alignment failed."

    inliers = int(mask.ravel().sum())

    if inliers < 8:
        return None, False, "Reliable alignment not found."

    # Align after image with before image
    height, width = before.shape[:2]

    registered_after = cv2.warpPerspective(
        after,
        H,
        (width, height)
    )

    return (
        registered_after,
        True,
        f"Alignment successful. Matches: {len(good_matches)}, Inliers: {inliers}"
    )
