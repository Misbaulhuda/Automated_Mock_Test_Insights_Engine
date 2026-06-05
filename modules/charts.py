import matplotlib.pyplot as plt


def topic_chart(topic_df):

    fig, ax = plt.subplots(figsize=(8,4))

    ax.bar(
        topic_df["topic"],
        topic_df["Accuracy"]
    )

    ax.set_title(
        "Topic Wise Accuracy"
    )

    ax.set_ylabel("Accuracy %")

    return fig


def difficulty_chart(diff_df):

    fig, ax = plt.subplots(figsize=(10,4))

    ax.bar(
        diff_df["question_id"],
        diff_df["Difficulty_Index"]
    )

    ax.set_title(
        "Question Difficulty Index"
    )

    ax.set_ylabel("Difficulty")

    return fig
