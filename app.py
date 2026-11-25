import os
import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from modules.registration import register_images
from modules.enhancement import enhance_image
from modules.change_detection import detect_changes
from modules.segmentation import segment_affected_areas
from modules.damage_map import create_damage_map
from modules.damage_classification import classify_damage
from modules.report_generator import create_pdf_report
from modules.analytics import create_damage_chart
from modules.image_quality import assess_image_quality
from modules.image_comparison import compare_images
from modules.evaluation_dashboard import show_evaluation_dashboard
from modules.download_report import show_csv_download
from modules.styles import inject_css, apply_chart_theme, render_hero


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Satellite Disaster Damage Assessment",
    page_icon="🛰️",
    layout="wide"
)

inject_css()
apply_chart_theme()
render_hero()

# PREMIUM MISSION CONTROL
with st.sidebar:
    st.markdown("## 🛰️ MISSION CONTROL")
    st.caption("SATELLITE INTELLIGENCE PLATFORM")
    st.markdown("---")
    st.markdown("### ⚙️ Analysis Settings")
    threshold_value = st.slider("Change detection sensitivity", 5, 100, 30, 5,
        help="Lower values detect subtle image changes; higher values are more selective.")
    min_region_area = st.slider("Minimum region size (pixels)", 20, 1000, 100, 20,
        help="Small regions below this area are filtered to reduce noise.")
    st.markdown("---")
    st.markdown("### 🧭 Analysis workflow")
    st.markdown("""
    1. Upload satellite images
    2. Align and enhance imagery
    3. Detect and segment changes
    4. Classify affected regions
    5. Export assessment reports
    """)
    st.markdown("---")
    st.markdown("### 📌 About this system")
    st.caption("An academic remote-sensing prototype. Detected changes require human verification before being treated as confirmed damage.")

st.markdown("""
<div class="status-ribbon">
  <span class="status-dot"></span><span>DISASTER INTELLIGENCE</span>
  <span class="ribbon-separator">/</span><span>REMOTE SENSING ANALYTICS</span>
  <span class="ribbon-spacer"></span><span class="live-label">● READY FOR ANALYSIS</span>
</div>
""", unsafe_allow_html=True)


# ==========================================
# IMAGE UPLOAD
# ==========================================

upload_col1, upload_col2 = st.columns(2)

with upload_col1:
    before_file = st.file_uploader(
        "📷 Upload Before Disaster Image",
        type=["png", "jpg", "jpeg"],
        key="before_image"
    )

with upload_col2:
    after_file = st.file_uploader(
        "📷 Upload After Disaster Image",
        type=["png", "jpg", "jpeg"],
        key="after_image"
    )


# ==========================================
# MAIN PROCESSING
# ==========================================

if before_file is not None and after_file is not None:

    try:

        # Read images
        before = np.array(
            Image.open(before_file).convert("RGB")
        )

        after = np.array(
            Image.open(after_file).convert("RGB")
        )

        # ======================================
        # 1. ORIGINAL IMAGES
        # ======================================

        st.header("1. Original Images")

        col1, col2 = st.columns(2)

        with col1:
            st.image(
                before,
                caption="Before Disaster",
                use_container_width=True
            )

        with col2:
            st.image(
                after,
                caption="After Disaster",
                use_container_width=True
            )

        # ======================================
        # 2. IMAGE REGISTRATION
        # ======================================

        st.header("2. Image Registration")

        registered_after, success, message = register_images(
            before,
            after
        )

        if not success:
            st.error(message)
            st.stop()

        st.success(message)

        st.image(
            registered_after,
            caption="Registered After Image",
            use_container_width=True
        )

        # ======================================
        # 3. IMAGE ENHANCEMENT
        # ======================================

        st.header("3. Image Enhancement")

        result_before = enhance_image(before)
        result_after = enhance_image(registered_after)

        norm_before = result_before["normalized"]
        norm_after = result_after["normalized"]

        col1, col2 = st.columns(2)

        with col1:
            st.image(
                norm_before,
                caption="Enhanced Before Image",
                use_container_width=True
            )

        with col2:
            st.image(
                norm_after,
                caption="Enhanced After Image",
                use_container_width=True
            )

        # ======================================
        # 4. CHANGE DETECTION
        # ======================================

        st.header("4. Advanced Change Detection")

        result = detect_changes(
            norm_before,
            norm_after,
            threshold_value=threshold_value,
            min_area=min_region_area
        )

        st.image(
            result["difference"],
            caption="Absolute Difference Image",
            use_container_width=True
        )

        st.image(
            result["change_map"],
            caption="Detected Changed Regions",
            use_container_width=True
        )

        # Change overlay
        overlay = registered_after.copy()

        contours, _ = cv2.findContours(
            np.asarray(result["change_map"], dtype=np.uint8),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        cv2.drawContours(
            overlay,
            contours,
            -1,
            (255, 0, 0),
            2
        )

        st.image(
            overlay,
            caption="Changed Regions Highlighted",
            use_container_width=True
        )

        # ======================================
        # 5. CHANGE DETECTION STATISTICS
        # ======================================

        st.header("5. Change Detection Statistics")

        col1, col2 = st.columns(2)

        col1.metric(
            "Changed Pixels",
            f'{result["changed_pixels"]:,}'
        )

        col2.metric(
            "Changed Pixel Percentage",
            f'{result["changed_percentage"]:.2f}%'
        )

        st.write(
            "Detected Regions:",
            len(result["regions"])
        )

        # ======================================
        # 6. IMAGE SEGMENTATION
        # ======================================

        st.header("6. Image Segmentation")

        segmentation = segment_affected_areas(
            result["change_map"],
            min_area=min_region_area
        )

        col1, col2 = st.columns(2)

        with col1:
            st.image(
                segmentation["mask"],
                caption="Segmented Affected Areas",
                use_container_width=True
            )

        with col2:
            st.image(
                registered_after,
                caption="After Disaster Image",
                use_container_width=True
            )

        # Segmentation overlay
        segmentation_overlay = registered_after.copy()

        mask = np.asarray(segmentation["mask"]) > 0

        red_color = np.array([255, 0, 0])

        segmentation_overlay[mask] = (
            0.5 * segmentation_overlay[mask].astype(np.float32)
            + 0.5 * red_color
        ).astype(np.uint8)

        st.image(
            segmentation_overlay,
            caption="Affected Areas Highlighted",
            use_container_width=True
        )

        # ======================================
        # 7. SEGMENTATION STATISTICS
        # ======================================

        st.header("7. Segmentation Statistics")

        col1, col2 = st.columns(2)

        col1.metric(
            "Affected Pixels",
            f'{segmentation["affected_pixels"]:,}'
        )

        col2.metric(
            "Affected Area Percentage",
            f'{segmentation["affected_percentage"]:.2f}%'
        )

        st.write(
            "Separate Affected Regions:",
            len(segmentation["regions"])
        )

        # ======================================
        # 8. DAMAGE VISUALIZATION MAP
        # ======================================

        st.header("8. Damage Visualization Map")

        damage_map, region_details = create_damage_map(
            registered_after,
            segmentation
        )

        st.image(
            damage_map,
            caption="Affected Regions Visualization",
            use_container_width=True
        )

        st.subheader("Affected Region Details")

        if region_details:
            st.dataframe(
                region_details,
                use_container_width=True
            )
        else:
            st.warning("No affected regions detected.")

        # ======================================
        # 9. DAMAGE CLASSIFICATION
        # ======================================

        st.header("9. Damage Classification")

        classified_regions = classify_damage(region_details)

        # CSV DOWNLOAD FEATURE
        st.subheader("Download Classified Regions (CSV)")

        show_csv_download(classified_regions)

        damage_counts = {}

        if classified_regions:

            st.dataframe(
                classified_regions,
                use_container_width=True
            )

            for item in classified_regions:

                category = item["damage_class"]

                damage_counts[category] = (
                    damage_counts.get(category, 0) + 1
                )

            st.subheader("Damage Category Summary")

            for category, count in damage_counts.items():
                st.write(f"**{category}:** {count} regions")

        else:
            st.warning(
                "No regions available for classification."
            )

        # PREMIUM EXECUTIVE OVERVIEW
        st.markdown('<div class="section-kicker">COMMAND CENTER / LIVE RESULTS</div>', unsafe_allow_html=True)
        st.header("Executive Damage Overview")
        total_regions = len(classified_regions)
        severe_count = sum(1 for item in classified_regions if str(item.get("damage_class", "")).lower() in ("severe", "high", "critical", "destroyed"))
        moderate_count = sum(1 for item in classified_regions if str(item.get("damage_class", "")).lower() in ("moderate", "medium", "major damage"))
        low_count = max(0, total_regions - severe_count - moderate_count)
        kpi_html = f"""
        <div class="kpi-grid">
          <div class="kpi-card"><div class="kpi-label">AFFECTED AREA</div><div class="kpi-value">{float(segmentation['affected_percentage']):.2f}<span>%</span></div><div class="kpi-foot">Of analyzed image pixels</div></div>
          <div class="kpi-card"><div class="kpi-label">DETECTED REGIONS</div><div class="kpi-value">{total_regions:,}</div><div class="kpi-foot">Segmented candidate regions</div></div>
          <div class="kpi-card"><div class="kpi-label">HIGH / SEVERE</div><div class="kpi-value">{severe_count:,}</div><div class="kpi-foot">Regions flagged for review</div></div>
          <div class="kpi-card"><div class="kpi-label">CHANGE PIXELS</div><div class="kpi-value">{int(result['changed_pixels']):,}</div><div class="kpi-foot">Pixels differing between images</div></div>
        </div>
        """
        st.markdown(kpi_html, unsafe_allow_html=True)
        left_summary, right_summary = st.columns([1.25, 1])
        with left_summary:
            st.markdown("#### Damage severity snapshot")
            if total_regions:
                for label, count, color in [("High / Severe", severe_count, "#fb7185"), ("Moderate", moderate_count, "#fbbf24"), ("Low / Other", low_count, "#34d399")]:
                    pct = (count / total_regions) * 100
                    st.markdown(f'<div class="severity-row"><div class="severity-head"><span>{label}</span><strong>{count} regions · {pct:.1f}%</strong></div><div class="severity-track"><div class="severity-fill" style="width:{pct:.1f}%;background:{color};"></div></div></div>', unsafe_allow_html=True)
            else:
                st.info("No candidate regions were found with the current settings.")
        with right_summary:
            st.markdown("#### Analysis configuration")
            st.markdown(f'<div class="info-panel"><div><span>Detection threshold</span><strong>{threshold_value}</strong></div><div><span>Minimum region size</span><strong>{min_region_area:,} px</strong></div><div><span>Image dimensions</span><strong>{before.shape[1]} × {before.shape[0]}</strong></div><div><span>Registration</span><strong>Completed</strong></div></div>', unsafe_allow_html=True)
        st.caption("These are image-change indicators, not ground-truth damage labels. Clouds, shadows, seasonal changes, image misalignment and sensor differences can create false positives.")

        st.success(
            "Image Processing, Segmentation, Damage Mapping "
            "and Classification Completed!"
        )

        # ======================================
        # 10. PDF ASSESSMENT REPORT
        # ======================================

        st.divider()

        st.header("10. Download Assessment Report")

        if st.button("Generate PDF Report", type="primary"):

            with st.spinner("Generating PDF Report..."):

                pdf_data = create_pdf_report(
                    before,
                    registered_after,
                    damage_map,
                    classified_regions,
                    segmentation["affected_percentage"]
                )

            st.download_button(
                label="Download PDF Report",
                data=pdf_data,
                file_name="Disaster_Assessment_Report.pdf",
                mime="application/pdf"
            )

        # ======================================
        # 11. DISASTER ANALYTICS DASHBOARD
        # ======================================

        st.divider()

        st.header("11. Disaster Analytics Dashboard")

        if classified_regions:

            chart, category_counts = create_damage_chart(
                classified_regions
            )

            st.pyplot(chart)

            st.subheader("Damage Category Statistics")

            col1, col2 = st.columns(2)

            col1.metric(
                "Total Detected Regions",
                len(classified_regions)
            )

            col2.metric(
                "Affected Pixel Percentage",
                f'{segmentation["affected_percentage"]:.2f}%'
            )

            st.subheader("Damage Classification Summary")

            for category, count in category_counts.items():
                st.write(f"**{category}:** {count}")

        else:
            st.info(
                "No affected regions available for analysis."
            )

        # ======================================
        # 12. SATELLITE IMAGE QUALITY CHECK
        # ======================================

        st.divider()

        st.header("12. Satellite Image Quality Check")

        st.write(
            "Check brightness, contrast and sharpness "
            "of Before and After Disaster Images."
        )

        before_quality = assess_image_quality(before)
        after_quality = assess_image_quality(after)

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Before Disaster Image")

            st.metric(
                "Brightness",
                before_quality["brightness"]
            )

            st.metric(
                "Contrast",
                before_quality["contrast"]
            )

            st.metric(
                "Sharpness",
                before_quality["sharpness"]
            )

            st.write("Status:", before_quality["quality"])

            for warning in before_quality["warnings"]:
                st.warning(warning)

            if not before_quality["warnings"]:
                st.success("No major quality warning detected.")

        with col2:

            st.subheader("After Disaster Image")

            st.metric(
                "Brightness",
                after_quality["brightness"]
            )

            st.metric(
                "Contrast",
                after_quality["contrast"]
            )

            st.metric(
                "Sharpness",
                after_quality["sharpness"]
            )

            st.write("Status:", after_quality["quality"])

            for warning in after_quality["warnings"]:
                st.warning(warning)

            if not after_quality["warnings"]:
                st.success("No major quality warning detected.")

        # ======================================
        # 13. BEFORE AND AFTER IMAGE COMPARISON
        # ======================================

        st.divider()

        st.header("13. Before and After Image Comparison")

        comparison_result = compare_images(before, after)

        st.image(
            comparison_result["comparison"],
            caption="Before and After Comparison",
            use_container_width=True
        )

        st.image(
            comparison_result["difference"],
            caption="Difference Image",
            use_container_width=True,
            clamp=True
        )

        st.metric(
            "Image Difference",
            f'{float(comparison_result["difference_percentage"]):.2f}%'
        )

        # ======================================
        # 14. MODEL EVALUATION DASHBOARD
        # ======================================

        st.divider()

        st.header("14. Model Evaluation Dashboard")

        st.write(
            "Evaluate disaster change detection results "
            "using available performance metrics."
        )

        os.makedirs("outputs", exist_ok=True)

        show_evaluation_dashboard(
            result,
            "outputs/confusion_matrix.png"
        )

        # ======================================
        # FINAL MESSAGE
        # ======================================

        st.divider()

        st.success(
            "Disaster Damage Assessment Completed Successfully!"
        )

        st.caption(
            "Note: This is an image-based change detection system. "
            "Detected changes are not necessarily confirmed disaster damage."
        )

    except Exception as e:

        st.error(
            f"An error occurred during image processing: {e}"
        )

        st.exception(e)

else:

    st.info(
        "Please upload both Before and After Disaster "
        "satellite images to start the assessment."
    )

    st.write(
        "Supported formats: PNG, JPG, JPEG"
    )