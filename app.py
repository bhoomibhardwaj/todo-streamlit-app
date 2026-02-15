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

# ---------------- THEME COLORS ----------------
def get_theme_colors(theme):
    if theme == "light":
        return {
            "bg_color": "#f0f2f6",
            "card_bg": "rgba(255, 255, 255, 0.25)",
            "glass_effect": "rgba(255, 255, 255, 0.4)",
            "neon": "#a855f7",
            "task_bg": "rgba(255, 255, 255, 0.35)",
            "task_text": "#1f2937",
            "badge_colors": {"High": "#ef4444", "Medium": "#f59e0b", "Low": "#22c55e"},
            "card_border": "rgba(255, 255, 255, 0.5)",
            "shadow": "rgba(168, 85, 247, 0.3)"
        }
    else:
        return {
            "bg_color": "#0a0c10",
            "card_bg": "rgba(30, 41, 59, 0.25)",
            "glass_effect": "rgba(30, 41, 59, 0.4)",
            "neon": "#f472b6",
            "task_bg": "rgba(30, 41, 59, 0.35)",
            "task_text": "#f8fafc",
            "badge_colors": {"High": "#f87171", "Medium": "#fbbf24", "Low": "#34d399"},
            "card_border": "rgba(255, 255, 255, 0.1)",
            "shadow": "rgba(244, 114, 182, 0.3)"
        }

# ---------------- APPLY THEME ----------------
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    theme_choice = st.radio(
        "Theme",
        ["🌞 Light", "🌙 Dark"],
        index=0 if st.session_state.theme == "light" else 1,
        horizontal=True,
        label_visibility="collapsed"
    )
st.session_state.theme = "light" if "Light" in theme_choice else "dark"
colors = get_theme_colors(st.session_state.theme)

# ---------------- CSS WITH ENHANCED GLASSMORPHISM ----------------
st.markdown(f"""
<style>
    /* Global Styles */
    .stApp {{
        background: {colors['bg_color']};
        transition: background 0.3s ease;
    }}
    
    /* Main Container Card with Glassmorphism */
    .main-card {{
        background: {colors['card_bg']};
        backdrop-filter: blur(12px) saturate(180%);
        -webkit-backdrop-filter: blur(12px) saturate(180%);
        border-radius: 30px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid {colors['card_border']};
        box-shadow: 0 15px 35px {colors['shadow']}, 0 0 0 1px {colors['card_border']} inset;
        animation: cardFloat 0.6s ease-out;
    }}
    
    @keyframes cardFloat {{
        from {{
            opacity: 0;
            transform: translateY(20px) scale(0.95);
        }}
        to {{
            opacity: 1;
            transform: translateY(0) scale(1);
        }}
    }}
    
    /* Title Styles */
    h1 {{
        text-align: center;
        color: {colors['neon']};
        text-shadow: 0 0 15px {colors['neon']};
        font-family: "Playfair Display", serif;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        animation: titleGlow 2s infinite alternate;
    }}
    
    @keyframes titleGlow {{
        from {{ text-shadow: 0 0 10px {colors['neon']}; }}
        to {{ text-shadow: 0 0 25px {colors['neon']}, 0 0 35px {colors['neon']}; }}
    }}
    
    /* Caption Style */
    .caption {{
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
        color: {colors['neon']};
        opacity: 0.9;
        letter-spacing: 2px;
        margin-bottom: 2rem;
        animation: fadeInCaption 1s ease;
    }}
    
    @keyframes fadeInCaption {{
        from {{ opacity: 0; transform: translateY(-10px); }}
        to {{ opacity: 0.9; transform: translateY(0); }}
    }}
    
    /* Input Fields with Glassmorphism */
    .stTextInput > div > div > input {{
        background: {colors['glass_effect']} !important;
        border: 2px solid {colors['neon']} !important;
        border-radius: 15px !important;
        backdrop-filter: blur(8px) !important;
        color: {colors['task_text']} !important;
        padding: 12px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        box-shadow: 0 0 20px {colors['neon']} !important;
        transform: translateY(-2px);
    }}
    
    /* Selectbox Styling */
    .stSelectbox > div > div {{
        background: {colors['glass_effect']} !important;
        border: 2px solid {colors['neon']} !important;
        border-radius: 15px !important;
        backdrop-filter: blur(8px) !important;
        color: {colors['task_text']} !important;
    }}
    
    /* Button Styling */
    .stButton > button {{
        background: {colors['glass_effect']} !important;
        border: 2px solid {colors['neon']} !important;
        border-radius: 15px !important;
        backdrop-filter: blur(8px) !important;
        color: {colors['task_text']} !important;
        font-weight: bold !important;
        padding: 10px 25px !important;
        width: 100%;
        transition: all 0.3s ease !important;
        box-shadow: 0 5px 15px {colors['shadow']} !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 25px {colors['neon']} !important;
        border-color: {colors['neon']} !important;
    }}
    
    /* Radio Buttons Styling */
    .stRadio > div {{
        background: {colors['glass_effect']} !important;
        border-radius: 50px !important;
        padding: 5px !important;
        backdrop-filter: blur(8px) !important;
        border: 1px solid {colors['card_border']} !important;
    }}
    
    .stRadio > div > label {{
        color: {colors['task_text']} !important;
        background: none !important;
        border-radius: 25px !important;
        padding: 5px 15px !important;
    }}
    
    .stRadio > div > label[data-baseweb="radio"] {{
        background: none !important;
    }}
    
    /* Task Card */
    .task-card {{
        background: {colors['task_bg']};
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid {colors['card_border']};
        border-radius: 15px;
        padding: 12px 15px;
        margin: 10px 0;
        transition: all 0.3s ease;
        animation: taskAppear 0.5s ease-out;
    }}
    
    .task-card:hover {{
        transform: translateX(5px) translateY(-2px);
        box-shadow: 0 10px 25px {colors['shadow']};
        border-color: {colors['neon']};
    }}
    
    @keyframes taskAppear {{
        from {{
            opacity: 0;
            transform: translateX(-20px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    .task-text {{
        color: {colors['task_text']};
        font-size: 1.1rem;
        margin: 0;
    }}
    
    .task-text.done {{
        text-decoration: line-through;
        opacity: 0.6;
    }}
    
    /* Priority Badges */
    .badge {{
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-left: 10px;
        border: 2px solid;
        animation: badgeGlow 1.5s infinite alternate;
    }}
    
    .badge-high {{
        border-color: {colors['badge_colors']['High']};
        color: {colors['badge_colors']['High']};
        background: rgba(239, 68, 68, 0.1);
    }}
    
    .badge-medium {{
        border-color: {colors['badge_colors']['Medium']};
        color: {colors['badge_colors']['Medium']};
        background: rgba(245, 158, 11, 0.1);
    }}
    
    .badge-low {{
        border-color: {colors['badge_colors']['Low']};
        color: {colors['badge_colors']['Low']};
        background: rgba(34, 197, 94, 0.1);
    }}
    
    @keyframes badgeGlow {{
        from {{ box-shadow: 0 0 5px currentColor; }}
        to {{ box-shadow: 0 0 15px currentColor; }}
    }}
    
    /* Delete Button */
    .delete-btn {{
        background: none !important;
        border: none !important;
        color: {colors['task_text']} !important;
        font-size: 1.2rem !important;
        padding: 0 10px !important;
        cursor: pointer;
        transition: all 0.3s ease !important;
    }}
    
    .delete-btn:hover {{
        color: #ef4444 !important;
        transform: scale(1.2);
    }}
    
    /* Checkbox Styling */
    .stCheckbox {{
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    
    /* Success Message */
    .stSuccess {{
        background: {colors['glass_effect']} !important;
        backdrop-filter: blur(8px) !important;
        border: 1px solid {colors['neon']} !important;
        border-radius: 15px !important;
        color: {colors['task_text']} !important;
    }}
    
    /* Section Titles */
    .section-title {{
        color: {colors['neon']};
        font-size: 1.5rem;
        margin: 1.5rem 0 1rem 0;
        text-shadow: 0 0 10px {colors['neon']};
        font-family: "Playfair Display", serif;
    }}
    
    /* Hide Streamlit Branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
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

# ---------------- MAIN CARD CONTAINER ----------------
st.markdown('<div class="main-card">', unsafe_allow_html=True)

# ---------------- TITLE AND CAPTION ----------------
st.markdown("<h1>✨ To-Do App ✨</h1>", unsafe_allow_html=True)
st.markdown('<div class="caption">MANAGE YOUR TASKS EFFICIENTLY</div>', unsafe_allow_html=True)

# ---------------- ADD TASK SECTION ----------------
st.markdown('<div class="section-title">📝 Add New Task</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    task = st.text_input("", placeholder="Enter your task here...", label_visibility="collapsed")
with col2:
    priority = st.selectbox("", ["High", "Medium", "Low"], label_visibility="collapsed")

if st.button("➕ Add Task", use_container_width=True):
    if task.strip():
        c.execute("INSERT INTO tasks (task, done, priority) VALUES (?, ?, ?)", (task, 0, priority))
        conn.commit()
        st.success("✨ Task added successfully!")
        st.rerun()
    else:
        st.warning("⚠️ Please enter a task!")

# ---------------- FILTER SECTION ----------------
st.markdown('<div class="section-title">🔍 Filter Tasks</div>', unsafe_allow_html=True)
filter_option = st.radio("", ["All", "Pending", "Done"], horizontal=True, label_visibility="collapsed")

# ---------------- TASKS DISPLAY SECTION ----------------
st.markdown('<div class="section-title">📋 Your Tasks</div>', unsafe_allow_html=True)

# Build query based on filter
query = "SELECT * FROM tasks"
if filter_option == "Pending":
    query += " WHERE done=0"
elif filter_option == "Done":
    query += " WHERE done=1"
query += " ORDER BY CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 WHEN 'Low' THEN 3 END"

tasks = c.execute(query).fetchall()

if not tasks:
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 3rem;
        color: {colors['task_text']};
        opacity: 0.7;
        background: {colors['glass_effect']};
        border-radius: 20px;
        backdrop-filter: blur(8px);
    ">
        🎉 No tasks here! Add some tasks to get started.
    </div>
    """, unsafe_allow_html=True)
else:
    for task_id, task_text, done, priority in tasks:
        badge_class = f"badge badge-{priority.lower()}"
        
        # Create a container for each task
        with st.container():
            col1, col2, col3 = st.columns([0.5, 5, 0.5])
            
            with col1:
                check = st.checkbox("", value=bool(done), key=f"check_{task_id}")
                if check != bool(done):
                    c.execute("UPDATE tasks SET done=? WHERE id=?", (int(check), task_id))
                    conn.commit()
                    st.rerun()
            
            with col2:
                st.markdown(f"""
                <div class="task-card">
                    <span class="task-text {'done' if done else ''}">
                        {task_text}
                        <span class="{badge_class}">{priority}</span>
                    </span>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                if st.button("🗑️", key=f"delete_{task_id}", help="Delete task"):
                    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
                    conn.commit()
                    st.rerun()

# Close the main card container
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- STATS SECTION (Optional) ----------------
if tasks:
    total = len(tasks)
    pending = len([t for t in tasks if not t[2]])
    completed = len([t for t in tasks if t[2]])
    
    st.markdown(f"""
    <div style="
        margin-top: 1rem;
        padding: 1rem;
        background: {colors['glass_effect']};
        border-radius: 20px;
        backdrop-filter: blur(8px);
        border: 1px solid {colors['card_border']};
        text-align: center;
        color: {colors['task_text']};
    ">
        📊 Total: {total} | ⏳ Pending: {pending} | ✅ Completed: {completed}
    </div>
    """, unsafe_allow_html=True)

















