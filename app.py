import streamlit as st
import sqlite3

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="To-Do App",
    page_icon="✅",
    layout="centered"
)

# ---------------- THEME TOGGLE ----------------
if "theme" not in st.session_state:
    st.session_state.theme = "light"

theme_choice = st.radio(
    "Theme",
    ["Light", "Dark"],
    index=0 if st.session_state.theme == "light" else 1,
    horizontal=True
)
st.session_state.theme = "light" if theme_choice=="Light" else "dark"

# ---------------- THEME COLORS ----------------
if st.session_state.theme == "light":
    bg_color = "#fdf4ff"
    glass = "rgba(255,255,255,0.35)"
    neon = "#a855f7"
    task_bg = "rgba(255,255,255,0.55)"
    task_text = "#1f2937"
    badge_colors = {"High":"#ef4444", "Medium":"#f59e0b", "Low":"#22c55e"}
else:
    bg_color = "#0f172a"
    glass = "rgba(30,41,59,0.45)"
    neon = "#f472b6"
    task_bg = "rgba(30,41,59,0.55)"
    task_text = "#f8fafc"
    badge_colors = {"High":"#f87171", "Medium":"#fbbf24", "Low":"#34d399"}

# ---------------- CSS ----------------
st.markdown(f"""
<style>
header, footer {{visibility:hidden;}}
body {{
    background:{bg_color};
    animation:fadein 0.6s ease;
}}
@keyframes fadein {{
from {{opacity:0; transform:translateY(10px);}}
to {{opacity:1; transform:translateY(0);}}
}}

h1 {{
    text-align:center;
    color:{neon};
    text-shadow:0 0 10px {neon};
    font-family: "Playfair Display", serif;
}}

/* CLEAN LABELS */
label {{
    background:none !important;
    border:none !important;
    font-weight:600;
    color:{task_text};
}}

/* CLEAN SELECTBOX */
.stSelectbox > div > div {{
    background:{glass};
    border-radius:14px;
    border:2px solid {neon};
    backdrop-filter:blur(12px);
    box-shadow:0 0 12px {neon};
    color:{task_text};
}}

/* TEXT INPUT */
.stTextInput input {{
    background:{glass};
    border-radius:14px;
    border:2px solid {neon};
    backdrop-filter:blur(12px);
    box-shadow:0 0 12px {neon};
    color:{task_text};
}}

/* BUTTON */
.stButton button {{
    background:{glass};
    border:2px solid {neon};
    border-radius:14px;
    backdrop-filter:blur(10px);
    box-shadow:0 0 12px {neon};
    transition:0.3s;
    color:{task_text};
}}
.stButton button:hover {{
    transform:translateY(-2px) scale(1.03);
    box-shadow:0 0 20px {neon};
}}

/* TASK CARD */
.task {{
    background:{task_bg};
    color:{task_text};
    padding:14px;
    border-radius:14px;
    margin-bottom:10px;
    backdrop-filter:blur(10px);
    box-shadow:0 0 10px {neon};
    transition:0.3s;
}}
.task:hover {{
    transform:translateY(-3px);
    box-shadow:0 0 18px {neon};
}}

/* DONE TASK */
.done {{
    text-decoration:line-through;
    opacity:0.6;
}}

/* TASK BADGES - NEON & ANIMATED */
.badge-high, .badge-medium, .badge-low {{
    color:white;
    font-weight:bold;
    background: none;
    border:2px solid;
    border-radius:8px;
    padding:2px 6px;
    font-family:"Playfair Display", serif;
    animation: glow 1.5s infinite alternate;
}}

.badge-high {{ border-color:{badge_colors["High"]}; color:{badge_colors["High"]}; }}
.badge-medium {{ border-color:{badge_colors["Medium"]}; color:{badge_colors["Medium"]}; }}
.badge-low {{ border-color:{badge_colors["Low"]}; color:{badge_colors["Low"]}; }}

@keyframes glow {{
    from {{ box-shadow:0 0 5px currentColor; }}
    to {{ box-shadow:0 0 15px currentColor; }}
}}
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
st.markdown("<h1>To-Do App</h1>", unsafe_allow_html=True)
st.markdown("""
<div style="
    text-align:center;
    font-weight:bold;
    font-size:18px;
    animation: fadeInCaption 1s ease-in-out;
    color: #ff6ec7;  /* tu chahe to neon color ya theme color bhi use kar sakta hai */
">
MANAGE YOUR TASKS EFFICIENTLY
</div>

<style>
@keyframes fadeInCaption {
    0% { opacity: 0; transform: translateY(10px); }
    100% { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)






# ---------------- ADD TASK ----------------
task = st.text_input("Enter your task")
priority = st.selectbox("Priority", ["High","Medium","Low"])

if st.button("➕ Add Task"):
    if task.strip():
        c.execute("INSERT INTO tasks (task, done, priority) VALUES (?, ?, ?)", (task,0,priority))
        conn.commit()
        st.success("Task added!")
        st.rerun()

# ---------------- FILTER ----------------
filter_option = st.radio("Show", ["All","Pending","Done"], horizontal=True)
query = "SELECT * FROM tasks"
if filter_option=="Pending": query+=" WHERE done=0"
elif filter_option=="Done": query+=" WHERE done=1"

tasks = c.execute(query).fetchall()

# ---------------- DISPLAY TASKS ----------------
st.markdown("### 📋 Your Tasks")

for task_id, task_text, done, priority in tasks:
    badge = "badge-high" if priority=="High" else "badge-medium" if priority=="Medium" else "badge-low"
    col1,col2,col3 = st.columns([1,6,1])

    with col1:
        check = st.checkbox("", value=bool(done), key=f"c{task_id}")
        if check != bool(done):
            c.execute("UPDATE tasks SET done=? WHERE id=?",(int(check),task_id))
            conn.commit()
            st.rerun()

    with col2:
        st.markdown(
            f'<div class="task {"done" if done else ""}">{task_text} <span class="{badge}">({priority})</span></div>',
            unsafe_allow_html=True
        )

    with col3:
        if st.button("❌", key=f"d{task_id}"):
            c.execute("DELETE FROM tasks WHERE id=?",(task_id,))
            conn.commit()
            st.rerun()

















