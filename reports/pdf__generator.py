from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

import os

REPORT_DIR = "reports"

os.makedirs(REPORT_DIR, exist_ok=True)


def generate_pdf(student_id, performance):

    pdf_path = os.path.join(
        REPORT_DIR,
        f"{student_id}_Report.pdf"
    )

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "Mock Test Performance Report",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            f"Student ID : {student_id}",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 10))

    summary_data = [
        ["Metric", "Value"],
        ["Score", performance["score"]],
        ["Total Questions", performance["total"]],
        ["Percentage", f"{performance['percentage']}%"]
    ]

    summary_table = Table(summary_data)

    summary_table.setStyle(
        TableStyle([
            ('BACKGROUND',(0,0),(-1,0),colors.lightblue),
            ('GRID',(0,0),(-1,-1),1,colors.black)
        ])
    )

    elements.append(summary_table)

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "Topic Wise Performance",
            styles["Heading2"]
        )
    )

    topic_data = [
        ["Topic","Accuracy"]
    ]

    for _, row in performance[
        "topic_performance"
    ].iterrows():

        topic_data.append([
            row["topic"],
            f"{row['Accuracy']:.2f}%"
        ])

    topic_table = Table(topic_data)

    topic_table.setStyle(
        TableStyle([
            ('BACKGROUND',(0,0),(-1,0),colors.lightgreen),
            ('GRID',(0,0),(-1,-1),1,colors.black)
        ])
    )

    elements.append(topic_table)

    elements.append(Spacer(1,20))

    elements.append(
        Paragraph(
            "Recommended Learning Resources",
            styles["Heading2"]
        )
    )

    resources = """
    Python - https://docs.python.org<br/>
    SQL - https://www.w3schools.com/sql<br/>
    DBMS - https://www.javatpoint.com/dbms-tutorial<br/>
    Data Structures - https://www.geeksforgeeks.org/data-structures/<br/>
    Aptitude - https://www.indiabix.com
    """

    elements.append(
        Paragraph(
            resources,
            styles["BodyText"]
        )
    )

    elements.append(PageBreak())

    doc.build(elements)

    return pdf_path
