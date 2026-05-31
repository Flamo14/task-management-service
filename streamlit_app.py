import streamlit as st
import requests
import time
from datetime import date
import os

API_BASE = st.secrets.get("API_BASE") or os.environ.get("API_BASE") or "http://localhost:8000"


def api_register(email: str, password: str):
    try:
        resp = requests.post(f"{API_BASE}/users/register", json={"email": email, "password": password})
        resp.raise_for_status()
        return resp.json(), None
    except requests.RequestException as e:
        return None, str(e)


def api_login(email: str, password: str):
    try:
        resp = requests.post(f"{API_BASE}/users/login", json={"email": email, "password": password})
        resp.raise_for_status()
        return resp.json(), None
    except requests.RequestException as e:
        return None, str(e)


def get_tasks(user_id):
    try:
        response = requests.get(f"{API_BASE}/tasks", params={"user_id": user_id})
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


def delete_task(task_id, user_id):
    try:
        response = requests.delete(f"{API_BASE}/tasks/{task_id}", params={"user_id": user_id})
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        st.error(f"Failed to delete task: {e}")
        return False


def ensure_session_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "email" not in st.session_state:
        st.session_state.email = None


def safe_rerun():
    """Rerun the Streamlit script, compatible with multiple versions."""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except AttributeError:
            try:
                st.experimental_set_query_params(_rerun=int(time.time()))
            except Exception:
                pass


def auth_screen():
    st.title("Task Management — Login / Register")
    tabs = st.tabs(["Login", "Register"])

    with tabs[0]:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            user, err = api_login(email, password)
            if err:
                st.error(f"Login failed: {err}")
            elif user is None:
                st.error("Invalid credentials")
            else:
                st.session_state.authenticated = True
                st.session_state.user_id = user.get("id")
                st.session_state.email = user.get("email")
                st.success("Login successful")
                time.sleep(0.5)
                safe_rerun()

    with tabs[1]:
        st.subheader("Register")
        with st.form("register_form", clear_on_submit=True):
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            submitted = st.form_submit_button("Register")
            if submitted:
                user, err = api_register(reg_email, reg_password)
                if err:
                    st.error(f"Registration failed: {err}")
                else:
                    st.success("Registration successful. You may now log in.")


def main_app():
    st.title("Task Management Service")

    col1, col2 = st.columns([8, 2])
    with col1:
        st.markdown(f"**Logged in as:** {st.session_state.email}")
    with col2:
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.email = None
            safe_rerun()

    st.header("Your Tasks")
    tasks, error = get_tasks(st.session_state.user_id)
    if error:
        st.error(error)
        tasks = []

    if not tasks:
        st.info("No tasks found for your account.")
    else:
        for task in tasks:
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"**{task['title']}**")
                st.markdown(
                    f"- Status: **{task['status']}**  \n"
                    f"- Priority: **{task['priority']}**"
                )
            with col2:
                if st.button("Edit", key=f"edit_{task['id']}"):
                    st.session_state[f"editing_{task['id']}"] = True
                if st.button("Details", key=f"details_{task['id']}"):
                    st.session_state[f"show_details_{task['id']}"] = True
                if task.get("status") != "done":
                    if st.button("Mark done", key=f"done_{task['id']}"):
                        if update_task(task['id'], {"status": "done"}, st.session_state.user_id):
                            st.success("Task marked as done")
                            time.sleep(0.5)
                            safe_rerun()
                        else:
                            st.error("Failed to update task status")
                if st.button("Delete", key=f"del_{task['id']}"):
                    if delete_task(task['id'], st.session_state.user_id):
                        st.success("Task deleted successfully!")
                        safe_rerun()
                    else:
                        st.error("Failed to delete task")
            if st.session_state.get(f"editing_{task['id']}"):
                with st.form(f"edit_form_{task['id']}", clear_on_submit=True):
                    new_title = st.text_input("Title", value=task["title"], key=f"title_{task['id']}")
                    new_description = st.text_area("Description", value=task.get("description") or "", key=f"desc_{task['id']}")
                    new_status = st.selectbox(
                        "Status",
                        ["pending", "in_progress", "done"],
                        index=["pending", "in_progress", "done"].index(task.get("status", "pending")),
                        key=f"status_{task['id']}"
                    )
                    new_priority = st.selectbox("Priority", ["low", "normal", "high"], index=["low","normal","high"].index(task.get("priority","normal")), key=f"prio_{task['id']}")
                    submitted = st.form_submit_button("Update")
                    if submitted:
                        data = {
                            "title": new_title,
                            "description": new_description if new_description else None,
                            "status": new_status,
                            "priority": new_priority,
                        }
                        if update_task(task['id'], data, st.session_state.user_id):
                            st.success("Task updated")
                            st.session_state.pop(f"editing_{task['id']}", None)
                            time.sleep(0.5)
                            safe_rerun()
                        else:
                            st.error("Failed to update task")
            # Details view
            if st.session_state.get(f"show_details_{task['id']}"):
                with st.expander("Details", expanded=True):
                    # Show common fields first
                    st.markdown(f"**Title:** {task.get('title')}")
                    st.markdown(f"**Description:** {task.get('description') or '—'}")
                    st.markdown(f"**Status:** {task.get('status')}")
                    st.markdown(f"**Priority:** {task.get('priority')}")
                    if task.get('start_date'):
                        st.markdown(f"**Start Date:** {task.get('start_date')}")
                    if task.get('end_date'):
                        st.markdown(f"**End Date:** {task.get('end_date')}")
                    # Show any other fields present
                    extra_keys = [k for k in task.keys() if k not in {'id','title','description','status','priority','start_date','end_date'}]
                    for k in extra_keys:
                        st.markdown(f"**{k}:** {task.get(k)}")
                    if st.button("Close Details", key=f"close_details_{task['id']}"):
                        st.session_state.pop(f"show_details_{task['id']}", None)
            st.divider()

    st.header("Create New Task")
    with st.form("create_task", clear_on_submit=True):
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
                    "user_id": st.session_state.user_id,
                    "description": description if description else None,
                    "priority": priority,
                    "start_date": start_date.isoformat() if start_date else None,
                    "end_date": end_date.isoformat() if end_date else None,
                }
                if create_task(data):
                    st.success("Task created successfully!")
                    time.sleep(0.5)
                    safe_rerun()
                else:
                    st.error("Failed to create task")


def main():
    ensure_session_state()

    if not st.session_state.authenticated:
        auth_screen()
    else:
        main_app()


if __name__ == "__main__":
    main()