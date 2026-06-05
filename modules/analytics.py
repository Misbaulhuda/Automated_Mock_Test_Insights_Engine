import pandas as pd


def calculate_difficulty_index(submissions):

    difficulty = (
        submissions
        .groupby("question_id")
        .agg(
            Total_Submissions=("student_id", "count"),
            Correct_Responses=("is_correct", "sum")
        )
        .reset_index()
    )

    difficulty["Difficulty_Index"] = (
        difficulty["Correct_Responses"]
        / difficulty["Total_Submissions"]
    )

    return difficulty


def topic_analysis(submissions, questions):

    merged = submissions.merge(
        questions,
        on="question_id",
        how="left"
    )

    topic_stats = (
        merged
        .groupby("topic")
        .agg(
            Questions_Attempted=("question_id", "count"),
            Correct=("is_correct", "sum")
        )
        .reset_index()
    )

    topic_stats["Accuracy"] = (
        topic_stats["Correct"]
        / topic_stats["Questions_Attempted"]
    ) * 100

    return topic_stats


def student_performance(student_id,
                        submissions,
                        questions):

    student = submissions[
        submissions["student_id"] == student_id
    ]

    merged = student.merge(
        questions,
        on="question_id",
        how="left"
    )

    score = merged["is_correct"].sum()

    total = len(merged)

    percentage = round(
        (score / total) * 100,
        2
    )

    topic_performance = (
        merged
        .groupby("topic")
        .agg(
            Correct=("is_correct", "sum"),
            Total=("question_id", "count")
        )
        .reset_index()
    )

    topic_performance["Accuracy"] = (
        topic_performance["Correct"]
        / topic_performance["Total"]
    ) * 100

    return {
        "score": score,
        "total": total,
        "percentage": percentage,
        "topic_performance": topic_performance
    }
