import streamlit as st
import sqlite3

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="To-Do App",
    page_icon="✅",
    layout="centered"
)

# ---------------- BOOTSTRAP ----------------
st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
""", unsafe_allow_html=True)

# ---------------- CSS (BEAUTIFUL UI + GLASSMORPHISM) ----------------
st.markdown("""
<style>
/* Full page background */
body {
    background-color: #d8b4fe;  /* light purple */
}

/* Glassmorphism card */
.app-card {
    background: rgba(255, 255, 255, 0.1);  /* semi-transparent */
    backdrop-filter: blur(10px);           /* blur background */
    -webkit-backdrop-filter: blur(10px);   /* Safari support */
    border-radius: 20px;
    padding: 30px;
    margin: 20px auto;
    max-width: 700px;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
}

/* Responsive for mobile */
@media (max-width: 768px) {
    .app-card {
        margin: 10px;
        padding: 20px;
    }
}

/* Task styling inside card */
.task {
    background: rgba(255, 255, 255, 0.15);
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: 0.3s;
}
.task:hover {
    background: rgba(255, 255, 255, 0.25);
    transform: translateY(-2px);
}

/* Stylish fonts */
h1, h2, h3 {
    font-family: "Playfair Display", serif;
    font-weight: 700;
}

.done {
    color: gray;
    text-decoration: line-through;
}
.badge-high { color: #ef4444; font-weight: bold; }
.badge-medium { color: #facc15; font-weight: bold; }
.badge-low { color: #22c55e; font-weight: bold; }
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

# ---------------- WRAP CONTENT IN GLASSMORPHIC CARD ----------------
st.markdown('<div class="app-card">', unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown(
    "<h1 style='color:#d946ef; font-family: \"Playfair Display\", serif; text-align:center;'>My To-Do App</h1>",
    unsafe_allow_html=True
)
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

# ---------------- END OF CARD ----------------
st.markdown('</div>', unsafe_allow_html=True)















