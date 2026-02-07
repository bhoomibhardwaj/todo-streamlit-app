import streamlit as st
import sqlite3

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="To-Do App",
    page_icon="💜",
    layout="centered"
)

# ---------------- CSS (FONT ENHANCEMENT ONLY) ----------------
st.markdown("""
<style>

/* Stylish Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&family=Playfair+Display:wght@600&display=swap');

/* Full screen background */
html, body, [class*="stApp"] {
    background-color: #f3e8ff;
    font-family: 'Poppins', sans-serif;
}

.main {
    background-color: #f3e8ff;
}

/* Main title – classy & bold */
h1 {
    font-family: 'Playfair Display', serif;
    color: #6d28d9;
    text-align: center;
    font-weight: 600;
    letter-spacing: 0.5px;
    animation: fadeDown 0.8s ease;
}

/* Caption */
p {
    text-align: center;
    color: #6b7280;
    font-weight: 500;
    letter-spacing: 0.3px;
    animation: fadeDown 1s ease;
}

/* Task card */
.task {
    background: #ffffff;
    padding: 14px 18px;
    border-radius: 16px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 8px 20px rgba(109,40,217,0.15);
    animation: fadeUp 0.5s ease;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    font-weight: 500;
    letter-spacing: 0.2px;
}

/* Hover animation */
.task:hover {
    transform: translateY(-4px);
    box-shadow: 0 14px 28px rgba(109,40,217,0.25);
}

/* Done task */
.done {
    color: #9ca3af;
    text-decoration: line-through;
    font-weight: 500;
}

/* Priority badges */
.badge-high { color: #dc2626; font-weight: 600; }
.badge-medium { color: #ca8a04; font-weight: 600; }
.badge-low { color: #16a34a; font-weight: 600; }

/* Buttons */
button {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}
button:hover {
    transform: scale(1.05);
}

/* Animations */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeDown {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}

</style>
""", unsafe_allow_html=True)

# ---------------- DATABASE ----------------
conn = sqlite3.connect("tasks.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT,
    done INTEGER,
    priority TEXT
)
""")
conn.commit()

# ---------------- TITLE ----------------
st.title("My To-Do App")
st.caption("Organize your day with clarity")

# ---------------- ADD TASK ----------------
with st.container():
    task = st.text_input("Enter your task")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])

    if st.button("➕ Add Task"):
        if task.strip():
            c.execute(
                "INSERT INTO tasks (task, done, priority) VALUES (?, ?, ?)",
                (task, 0, priority)
            )
            conn.commit()
            st.success("Task added!")
            st.rerun()

# ---------------- FILTER ----------------
filter_option = st.radio(
    "Show",
    ["All", "Pending", "Done"],
    horizontal=True
)

# ---------------- FETCH TASKS ----------------
query = "SELECT * FROM tasks"
if filter_option == "Pending":
    query += " WHERE done = 0"
elif filter_option == "Done":
    query += " WHERE done = 1"

tasks = c.execute(query).fetchall()

# ---------------- DISPLAY TASKS ----------------
st.markdown("### 📋 Your Tasks")

for task_id, task_text, done, priority in tasks:

    badge = (
        "badge-high" if priority == "High"
        else "badge-medium" if priority == "Medium"
        else "badge-low"
    )

    col1, col2, col3 = st.columns([1, 6, 1])

    with col1:
        check = st.checkbox("", value=bool(done), key=f"c{task_id}")
        if check != bool(done):
            c.execute(
                "UPDATE tasks SET done = ? WHERE id = ?",
                (int(check), task_id)
            )
            conn.commit()
            st.rerun()

    with col2:
        st.markdown(
            f"""
            <div class="task {'done' if done else ''}">
                {task_text}
                <span class="{badge}">({priority})</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        if st.button("❌", key=f"d{task_id}"):
            c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            st.rerun()















