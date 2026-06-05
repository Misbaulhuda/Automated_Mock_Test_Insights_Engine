import sqlite3
import pandas as pd


DB_PATH = "database/assessment.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def load_student_submissions():
    conn = get_connection()

    query = """
    SELECT *
    FROM student_submissions
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def load_question_bank():
    conn = get_connection()

    query = """
    SELECT *
    FROM question_bank
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def get_students():
    conn = get_connection()

    query = """
    SELECT DISTINCT student_id
    FROM student_submissions
    """

    students = pd.read_sql(query, conn)

    conn.close()

    return students["student_id"].tolist()
