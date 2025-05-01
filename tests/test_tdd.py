import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from tasks import edit_task, flag_tasks, sort_tasks_by_date
from test_basic import sample_tasks


@pytest.fixture
def sample_tasks():
    return [
        {"id": 1, "title": "Task 1", "priority": "High", "category": "Work", "due_date": "2025-04-30", "completed": False, "flagged": False},
        {"id": 2, "title": "Task 2", "priority": "Low", "category": "Personal", "due_date": "2025-04-28", "completed": True, "flagged": False},
        {"id": 3, "title": "Task 3", "priority": "Medium", "category": "School", "due_date": "2025-05-02", "completed": False, "flagged": False},
        {"id": 4, "title": "Task 4", "priority": "High", "category": "Other", "due_date": "2025-04-26", "completed": True, "flagged": False},
        {"id": 5, "title": "Task 5", "priority": "High", "category": "Other", "due_date": "2025-05-01", "completed": True, "flagged": False},
        {"id": 6, "title": "Task 6", "priority": "Medium", "category": "Work", "due_date": "2025-05-02", "completed": True, "flagged": False},
    ]

def test_sort(sample_tasks):
    sorted_tasks = sort_tasks_by_date(sample_tasks)

    expected_order = ["Task 4", "Task 2", "Task 1", "Task 5", "Task 3", "Task 6"]
    assert [task["title"] for task in sorted_tasks] == expected_order

def test_edit(sample_tasks):
    updated_task = {"title": "Updated Task", "description": "Updated description", "priority": "Low", "category": "Other", "due_date": "2025-01-27"}
    edit_task(sample_tasks, task_id=1, updates=updated_task)

    assert sample_tasks[0]["title"] == "Updated Task"
    assert sample_tasks[0]["description"] == "Updated description"
    assert sample_tasks[0]["priority"] == "Low"
    assert sample_tasks[0]["category"] == "Other"
    assert sample_tasks[0]["due_date"] == "2025-01-27"

def test_flag(sample_tasks):
    before_flag = sample_tasks[0]["flagged"]
    flag_tasks(sample_tasks, task_id=1)
    assert sample_tasks[0]["flagged"] != before_flag
