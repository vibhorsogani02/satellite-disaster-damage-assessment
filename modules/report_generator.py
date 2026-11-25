
from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, Image
)
from PIL import Image as PILImage


def create_pdf_report(
    before_image,
    after_image,
    damage_map,
    classified_regions,
    affected_percentage
):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(
        "Satellite-Based Disaster Damage Assessment",
        styles["Title"]
    ))

    story.append(Spacer(1, 12))

    story.append(Paragraph(
        f"Report Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
        styles["Normal"]
    ))

    story.append(Spacer(1, 15))

    story.append(Paragraph(
        "1. Assessment Summary",
        styles["Heading2"]
    ))

    summary = [
        ["Parameter", "Result"],
        ["Detected Regions", str(len(classified_regions))],
        ["Affected Pixel Percentage", f"{affected_percentage:.2f}%"]
    ]

    table = Table(summary, colWidths=[250, 180])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8)
    ]))

    story.append(table)
    story.append(Spacer(1, 20))

    story.append(Paragraph(
        "2. Damage Classification",
        styles["Heading2"]
    ))

    rows = [["Region", "Area (pixels)", "Category"]]

    for item in classified_regions:
        rows.append([
            str(item["region"]),
            str(item["area_pixels"]),
            item["damage_class"]
        ])

    damage_table = Table(rows, repeatRows=1)

    damage_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 7)
    ]))

    story.append(damage_table)
    story.append(Spacer(1, 20))

    def add_image(title, image_array):
        story.append(Paragraph(title, styles["Heading2"]))

        image_buffer = BytesIO()
        PILImage.fromarray(image_array).save(
            image_buffer, format="PNG"
        )
        image_buffer.seek(0)

        story.append(Image(
            image_buffer,
            width=6 * inch,
            height=3.5 * inch,
            kind="proportional"
        ))
        story.append(Spacer(1, 15))

    add_image("3. Before Disaster Image", before_image)
    add_image("4. After Disaster Image", after_image)
    add_image("5. Damage Visualization Map", damage_map)

    story.append(Paragraph(
        "Note: This report contains prototype image-change "
        "analysis. Results are not verified ground-truth damage "
        "assessments. Pixel area is not equivalent to geographic area.",
        styles["Italic"]
    ))

    doc.build(story)

    buffer.seek(0)
    return buffer.getvalue()
