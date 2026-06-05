from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet

import os


def generate_pdf(
        student_id,
        performance,
        filename):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        f"Performance Report - {student_id}",
        styles["Title"]
    )

    elements.append(title)

    elements.append(
        Spacer(1,12)
    )

    score_text = Paragraph(
        f"""
        Score : {performance['score']}
        <br/>
        Total Questions : {performance['total']}
        <br/>
        Percentage : {performance['percentage']} %
        """,
        styles["BodyText"]
    )

    elements.append(score_text)

    elements.append(
        Spacer(1,20)
    )

    topic_title = Paragraph(
        "Topic Performance",
        styles["Heading2"]
    )

    elements.append(topic_title)

    for _, row in performance[
        "topic_performance"
    ].iterrows():

        txt = Paragraph(
            f"{row['topic']} : {row['Accuracy']:.2f}%",
            styles["BodyText"]
        )

        elements.append(txt)

    elements.append(
        Spacer(1,20)
    )

    recommendation = Paragraph(
        """
        Recommended Learning Resources

        <br/>
        Python:
        https://docs.python.org

        <br/>
        SQL:
        https://www.w3schools.com/sql

        <br/>
        Data Structures:
        https://www.geeksforgeeks.org
        """,
        styles["BodyText"]
    )

    elements.append(recommendation)

    elements.append(PageBreak())

    doc.build(elements)

    return filename
