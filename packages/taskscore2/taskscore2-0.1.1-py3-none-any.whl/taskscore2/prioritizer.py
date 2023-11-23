def calculate_task_score(importance: float, effort: float) -> float:
    """
    Calculate the score of a task based on its importance and effort.

    Parameters:
    importance (float): The importance of the task, should be between 1 and 4.
    effort (float): The effort required to complete the task, should be between 1 and 4.

    Returns:
    float: The calculated score of the task.

    Raises:
    ValueError: If importance or effort is not within the required range.
    """

    if not (1 <= importance <= 4) or not (1 <= effort <= 4):
        raise ValueError("Importance and effort must be between 1 and 4.")

    score = 25 * (importance * (1 / effort))
    return score
