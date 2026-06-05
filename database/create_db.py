import sqlite3

conn = sqlite3.connect("database/assessment.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS student_submissions (
    student_id TEXT,
    question_id TEXT,
    selected_option TEXT,
    is_correct INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS question_bank (
    question_id TEXT,
    topic TEXT,
    correct_option TEXT
)
""")

conn.commit()
conn.close()

print("assessment.db created successfully")
