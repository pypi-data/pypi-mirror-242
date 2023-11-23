# Task Prioritizer

Task Prioritizer is a Python package designed to help you decide which task to tackle first based on a simple scoring formula. This tool is particularly useful when you're balancing tasks with varying levels of importance and effort.

## Installation

You can install Task Prioritizer directly from PyPi:

```bash
pip install task_prioritizer
```

## Usage

To use Task Prioritizer, you need to provide two key pieces of information for each task: its importance and the effort required to complete it. Both parameters should be between 1 and 4.

Here's a quick example:

```python
from task_prioritizer.prioritizer import calculate_task_score


# Example tasks
tasks = {
    "Cleaning the house": (3, 4),  # (importance, effort)
    "Studying programming": (4, 2),
    "Paying the bills": (4, 1)
}

# Calculating and printing task scores
for task, (importance, effort) in tasks.items():
    score = calculate_task_score(importance, effort)
    print(f"Task: {task}, Score: {score}")
```

## Function Documentation

calculate_task_score(importance: float, effort: float) -> float

importance (float): The importance of the task, should be between 1 and 4.
effort (float): The effort required to complete the task, should be between 1 and 4.
Returns (float): The calculated score of the task.
Raises ValueError: If importance or effort is not within the required range.


## Contributing

Contributions to Task Prioritizer are welcome! Please feel free to submit pull requests or open issues on the GitHub repository.

## License

This project is licensed under the MIT License.