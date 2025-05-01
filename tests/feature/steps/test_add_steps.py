import pytest
from pytest_bdd import scenarios, given, when, then
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../src")))
from tasks import sort_tasks_by_date, flag_tasks, filter_tasks_by_category, generate_unique_id, filter_tasks_by_priority, edit_task

scenarios("../add_task.feature")

@pytest.fixture
@given("a nonempty list of tasks")
def task_list():
    return [
        {"id": 1, "title": "Task 1", "priority": "High", "category": "Work", "due_date": "2025-04-30", "completed": False, "flagged": False},
        {"id": 2, "title": "Task 2", "priority": "Low", "category": "Personal", "due_date": "2025-04-28", "completed": True, "flagged": False},
        {"id": 3, "title": "Task 3", "priority": "Medium", "category": "School", "due_date": "2025-05-02", "completed": False, "flagged": False},
        {"id": 4, "title": "Task 4", "priority": "High", "category": "Other", "due_date": "2025-04-26", "completed": True, "flagged": False},
        {"id": 5, "title": "Task 5", "priority": "High", "category": "Other", "due_date": "2025-05-01", "completed": True, "flagged": False},
        {"id": 6, "title": "Task 6", "priority": "Medium", "category": "Work", "due_date": "2025-05-02", "completed": True, "flagged": False},
    ]

@pytest.fixture
@when("I sort the tasks by date")
def sort_tasks(task_list):
    return sort_tasks_by_date(task_list)


@then("the tasks should be ordered with the task with the closest due date first to the task with the furthest due date")
def verify_sorted_order(sort_tasks):
    expected_order = ["Task 4", "Task 2", "Task 1", "Task 5", "Task 3", "Task 6"]
    assert [task["title"] for task in sort_tasks] == expected_order

@pytest.fixture
@when('I filter tasks by category Work')
def filter_work_tasks(task_list):
    return filter_tasks_by_category(task_list, "Work")

@then("only tasks belonging to Work should be displayed")
def verify_filtered_tasks(filter_work_tasks):
    """Checks that only 'Work' tasks are displayed."""
    expected_titles = ["Task 1", "Task 6"]
    assert [task["title"] for task in filter_work_tasks] == expected_titles

@pytest.fixture
@when("I flag a task with ID 1")
def flag_existing_task(task_list):
    previous_flag = task_list[0]["flagged"]
    return flag_tasks(task_list, task_id=1), previous_flag

@then("the task with ID 1 should have a toggled flagged value")
def verify_flagged(flag_existing_task):
    task, previous = flag_existing_task
    assert task["flagged"] != previous

@pytest.fixture
@when('I update the task with ID 2 to have a new title Updated Task and category Personal')
def update_task(task_list):
    updates = {
        "title": "Updated Task",
        "category": "Personal",
        "priority": "Low",
        "due_date": "2025-04-28"
    }
    return edit_task(task_list, task_id=2, updates=updates)

@then('the task with ID 2 should have title Updated Task and category Personal')
def verify_task_edit(update_task):
    assert update_task["title"] == "Updated Task"
    assert update_task["category"] == "Personal"

@pytest.fixture
@when("I generate a new unique task ID")
def generate_id(task_list):
    return generate_unique_id(task_list)


@then("the ID should be one greater than the highest existing ID")
def verify_new_id(generate_id, task_list):
    expected_id = max(task["id"] for task in task_list) + 1
    assert generate_id == expected_id
