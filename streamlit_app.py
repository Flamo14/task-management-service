import streamlit as st
import requests
import time
from datetime import date
import os

API_BASE = os.environ.get("API_BASE") or st.secrets.get("API_BASE") or "http://localhost:8000"


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


### UI helpers and styling (presentation-only) ###


def _priority_color(priority: str) -> str:
    mapping = {
        "high": "#e53935",  # red
        "normal": "#FBBC05",  # orange/yellow
        "low": "#2e7d32",  # green
    }
    return mapping.get((priority or "").lower(), "#9e9e9e")


def _inject_css():
        css = """
        <style>
        /* Page layout */
        .tm-header {
            padding: 8px 6px;
            border-bottom: 1px solid #eee;
            margin-bottom: 10px;
        }
        .tm-user {
            color: #555;
            font-size: 13px;
        }
        /* Task row card */
        .tm-task {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 12px;
            border-radius: 8px;
            background: #ffffff;
            border: 1px solid rgba(50,50,93,0.06);
            margin-bottom: 8px;
            transition: box-shadow 0.08s ease, transform 0.06s ease;
        }
        .tm-task:hover {
            box-shadow: 0 6px 18px rgba(15,15,15,0.04);
            transform: translateY(-1px);
        }
        .tm-task .tm-border {
            width: 6px;
            height: 36px;
            border-radius: 4px;
            flex: 0 0 6px;
        }
        .tm-task-main {
            flex: 1 1 auto;
            min-width: 0;
            display:flex;
            flex-direction:column;
            gap:4px;
        }
        .tm-title {
            font-weight: 600;
            font-size: 15px;
            color: #111;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .tm-meta {
            display:flex;
            gap:10px;
            align-items:center;
            font-size:13px;
            color:#666;
        }
        .tm-badge {
            padding: 4px 8px;
            border-radius: 999px;
            font-size: 12px;
            color: #fff;
            display: inline-block;
        }
        .tm-status-pending { background: #6c757d; }
        .tm-status-in_progress { background: #1976d2; }
        .tm-status-done { background: #2e7d32; }
        /* Actions */
        .tm-actions { display:flex; gap:8px; align-items:center; }
        .stButton>button, .stDownloadButton>button {
            white-space: nowrap;
        }
        .tm-action-compact { padding:6px 10px; font-size:13px; }

        /* Create panel */
        .tm-panel { padding:12px; border-radius:8px; background:#fff; border:1px solid rgba(50,50,93,0.06); }

        /* Form tweaks */
        .tm-form .stTextInput>div>div>input, .tm-form .stTextArea>div>div>textarea {
            padding: 8px;
        }
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)


def _render_badge(label: str, bg: str) -> str:
    return f"<span class='tm-badge' style='background:{bg}'>{label}</span>"



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
    _inject_css()

    # Header / user info
    header = st.container()
    with header:
        c1, c2 = st.columns([8, 2])
        with c1:
            st.markdown("<div class='tm-header'><h2 style='margin:0'>Task Management</h2><div class='tm-user'>Professional dashboard</div></div>", unsafe_allow_html=True)
        with c2:
            if st.button("Logout"):
                st.session_state.authenticated = False
                st.session_state.user_id = None
                st.session_state.email = None
                safe_rerun()

    st.markdown(f"**Logged in as:** {st.session_state.email}")

    st.subheader("Your Tasks")
    tasks, error = get_tasks(st.session_state.user_id)
    if error:
        st.error(error)
        tasks = []

    # Two-column dashboard layout: left for tasks, right for create form
    left_col, right_col = st.columns([7, 3])

    # LEFT: Task list and management
    with left_col:
        if not tasks:
            st.info("No tasks found for your account.")
        else:
            for task in tasks:
                prio_color = _priority_color(task.get("priority"))
                status = task.get("status") or "pending"

                # Row layout: prio bar | card (title + badges) | actions x4
                row_cols = st.columns([0.25, 6, 1.2, 1.2, 1.2, 1.2])
                # Priority bar
                with row_cols[0]:
                    st.markdown(f"<div style='width:6px;height:48px;background:{prio_color};border-radius:4px;margin-top:6px'></div>", unsafe_allow_html=True)

                # Title and meta card
                status_colors = {"pending": "#6c757d", "in_progress": "#1976d2", "done": "#2e7d32"}
                status_color = status_colors.get(status, "#6c757d")
                prio_label = (task.get("priority") or "").title()
                with row_cols[1]:
                    card_html = (
                        f"<div class='tm-card' style='padding:8px;border:1px solid #edf0f4;border-radius:8px;'>"
                        f"<div class='tm-title' title='{task.get('title')}'>{task.get('title')}</div>"
                        f"<div class='tm-meta' style='margin-top:6px;'>"
                        f"{_render_badge(status.replace('_',' ').title(), status_color)}"
                        f"&nbsp;"
                        f"<span style='color:#777;font-size:13px;padding-left:6px'>{prio_label}</span>"
                        f"</div></div>"
                    )
                    st.markdown(card_html, unsafe_allow_html=True)

                # Actions - wider columns to avoid wrapping
                with row_cols[2]:
                    if st.button("View", key=f"details_{task['id']}"):
                        st.session_state[f"show_details_{task['id']}"] = True
                with row_cols[3]:
                    if st.button("Edit", key=f"edit_{task['id']}"):
                        st.session_state[f"editing_{task['id']}"] = True
                with row_cols[4]:
                    if task.get("status") != "done":
                        if st.button("Done", key=f"done_{task['id']}"):
                            if update_task(task['id'], {"status": "done"}, st.session_state.user_id):
                                st.success("Task marked as done")
                                time.sleep(0.5)
                                safe_rerun()
                            else:
                                st.error("Failed to update task status")
                with row_cols[5]:
                    if st.button("Delete", key=f"del_{task['id']}"):
                        if delete_task(task['id'], st.session_state.user_id):
                            st.success("Task deleted successfully!")
                            safe_rerun()
                        else:
                            st.error("Failed to delete task")

                # Inline edit form (compact)
                if st.session_state.get(f"editing_{task['id']}"):
                    with st.form(f"edit_form_{task['id']}", clear_on_submit=True):
                        ecol1, ecol2 = st.columns([3,1])
                        with ecol1:
                            new_title = st.text_input("Title", value=task["title"], key=f"title_{task['id']}")
                            new_description = st.text_area("Description", value=task.get("description") or "", key=f"desc_{task['id']}")
                        with ecol2:
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

                # Details view (collapsible)
                if st.session_state.get(f"show_details_{task['id']}"):
                    with st.expander("Details", expanded=True):
                        st.markdown(f"**Title:** {task.get('title')}")
                        st.markdown(f"**Description:** {task.get('description') or '—'}")
                        st.markdown(f"**Status:** {task.get('status')}")
                        st.markdown(f"**Priority:** {task.get('priority')}")
                        if task.get('start_date'):
                            st.markdown(f"**Start Date:** {task.get('start_date')}")
                        if task.get('end_date'):
                            st.markdown(f"**End Date:** {task.get('end_date')}")
                        extra_keys = [k for k in task.keys() if k not in {'id','title','description','status','priority','start_date','end_date'}]
                        for k in extra_keys:
                            st.markdown(f"**{k}:** {task.get(k)}")
                        if st.button("Close Details", key=f"close_details_{task['id']}"):
                            st.session_state.pop(f"show_details_{task['id']}", None)

                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # RIGHT: Create task panel (always visible)
    with right_col:
        st.markdown("<div style='padding:12px;border:1px solid #edf0f4;border-radius:8px;background:#fff'>", unsafe_allow_html=True)
        st.subheader("Create Task")
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
        st.markdown("</div>", unsafe_allow_html=True)


def main():
    ensure_session_state()
    # Show which backend URL the app is using (helps debug deployment vs local)
    st.sidebar.markdown(f"**API_BASE:** {API_BASE}")

    if not st.session_state.authenticated:
        auth_screen()
    else:
        main_app()


if __name__ == "__main__":
    main()