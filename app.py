import os

if not os.path.exists("database/assessment.db"):
    exec(open("database/create_db.py").read())
import streamlit as st

from modules.db_operations import (
    load_student_submissions,
    load_question_bank,
    get_students
)

from modules.analytics import (
    calculate_difficulty_index,
    topic_analysis,
    student_performance
)

from modules.charts import (
    topic_chart,
    difficulty_chart
)

from modules.pdf_generator import (
    generate_pdf
)

import tempfile


st.set_page_config(
    page_title="Mock Test Insights Engine",
    layout="wide"
)

st.title(
    "📊 Automated Mock Test Insights Engine"
)

submissions = load_student_submissions()
questions = load_question_bank()

students = get_students()

selected_student = st.selectbox(
    "Select Student",
    students
)

# Student Metrics

performance = student_performance(
    selected_student,
    submissions,
    questions
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Score",
    performance["score"]
)

col2.metric(
    "Total Questions",
    performance["total"]
)

col3.metric(
    "Percentage",
    f"{performance['percentage']}%"
)

st.divider()

st.subheader(
    "Topic Wise Performance"
)

st.dataframe(
    performance["topic_performance"]
)

fig1 = topic_chart(
    performance["topic_performance"]
)

st.pyplot(fig1)

st.divider()

st.subheader(
    "Question Difficulty Analysis"
)

difficulty = calculate_difficulty_index(
    submissions
)

st.dataframe(difficulty)

fig2 = difficulty_chart(
    difficulty
)

st.pyplot(fig2)

st.divider()

st.subheader(
    "Topic Analysis"
)

topic_stats = topic_analysis(
    submissions,
    questions
)

st.dataframe(topic_stats)

# PDF

if st.button("Generate PDF Report"):

    temp_pdf = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    generate_pdf(
        selected_student,
        performance,
        temp_pdf.name
    )

    with open(
        temp_pdf.name,
        "rb"
    ) as pdf_file:

        st.download_button(
            label="Download Report",
            data=pdf_file,
            file_name=f"{selected_student}_report.pdf",
            mime="application/pdf"
        )
