# Task Optimizer

Task Optimizer is a Python package designed to help prioritize tasks based on their importance and required effort. It uses a simple yet effective scoring formula to determine which tasks should be tackled first, making your decision-making process more efficient and data-driven.

## Installation

To install Task Optimizer, simply use pip:

```bash
pip install taskscore
```

## Usage

Using Task Optimizer is straightforward. Import the calculate_task_score function from the package and provide the task's importance and effort levels as integers between 1 and 4.

Example:
```python
from taskscore.optimizer import calculate_task_score

# Define your task parameters
importance = 3  # Scale: 1 (least important) to 4 (most important)
effort = 2      # Scale: 1 (least effort) to 4 (most effort)

# Calculate the task score
score = calculate_task_score(importance, effort)
print(f"Task Score: {score}")
```

## Functionality

- calculate_task_score(importance: int, effort: int) -> float:
- importance: Integer between 1 and 4, where 4 is the most important.
- effort: Integer between 1 and 4, where 4 requires the most effort.
- Returns: A float value representing the task score. Higher scores indicate tasks that should be prioritized.


## Contributing

Contributions to Task Optimizer are welcome! Please read our contribution guidelines for details on submitting pull requests.

## License

This project is licensed under the MIT License - see the file for details.
