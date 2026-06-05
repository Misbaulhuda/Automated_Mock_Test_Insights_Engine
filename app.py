```python
# app.py

import streamlit as st
import pandas as pd
import sqlite3
import os

from reports.report_generator import generate_student_report

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="Automated Mock Test Insights Engine",
    page_icon="📊",
    layout="wide"
)

# -----------------------------------
# Title
# -----------------------------------

st.title("📊 Automated Mock Test Insights Engine")
st.markdown("Analyze student performance and generate PDF reports.")

# -----------------------------------
# Database Connection
# -----------------------------------

DB_PATH = "assessment.db"


@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)

    submissions = pd.read_sql(
        "SELECT * FROM student_submissions",
        conn
    )

    question_bank = pd.read_sql(
        "SELECT * FROM question_bank",
        conn
    )

    conn.close()

    return submissions, question_bank


try:
    submissions_df, questions_df = load_data()

except Exception as e:
    st.error(f"Database Error: {e}")
    st.stop()

# -----------------------------------
# Display Data
# -----------------------------------

st.subheader("Student Submission Data")
st.dataframe(submissions_df, use_container_width=True)

st.subheader("Question Bank")
st.dataframe(questions_df, use_container_width=True)

# -----------------------------------
# Student Selection
# -----------------------------------

student_ids = sorted(
    submissions_df["student_id"].unique()
)

selected_student = st.selectbox(
    "Select Student",
    student_ids
)

# -----------------------------------
# Student Analysis
# -----------------------------------

student_data = submissions_df[
    submissions_df["student_id"] == selected_student
]

total_questions = len(student_data)

correct_answers = student_data["is_correct"].sum()

accuracy = (
    correct_answers / total_questions * 100
    if total_questions > 0
    else 0
)

# -----------------------------------
# Merge for Topic Analysis
# -----------------------------------

merged = student_data.merge(
    questions_df,
    on="question_id",
    how="left"
)

weak_topics = (
    merged[merged["is_correct"] == 0]
    ["topic"]
    .value_counts()
    .index
    .tolist()
)

# -----------------------------------
# Metrics
# -----------------------------------

st.subheader("Performance Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Questions",
        total_questions
    )

with col2:
    st.metric(
        "Correct Answers",
        int(correct_answers)
    )

with col3:
    st.metric(
        "Accuracy %",
        f"{accuracy:.2f}"
    )

# -----------------------------------
# Weak Topics
# -----------------------------------

st.subheader("Weak Topics")

if weak_topics:
    weak_df = pd.DataFrame(
        {"Weak Topics": weak_topics}
    )

    st.dataframe(
        weak_df,
        use_container_width=True
    )
else:
    st.success("No weak topics found.")

# -----------------------------------
# Generate PDF
# -----------------------------------

st.subheader("Generate Report")

if st.button("Generate PDF Report"):

    pdf_path = generate_student_report(
        selected_student,
        accuracy,
        weak_topics
    )

    st.success("PDF Generated Successfully!")

    with open(pdf_path, "rb") as pdf_file:
        st.download_button(
            label="Download PDF",
            data=pdf_file,
            file_name=os.path.basename(pdf_path),
            mime="application/pdf"
        )

# -----------------------------------
# Leaderboard
# -----------------------------------

st.subheader("Student Leaderboard")

leaderboard = []

for student in student_ids:

    temp = submissions_df[
        submissions_df["student_id"] == student
    ]

    total = len(temp)

    correct = temp["is_correct"].sum()

    acc = (
        correct / total * 100
        if total > 0
        else 0
    )

    leaderboard.append(
        {
            "Student ID": student,
            "Accuracy (%)": round(acc, 2)
        }
    )

leaderboard_df = pd.DataFrame(
    leaderboard
).sort_values(
    by="Accuracy (%)",
    ascending=False
)

st.dataframe(
    leaderboard_df,
    use_container_width=True
)

st.bar_chart(
    leaderboard_df.set_index(
        "Student ID"
    )["Accuracy (%)"]
)
```


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
