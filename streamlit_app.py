import streamlit as st
import requests
from datetime import date

API_BASE = "http://localhost:8000"

def get_tasks(user_id):
    try:
        response = requests.get(f"{API_BASE}/tasks", params={"user_id": user_id})
        response.raise_for_status()
        return response.json(), None
    except requests.RequestException as e:
        return [], f"Failed to fetch tasks: {e}"


def get_all_tasks():
    try:
        response = requests.get(f"{API_BASE}/tasks")
        response.raise_for_status()
        return response.json(), None
    except requests.RequestException as e:
        return [], f"Failed to fetch tasks: {e}"

def create_task(data):
    try:
        response = requests.post(f"{API_BASE}/tasks", json=data)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        st.error(f"Failed to create task: {e}")
        return False

def update_task(task_id, data, user_id):
    try:
        response = requests.put(f"{API_BASE}/tasks/{task_id}", params={"user_id": user_id}, json=data)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        st.error(f"Failed to update task: {e}")
        return False

def delete_task(task_id):
    try:
        response = requests.delete(f"{API_BASE}/tasks/{task_id}")
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        st.error(f"Failed to delete task: {e}")
        return False

def main():
    st.title("Task Management Service")

    user_id = st.text_input("User ID", value="user1")

    st.header("Task List")

    # Get All Tasks button (works independently of user_id)
    if st.button("Get All Tasks"):
        tasks, error = get_all_tasks()
        if error:
            st.error(error)
            tasks = []
        else:
            st.success(f"Successfully loaded {len(tasks)} tasks")
    else:
        # Default behavior: show tasks filtered by user_id (if provided)
        tasks, error = get_tasks(user_id) if user_id else ([], None)

    if error:
        st.error(error)
    elif not tasks:
        st.info("No tasks found for this user.")
    else:
        for task in tasks:
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"**{task['title']}**")
                st.markdown(
                    f"- Status: **{task['status']}**  \n"
                    f"- Priority: **{task['priority']}**  \n"
                    f"- User ID: **{task['user_id']}**"
                )
            with col2:
                if st.button("Delete", key=f"del_{task['id']}"):
                    if delete_task(task['id']):
                        st.success("Task deleted successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to delete task")
            st.divider()

    # Create New Task (always visible)
    st.header("Create New Task")
    with st.form("create_task"):
        title = st.text_input("Title")
        description = st.text_area("Description")
        priority = st.selectbox("Priority", ["low", "normal", "high"])
        start_date = st.date_input("Start Date", value=None)
        end_date = st.date_input("End Date", value=None)

        submitted = st.form_submit_button("Create Task")
        if submitted:
            if not title:
                st.error("Title is required")
            else:
                data = {
                    "title": title,
                    "user_id": user_id,
                    "description": description if description else None,
                    "priority": priority,
                    "start_date": start_date.isoformat() if start_date else None,
                    "end_date": end_date.isoformat() if end_date else None,
                }
                if create_task(data):
                    st.success("Task created successfully!")
                    st.rerun()
                else:
                    st.error("Failed to create task")

if __name__ == "__main__":
    main()