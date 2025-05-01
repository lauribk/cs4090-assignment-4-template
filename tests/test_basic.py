import pytest
import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from tasks import load_tasks, save_tasks, generate_unique_id, filter_tasks_by_priority, filter_tasks_by_completion, get_overdue_tasks
from datetime import datetime, timedelta

# Test file setup
TEST_TASKS_FILE = "test_tasks.json"

""" FAKE TASKS FOR TESTING"""

@pytest.fixture
def sample_tasks():
    return [
        {"id": 1, "title": "Task 1", "priority": "High", "category": "Work", "due_date": "2025-04-27", "completed": False},
        {"id": 2, "title": "Task 2", "priority": "Low", "category": "Personal", "due_date": "2025-04-28", "completed": True},
        {"id": 3, "title": "Task 3", "priority": "Medium", "category": "School", "due_date": "2025-04-29", "completed": False},
        {"id": 4, "title": "Task 4", "priority": "High", "category": "Other", "due_date": "2025-04-30", "completed": True},
        {"id": 5, "title": "Task 5", "priority": "High", "category": "Other", "due_date": "2025-05-01", "completed": True},
        {"id": 6, "title": "Task 6", "priority": "Medium", "category": "Work", "due_date": "2025-05-02", "completed": True},
    ]

""" TESTING LOADING TESTS"""

# Tests loading tasks from a test json file
def test_load(sample_tasks):
    with open(TEST_TASKS_FILE, "w") as f:
        json.dump(sample_tasks, f)

    loaded_tasks = load_tasks(TEST_TASKS_FILE)
    assert isinstance(loaded_tasks, list)
    assert len(loaded_tasks) == len(sample_tasks)

# Tests loading tasks from an empty file
def test_load_empty_file():
    # Creates and empty file
    open(TEST_TASKS_FILE, "w").close()

    loaded_tasks = load_tasks(TEST_TASKS_FILE)
    assert isinstance(loaded_tasks, list)
    assert loaded_tasks == []

# Tests loading tasks when the file is missing
def test_load_mising_file():
    if os.path.exists(TEST_TASKS_FILE):
        os.remove(TEST_TASKS_FILE)

    loaded_tasks = load_tasks(TEST_TASKS_FILE)
    assert isinstance(loaded_tasks, list)
    assert loaded_tasks == []

# removes the test files after running the tests to keep clean
@pytest.fixture(scope="module", autouse=True)
def clean():
    yield
    if os.path.exists(TEST_TASKS_FILE):
        os.remove(TEST_TASKS_FILE)

""" TESTING SAVING TASKS"""

def test_save(sample_tasks):
    save_tasks(sample_tasks, TEST_TASKS_FILE)
    with open(TEST_TASKS_FILE, "r") as f:
        saved_tasks = json.load(f)

    assert isinstance(saved_tasks, list)
    assert len(saved_tasks) == len(sample_tasks)

""" TESTING GENERATING ID"""

def test_id(sample_tasks):
    new_id = generate_unique_id(sample_tasks)
    assert new_id == max(task["id"] for task in sample_tasks) + 1

# Test for no tasks
def test_id_no_tasks():
    assert generate_unique_id([]) == 1

""" TESTING PRIORITY FILTER"""

# Tests high priority filter
def test_filter_high_priority(sample_tasks):
    high_priority_tasks = filter_tasks_by_priority(sample_tasks, "High")
    assert len(high_priority_tasks) == 3
    assert high_priority_tasks[0]["priority"] == "High"

# Tests medium priority filter
def test_filter_medium_priority(sample_tasks):
    medium_priority_tasks = filter_tasks_by_priority(sample_tasks, "Medium")
    assert len(medium_priority_tasks) == 2
    assert medium_priority_tasks[0]["priority"] == "Medium"

# Tests low priority filter
def test_filter_low_priority(sample_tasks):
    low_priority_tasks = filter_tasks_by_priority(sample_tasks, "Low")
    assert len(low_priority_tasks) == 1
    assert low_priority_tasks[0]["priority"] == "Low"

""" TESTING GETTING OVERDUE TASKS"""

def test_overdue(sample_tasks):
    today = datetime.now().strftime("%Y-%m-%d")
    overdue_tasks = get_overdue_tasks(sample_tasks)
    assert all(task["due_date"] < today and not task["completed"] for task in overdue_tasks)

""" TESTING COMPLETION FILTER"""

def test_filter_completed(sample_tasks):
    completed_tasks = filter_tasks_by_completion(sample_tasks)
    assert len(completed_tasks) == 4
