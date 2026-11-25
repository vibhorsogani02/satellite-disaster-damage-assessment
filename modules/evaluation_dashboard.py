
import os
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image


def show_evaluation_dashboard(result, confusion_matrix_path):

    st.subheader("Model Evaluation Dashboard")

    if not isinstance(result, dict):
        st.error("Invalid evaluation data.")
        return

    # Extract values
    changed_pixels = int(result.get("changed_pixels", 0))
    changed_percentage = float(result.get("changed_percentage", 0))
    regions = result.get("regions", [])
    change_map = result.get("change_map")

    total_pixels = (
        int(np.asarray(change_map).size)
        if change_map is not None else 0
    )

    unchanged_pixels = max(total_pixels - changed_pixels, 0)

    # =====================================
    # 1. PERFORMANCE METRICS
    # =====================================

    st.markdown("### 1. Change Detection Performance")

    col1, col2, col3 = st.columns(3)

    col1.metric("Changed Pixels", f"{changed_pixels:,}")
    col2.metric("Changed Area", f"{changed_percentage:.2f}%")
    col3.metric("Detected Regions", len(regions))

    # =====================================
    # 2. IMAGE STATISTICS
    # =====================================

    st.markdown("### 2. Image Statistics")

    col1, col2 = st.columns(2)

    col1.metric("Total Image Pixels", f"{total_pixels:,}")
    col2.metric("Unchanged Pixels", f"{unchanged_pixels:,}")

    # =====================================
    # 3. CHANGE DISTRIBUTION
    # =====================================

    st.markdown("### 3. Change Distribution")

    if total_pixels > 0:

        fig, ax = plt.subplots(figsize=(7, 4))

        ax.bar(
            ["Changed Pixels", "Unchanged Pixels"],
            [changed_pixels, unchanged_pixels]
        )

        ax.set_ylabel("Number of Pixels")
        ax.set_title("Image Change Distribution")

        st.pyplot(fig)
        plt.close(fig)

    else:
        st.info("Image statistics are unavailable.")

    # =====================================
    # 4. CONFUSION MATRIX
    # =====================================

    st.markdown("### 4. Confusion Matrix")

    st.write(
        "Upload the actual Ground Truth Damage Mask "
        "to evaluate the change detection results."
    )

    st.caption(
        "White pixels = Actual damaged/changed areas. "
        "Black pixels = No damage/no change."
    )

    uploaded_mask = st.file_uploader(
        "Upload Ground Truth Mask",
        type=["png", "jpg", "jpeg"],
        key="ground_truth_upload"
    )

    if uploaded_mask is not None and change_map is not None:

        try:
            # Read actual ground truth mask
            ground_truth_image = Image.open(
                uploaded_mask
            ).convert("L")

            y_true = np.asarray(ground_truth_image)

            # Read predicted change map
            predicted_map = np.asarray(change_map)

            if predicted_map.ndim == 3:
                predicted_map = np.mean(
                    predicted_map[:, :, :3],
                    axis=2
                )

            if y_true.shape != predicted_map.shape:

                st.error(
                    "Ground Truth Mask and Change Map "
                    "must have the same image dimensions."
                )

            else:

                # Convert both images into binary masks
                y_true = (y_true > 0).astype(np.uint8)
                y_pred = (predicted_map > 0).astype(np.uint8)

                # Confusion Matrix
                tn = int(np.sum((y_true == 0) & (y_pred == 0)))
                fp = int(np.sum((y_true == 0) & (y_pred == 1)))
                fn = int(np.sum((y_true == 1) & (y_pred == 0)))
                tp = int(np.sum((y_true == 1) & (y_pred == 1)))

                matrix = np.array([
                    [tn, fp],
                    [fn, tp]
                ])

                total = tn + fp + fn + tp

                # Evaluation Metrics
                accuracy = (
                    (tp + tn) / total
                    if total > 0 else 0
                )

                precision = (
                    tp / (tp + fp)
                    if (tp + fp) > 0 else 0
                )

                recall = (
                    tp / (tp + fn)
                    if (tp + fn) > 0 else 0
                )

                f1_score = (
                    2 * precision * recall / (precision + recall)
                    if (precision + recall) > 0 else 0
                )

                st.success("Ground Truth Mask loaded successfully!")

                # Display metrics
                st.markdown("#### Model Performance")

                col1, col2, col3, col4 = st.columns(4)

                col1.metric("Accuracy", f"{accuracy * 100:.2f}%")
                col2.metric("Precision", f"{precision * 100:.2f}%")
                col3.metric("Recall", f"{recall * 100:.2f}%")
                col4.metric("F1-Score", f"{f1_score * 100:.2f}%")

                # Display Confusion Matrix
                st.markdown("#### Confusion Matrix")

                fig, ax = plt.subplots(figsize=(7, 5))

                im = ax.imshow(matrix, cmap="Blues")

                ax.set_title("Confusion Matrix")
                ax.set_xlabel("Predicted Label")
                ax.set_ylabel("Actual Label")

                ax.set_xticks([0, 1])
                ax.set_yticks([0, 1])

                ax.set_xticklabels(["No Change", "Changed"])
                ax.set_yticklabels(["No Change", "Changed"])

                for i in range(2):
                    for j in range(2):
                        ax.text(
                            j,
                            i,
                            str(matrix[i, j]),
                            ha="center",
                            va="center",
                            color="black",
                            fontsize=12
                        )

                fig.colorbar(im, ax=ax)

                st.pyplot(fig)

                # Save confusion matrix
                if confusion_matrix_path:

                    output_dir = os.path.dirname(
                        confusion_matrix_path
                    )

                    if output_dir:
                        os.makedirs(output_dir, exist_ok=True)

                    fig.savefig(
                        confusion_matrix_path,
                        bbox_inches="tight"
                    )

                plt.close(fig)

                st.success(
                    "Confusion Matrix generated successfully!"
                )

                # Explanation
                st.markdown("#### Confusion Matrix Explanation")

                st.write(f"True Negative (TN): {tn}")
                st.write(f"False Positive (FP): {fp}")
                st.write(f"False Negative (FN): {fn}")
                st.write(f"True Positive (TP): {tp}")

        except Exception as e:
            st.error(f"Evaluation Error: {e}")

    elif change_map is None:

        st.warning(
            "Predicted Change Map is not available. "
            "Run change detection first."
        )

    else:

        st.info(
            "Please upload an actual Ground Truth Damage Mask "
            "to generate the Confusion Matrix."
        )

    # =====================================
    # 5. EVALUATION SUMMARY
    # =====================================

    st.markdown("### 5. Evaluation Summary")

    st.write(f"Total Changed Pixels: {changed_pixels:,}")

    st.write(
        f"Changed Area Percentage: {changed_percentage:.2f}%"
    )

    st.write(f"Detected Regions: {len(regions)}")

    st.success("Model Evaluation Dashboard Loaded Successfully!")
