import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from tasks import filter_tasks_by_priority, load_tasks
from unittest.mock import MagicMock

@pytest.fixture
def sample_tasks():
    """ Returns a sample list of tasks for testing. """
    return [
        {"id": 1, "title": "Task 1", "priority": "High", "category": "Work", "due_date": "2025-04-27", "completed": False},
        {"id": 2, "title": "Task 2", "priority": "Low", "category": "Personal", "due_date": "2025-04-28", "completed": True},
        {"id": 3, "title": "Task 3", "priority": "Medium", "category": "School", "due_date": "2025-04-29", "completed": False},
        {"id": 4, "title": "Task 4", "priority": "High", "category": "Other", "due_date": "2025-04-30", "completed": True},
        {"id": 5, "title": "Task 5", "priority": "High", "category": "Other", "due_date": "2025-05-01", "completed": True},
        {"id": 6, "title": "Task 6", "priority": "Medium", "category": "Work", "due_date": "2025-05-02", "completed": True},
    ]

@pytest.mark.parametrize("priority, expected_count", [
    ("High", 3),
    ("Medium", 2),
    ("Low", 1),
])

def test_parameterized(sample_tasks, priority, expected_count):
    filtered = filter_tasks_by_priority(sample_tasks, priority)
    assert len(filtered) == expected_count

def test_mocking():
    mock_load = MagicMock(return_value=[{"title": "Mock Task", "priority": "High"}])
    tasks = mock_load()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Mock Task"
