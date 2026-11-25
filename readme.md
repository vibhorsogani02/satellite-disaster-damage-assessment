
# 🛰️ Satellite-Based Disaster Damage Assessment System

An interactive satellite image analysis system designed to identify, visualize, and assess changes caused by natural disasters using pre-disaster and post-disaster satellite imagery.

The application uses image processing and computer vision techniques to detect affected regions, estimate affected areas, classify damage severity, and generate assessment reports through an interactive Streamlit dashboard.

## 📌 Project Overview

Natural disasters such as floods, earthquakes, and cyclones can cause significant damage to buildings, infrastructure, and land.

This project provides a satellite-based approach to disaster assessment by comparing satellite images captured before and after a disaster.

The system processes both images, detects changes, identifies affected regions, and presents the results through visual maps, statistical analysis, and downloadable reports.

## ✨ Key Features

- **Satellite Image Upload:** Upload before-disaster and after-disaster satellite images.
- **Image Registration:** Align satellite images to improve comparison accuracy.
- **Image Enhancement:** Improve image quality through normalization and enhancement techniques.
- **Change Detection:** Identify differences between pre-disaster and post-disaster images.
- **Change Sensitivity Control:** Adjust detection thresholds to identify subtle or significant changes.
- **Image Segmentation:** Extract and separate affected regions.
- **Damage Visualization Map:** Highlight detected affected areas using visual overlays.
- **Damage Classification:** Categorize detected regions into damage severity levels.
- **Statistical Analysis:** Calculate changed pixels, affected area percentage, and detected regions.
- **Interactive Dashboard:** Display damage statistics, KPIs, and analytical charts.
- **Image Quality Assessment:** Evaluate brightness, contrast, and sharpness.
- **Before/After Comparison:** Visually compare original satellite images and their differences.
- **PDF Report Generation:** Generate downloadable disaster assessment reports.
- **CSV Export:** Download classified affected-region data.
- **Evaluation Dashboard:** Display available evaluation metrics and confusion matrix visualization.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web dashboard |
| OpenCV | Image processing and computer vision |
| NumPy | Numerical operations and image arrays |
| Matplotlib | Data visualization and charts |
| Pillow (PIL) | Image loading and manipulation |
| Pandas | Tabular data handling |

## ⚙️ Project Workflow

1. Upload pre-disaster and post-disaster satellite images.
2. Register and align both images.
3. Enhance and normalize the images.
4. Perform change detection using image differences and thresholding.
5. Segment the detected affected regions.
6. Generate damage visualization maps.
7. Classify affected regions based on estimated severity.
8. Calculate affected area and other statistical measurements.
9. Display results in the interactive dashboard.
10. Generate PDF reports and export classified data as CSV.

## 📂 Project Structure

```text
satellite-disaster-damage-assessment/
│
├── app.py
│
├── modules/
│   ├── registration.py
│   ├── enhancement.py
│   ├── change_detection.py
│   ├── segmentation.py
│   ├── damage_map.py
│   ├── damage_classification.py
│   ├── report_generator.py
│   ├── analytics.py
│   ├── image_quality.py
│   ├── image_comparison.py
│   ├── evaluation_dashboard.py
│   ├── download_report.py
│   └── styles.py
│
├── outputs/
│
├── .streamlit/
│
├── before.png
├── after.png
│
└── README.md
```

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/vibhorsogani02/satellite-disaster-damage-assessment.git
```

### 2. Navigate to the Project Directory

```bash
cd satellite-disaster-damage-assessment
```

### 3. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate the environment:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install streamlit opencv-python numpy matplotlib pillow pandas reportlab
```

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at:

```text
http://localhost:8501
```

## 🖥️ How to Use

1. Start the Streamlit application.
2. Upload a satellite image captured before the disaster.
3. Upload another satellite image captured after the disaster.
4. Adjust change detection sensitivity and minimum region size.
5. Allow the system to process and compare the images.
6. Explore detected changes, affected regions, and damage statistics.
7. View the damage visualization map and analytical dashboard.
8. Download the generated PDF assessment report or CSV data.

## 📊 Expected Output

The system provides:

- Registered satellite images.
- Enhanced before and after images.
- Difference images and detected change maps.
- Segmented affected regions.
- Damage visualization overlays.
- Damage severity classification.
- Changed pixel count and affected area percentage.
- Statistical charts and dashboard metrics.
- Downloadable PDF and CSV reports.

## 🎯 Applications

- Flood damage assessment.
- Earthquake-affected area identification.
- Cyclone damage monitoring.
- Infrastructure damage analysis.
- Remote sensing and geographical analysis.
- Disaster response and recovery planning.

## ⚠️ Limitations

- The system depends on the quality and alignment of satellite images.
- Clouds, shadows, seasonal variations, and sensor differences may produce false detections.
- Detected image changes do not necessarily represent actual disaster damage.
- Damage severity classifications are estimates and require validation.
- Results should be verified by domain experts before being used for real-world disaster response decisions.

## 🔮 Future Improvements

- Integration of deep learning-based damage segmentation.
- U-Net-based building damage identification.
- More accurate damage severity estimation.
- GIS-based geographical damage visualization.
- Integration of real-time satellite imagery.
- Improved model evaluation using ground-truth datasets.

## 👨‍💻 Author

**Vibhor Jain**

Electronics and Communication Engineering  
Indian Institute of Information Technology (IIIT), Surat

GitHub: [@vibhorsogani02](https://github.com/vibhorsogani02)

---

⭐ If you find this project interesting, consider giving it a star!
