def calculate_task_score(importance: int, effort: int) -> float:
    """
    Calculate the score of a task based on its importance and effort.

    Parameters:
    importance (int): An integer between 1 and 4 indicating the importance of the task.
    effort (int): An integer between 1 and 4 indicating the effort required for the task.

    Returns:
    float: The calculated score of the task.

    Raises:
    ValueError: If importance or effort is not within the range of 1 to 4.
    """
    if not 1 <= importance <= 4 or not 1 <= effort <= 4:
        raise ValueError("Importance and effort must be integers between 1 and 4.")

    score = 25 * (importance * (1 / effort))
    return score
