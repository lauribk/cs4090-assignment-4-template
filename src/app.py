import streamlit as st
import pandas as pd
import subprocess
import os
from datetime import datetime
from tasks import load_tasks, save_tasks, filter_tasks_by_priority, filter_tasks_by_category, generate_unique_id, sort_tasks_by_date, edit_task

def run_tests():
    result = subprocess.run(["pytest", "tests/test_basic.py"], capture_output=True, text=True)
    st.text_area("Test Results:", result.stdout, height=300)

def run_parameterized():
    result = subprocess.run(["pytest", "-k", "test_parameterized", "tests/test_advanced.py"], capture_output=True, text=True)
    st.text_area("Parameterized Test Results:", result.stdout, height=300)

def run_coverage():
    result = subprocess.run(["pytest", "--cov=tasks", "--cov-report=term-missing", "tests/"], capture_output=True, text=True)
    st.text_area("Coverage Results:", result.stdout, height=300)

def run_mocking():
    result = subprocess.run(["pytest", "-k", "test_mocking", "tests/test_advanced.py"], capture_output=True, text=True)
    st.text_area("Mocking Test Results:", result.stdout, height=300)

def run_report():
    result = subprocess.run(["pytest", "--cov=tasks", "--cov-report=html", "tests/"], capture_output=True, text=True)
    st.text_area("HTML Report Generation:", result.stdout, height=300)
    st.write("Report saved in `htmlcov/index.html`. Expand it below.")

    report_path = "htmlcov/index.html"
    if os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        with st.expander("View HTML Coverage Report", expanded=False):
            st.components.v1.html(html_content, height=600, scrolling=True)
    else:
        st.error("HTML coverage report not found. Try running the tests again.")

def run_bdd():
    result = subprocess.run(["pytest", "tests/feature/"], capture_output=True, text=True)
    st.text_area("BDD Test Results:", result.stdout, height=300)

def main():
    st.title("To-Do Application")

    # Initialize state for editing feasture
    if "editing_task_id" not in st.session_state:
        st.session_state["editing_task_id"] = None
    
    # Load existing tasks
    tasks = load_tasks()
    
    # Sidebar for adding new tasks
    st.sidebar.header("Add New Task")
    
    # Task creation form
    with st.sidebar.form("new_task_form"):
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description")
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_category = st.selectbox("Category", ["Work", "Personal", "School", "Other"])
        task_due_date = st.date_input("Due Date")

        submit_button = st.form_submit_button("Edit Task" if st.session_state["editing_task_id"] else "Add Task")

        if submit_button:
            if not task_title:
                st.sidebar.error("Please provide a task title!")
            else:
                if st.session_state["editing_task_id"]:
                    updated_task = {
                        "title": task_title,
                        "description": task_description,
                        "priority": task_priority,
                        "category": task_category,
                        "due_date": task_due_date.strftime("%Y-%m-%d"),
                    }
                    edit_task(tasks, st.session_state["editing_task_id"], updated_task)
                    st.sidebar.success("Task updated!")

                else:
                    new_task = {
                        "id": generate_unique_id(tasks),
                        "title": task_title,
                        "description": task_description,
                        "priority": task_priority,
                        "category": task_category,
                        "due_date": task_due_date.strftime("%Y-%m-%d"),
                        "completed": False,
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "flagged": False,
                    }
                    tasks.append(new_task)
                    st.sidebar.success("Task added successfully!")
                save_tasks(tasks)
                st.session_state["editing_task_id"] = None
                st.rerun()


    # Main area to display tasks
    st.header("Your Tasks")
    

    # Task button
    if st.button("Run Tests"):
        run_tests()

    # Parameterized Tests Button
    if st.button("Run Parameterized Tests"):
        run_parameterized()

    # Mocking Test Button
    if st.button("Run Mocking Tests"):
        run_mocking()

    # BDD Test Button
    if st.button("Run BDD Tests"):
        run_bdd()

    # Coverage Test button
    if st.button("Run Coverage Tests"):
        run_coverage()

    # HTML Report Button
    if st.button("Get Report"):
        run_report()



    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_category = st.selectbox("Filter by Category", ["All"] + list(set([task["category"] for task in tasks])))
    with col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    
    col1, col2 = st.columns(2)
    with col1:
        show_completed = st.checkbox("Show Completed Tasks")
    with col2:
        sort_by_date = st.checkbox("Order by Due Date")

    # Apply filters
    filtered_tasks = tasks.copy()
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    if not show_completed:
        filtered_tasks = [task for task in filtered_tasks if not task["completed"]]
    if sort_by_date:
        filtered_tasks = sort_tasks_by_date(filtered_tasks)

    # Display tasks
    for task in filtered_tasks:
        col1, col2 = st.columns([4, 1])
        with col1:
            task["flagged"] = st.checkbox(f"Flag", value=task.get("flagged", False), key=f"flag_{task['id']}")
            task_display = f"🚩 {task['title']}" if task["flagged"] else f"📌 {task['title']}"
            if task["flagged"]:
                title = f"🚩 {task['title']}"
            else:
                title = f"{task['title']}"
            if task["completed"]:
                st.markdown(f"~~**{title}**~~")
            else:
                st.markdown(f"**{title}**")
            st.write(task["description"])
            st.caption(f"Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}")

        with col2:
            if st.button("Complete" if not task["completed"] else "Undo", key=f"complete_{task['id']}"):
                for t in tasks:
                    if t["id"] == task["id"]:
                        t["completed"] = not t["completed"]
                        save_tasks(tasks)
                        st.rerun()
            if st.button("Delete", key=f"delete_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                st.session_state["editing_task_id"] = None
                save_tasks(tasks)
                st.rerun()
            if st.button("Edit", key=f"edit_{task['id']}"):
                st.session_state["editing_task_id"] = task["id"]
                st.rerun()

if __name__ == "__main__":
    main()
