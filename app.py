# ============================================================
#   JEE/PW DAILY STUDY TRACKER  —  Streamlit Web App Version
#   Run with:  streamlit run study_tracker_web.py
# ============================================================

# --- IMPORTS ---
# streamlit : The library that turns Python code into a web app
# json      : Save and load data as a text file
# datetime  : Work with today's date
# os        : Check if a file exists on the computer

import streamlit as st
import json
import datetime
import os


# ============================================================
# SECTION 1: PAGE CONFIG
# This MUST be the very first Streamlit command in the file.
# It sets the browser tab title, icon, and layout.
# ============================================================

st.set_page_config(
    page_title="JEE Study Tracker",
    page_icon="⚡",
    layout="centered"   # 'centered' keeps content in a neat column
)


# ============================================================
# SECTION 2: CUSTOM CSS STYLING
# Streamlit lets us inject CSS to style the page.
# st.markdown() with unsafe_allow_html=True renders raw HTML/CSS.
# ============================================================

st.markdown("""
<style>
/* ── Google Font import ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Global reset & background ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0f1117 !important;
    font-family: 'Inter', sans-serif !important;
    color: #e2e8f0 !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding-top: 2rem !important; max-width: 680px !important; }

/* ── Stat cards ── */
.stat-card {
    background: #1a1d2e;
    border-radius: 12px;
    padding: 18px 20px;
    text-align: center;
    border: 1px solid #2d3148;
}
.stat-value   { font-size: 2rem; font-weight: 800; margin: 4px 0; }
.stat-label   { font-size: 0.72rem; color: #64748b; font-weight: 600;
                letter-spacing: 0.08em; text-transform: uppercase; }
.stat-sub     { font-size: 0.78rem; color: #64748b; }

/* ── Task rows ── */
.task-row {
    background: #22263a;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 6px 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border: 1px solid #2d3148;
    transition: background 0.2s;
}
.task-row.done {
    background: #1a2e1a;
    border-color: #2d4a2d;
}
.task-name      { font-size: 1rem; font-weight: 500; }
.task-name.done { color: #4ade80; text-decoration: line-through;
                  text-decoration-color: #4ade8077; }
.badge-done     { background: #1a3a1a; color: #4ade80; padding: 3px 10px;
                  border-radius: 20px; font-size: 0.75rem; font-weight: 700;
                  border: 1px solid #4ade8044; }
.badge-pending  { background: #1e2238; color: #64748b; padding: 3px 10px;
                  border-radius: 20px; font-size: 0.75rem; font-weight: 600;
                  border: 1px solid #2d3148; }

/* ── Section headers ── */
.section-title {
    font-size: 0.72rem; font-weight: 700; color: #64748b;
    letter-spacing: 0.1em; text-transform: uppercase;
    margin: 24px 0 10px 2px;
}

/* ── Date bar ── */
.date-bar {
    background: #1a1d2e;
    border-radius: 10px;
    padding: 12px 18px;
    color: #94a3b8;
    font-size: 0.9rem;
    border: 1px solid #2d3148;
    margin-bottom: 16px;
}

/* ── History row ── */
.hist-row {
    background: #1a1d2e;
    border-radius: 10px;
    padding: 12px 18px;
    margin: 5px 0;
    border: 1px solid #2d3148;
    display: flex;
    align-items: center;
    gap: 16px;
}
.hist-day   { font-weight: 700; font-size: 0.9rem; min-width: 80px; }
.hist-date  { font-size: 0.78rem; color: #64748b; }
.hist-badge { font-size: 0.8rem; font-weight: 700; margin-left: auto; }

/* ── Progress bar styling (native Streamlit override) ── */
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #7c6af7, #4ade80) !important;
    border-radius: 99px !important;
    height: 10px !important;
}
[data-testid="stProgress"] > div {
    background: #22263a !important;
    border-radius: 99px !important;
    height: 10px !important;
}

/* ── Checkbox styling ── */
[data-testid="stCheckbox"] label {
    font-size: 1rem !important;
    color: #e2e8f0 !important;
    font-weight: 500 !important;
    cursor: pointer !important;
}
[data-testid="stCheckbox"] span { color: #e2e8f0 !important; }

/* ── Buttons ── */
.stButton > button {
    background: #7c6af7 !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 0.5rem 1.2rem !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* ── Success / info messages ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border: none !important;
}

/* ── Divider ── */
hr { border-color: #2d3148 !important; margin: 1.5rem 0 !important; }

/* ── Footer quote ── */
.footer-quote {
    color: #475569; font-style: italic;
    font-size: 0.82rem; text-align: center;
    padding: 16px 0 8px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #1a1d2e !important;
    border-right: 1px solid #2d3148 !important;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# SECTION 3: DATA FUNCTIONS
# These functions handle loading and saving progress to a file.
# In Streamlit, we use plain functions instead of a class.
# ============================================================

DATA_FILE = "progress_data.json"   # File where progress is stored

TASKS = [
    "📚  Physics Class",
    "⚗️  Chemistry Class",
    "📐  Maths Class",
    "📝  Notes Complete",
    "📋  Homework Complete",
    "💡  Question Practice",
]


def load_data():
    """
    Reads the JSON file and returns a Python dictionary.
    If the file doesn't exist yet, returns an empty dict {}.
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_data(data):
    """
    Writes the Python dictionary to the JSON file.
    indent=4 makes it easy to read the file manually.
    """
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_today_key():
    """Returns today's date as a string like '2024-01-15'."""
    return datetime.date.today().strftime("%Y-%m-%d")


def calculate_streak(data):
    """
    Counts how many days IN A ROW all tasks were completed.

    OLD logic: started from yesterday → today was never counted.
    NEW logic: start from TODAY first.
      - If today is fully done  → count it, then go backwards.
      - If today is not done yet → skip today, start from yesterday.
    This way the streak shows 1 the moment you finish all tasks today.
    """
    streak = 0
    today_key = datetime.date.today().strftime("%Y-%m-%d")

    # --- Step 1: Decide the starting date ---
    # Check if today's tasks are ALL completed (every value is True).
    today_complete = (
        today_key in data          # today has an entry  AND
        and len(data[today_key]) > 0   # it is not empty  AND
        and all(data[today_key].values())  # every task is True
    )

    if today_complete:
        # Today is done → start counting from today
        check_date = datetime.date.today()
    else:
        # Today is not done yet → start counting from yesterday
        check_date = datetime.date.today() - datetime.timedelta(days=1)

    # --- Step 2: Walk backwards day by day ---
    for _ in range(365):
        key = check_date.strftime("%Y-%m-%d")

        if key in data and all(data[key].values()):
            streak += 1                               # This day was perfect → add 1
            check_date -= datetime.timedelta(days=1)  # Move one day further back
        else:
            break   # Chain is broken → stop counting

    return streak


# ============================================================
# SECTION 4: SESSION STATE — Streamlit's "Memory"
#
# KEY CONCEPT FOR BEGINNERS:
# Streamlit reruns the ENTIRE script from top to bottom every
# time the user clicks anything (checkbox, button, etc.).
#
# This means normal Python variables would RESET each time!
#
# st.session_state is a special dictionary that PERSISTS
# between reruns. Think of it as the app's short-term memory.
#
# We use it to store: task checkboxes, loaded data, messages.
# ============================================================

# Load data from file (only once when app first starts)
if "all_data" not in st.session_state:
    # 'all_data' not in session_state means this is the first run
    st.session_state.all_data = load_data()

if "today_key" not in st.session_state:
    st.session_state.today_key = get_today_key()

# Make sure today has an entry in our data
today_key = st.session_state.today_key
if today_key not in st.session_state.all_data:
    st.session_state.all_data[today_key] = {task: False for task in TASKS}

# Initialize each task's checkbox state in session_state
# The key for each task is just the task name string.
for task in TASKS:
    if task not in st.session_state:
        st.session_state[task] = st.session_state.all_data[today_key].get(task, False)

# A flag to show the history section (toggled by a button)
if "show_history" not in st.session_state:
    st.session_state.show_history = False

# Store any message to show (success/info banners)
if "message" not in st.session_state:
    st.session_state.message = None


# ============================================================
# SECTION 5: HELPER — Sync checkboxes → data dictionary
#
# This function reads the current checkbox states from
# session_state and writes them into all_data[today_key].
# We call this before any save/reset operation.
# ============================================================

def sync_tasks_to_data():
    """Copy current checkbox values into the data dictionary."""
    for task in TASKS:
        st.session_state.all_data[today_key][task] = st.session_state[task]


def calculate_stats():
    """
    Returns a tuple: (done_count, total, percentage, remaining)
    Reads directly from session_state checkbox values.
    """
    total = len(TASKS)
    done = sum(1 for task in TASKS if st.session_state[task])
    remaining = total - done
    percentage = int((done / total) * 100)
    return done, total, percentage, remaining


# ============================================================
# SECTION 6: SIDEBAR
# The sidebar is a panel on the left side of the page.
# We put the motivational quote and quick info here.
# ============================================================

with st.sidebar:
    st.markdown("### ⚡ JEE Study Tracker")
    st.markdown("---")

    # Show today's date nicely
    today_display = datetime.date.today().strftime("%A\n%d %B %Y")
    st.markdown(f"📅 **{datetime.date.today().strftime('%d %B %Y')}**")
    st.markdown(f"*{datetime.date.today().strftime('%A')}*")

    st.markdown("---")

    # Motivational quotes — pick one based on day of year
    quotes = [
        "Success is the sum of small efforts repeated every day.",
        "JEE is a marathon, not a sprint. Consistency wins.",
        "Every expert was once a beginner. Keep going!",
        "Focus on progress, not perfection.",
        "One day at a time. One task at a time.",
        "The secret of getting ahead is getting started.",
        "Hard work beats talent when talent doesn't work hard.",
    ]
    quote = quotes[datetime.date.today().timetuple().tm_yday % len(quotes)]
    st.markdown(f"> *\"{quote}\"*")

    st.markdown("---")
    st.markdown("**How to use:**")
    st.markdown("1. ☑️ Check tasks as you complete them")
    st.markdown("2. 💾 Click **Save Progress** to save")
    st.markdown("3. 📊 View your **History** below")


# ============================================================
# SECTION 7: HEADER
# ============================================================

st.markdown(
    "<h1 style='color:#e2e8f0; font-weight:800; margin-bottom:4px;'>⚡ Study Tracker</h1>"
    "<p style='color:#64748b; margin-top:0;'>JEE / PW Daily Progress</p>",
    unsafe_allow_html=True
)

# Date bar
today_str = datetime.date.today().strftime("%A, %d %B %Y")
st.markdown(f"<div class='date-bar'>📅 &nbsp; {today_str}</div>", unsafe_allow_html=True)


# ============================================================
# SECTION 8: STATS CARDS
# We use st.columns() to create 3 side-by-side columns.
# ============================================================

done, total, percentage, remaining = calculate_stats()
streak = calculate_streak(st.session_state.all_data)

col1, col2, col3 = st.columns(3)   # Creates 3 equal-width columns

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Done</div>
        <div class="stat-value" style="color:#4ade80">{percentage}%</div>
        <div class="stat-sub">completion</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Tasks</div>
        <div class="stat-value" style="color:#7c6af7">{done}/{total}</div>
        <div class="stat-sub">completed</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Streak</div>
        <div class="stat-value" style="color:#fbbf24">{streak}🔥</div>
        <div class="stat-sub">day streak</div>
    </div>
    """, unsafe_allow_html=True)

# Small spacing
st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# SECTION 9: PROGRESS BAR
# st.progress() takes a value from 0.0 to 1.0
# We divide percentage by 100 to convert: 75% → 0.75
# ============================================================

st.markdown("<div class='section-title'>Progress</div>", unsafe_allow_html=True)
st.progress(percentage / 100)   # e.g., 50% → 0.50

# Show remaining tasks text
if percentage == 100:
    st.markdown(
        "<p style='color:#4ade80; font-size:0.85rem; margin-top:4px;'>"
        "🎉 All tasks completed! Amazing work!</p>",
        unsafe_allow_html=True
    )
else:
    st.markdown(
        f"<p style='color:#64748b; font-size:0.85rem; margin-top:4px;'>"
        f"{remaining} task{'s' if remaining > 1 else ''} remaining</p>",
        unsafe_allow_html=True
    )


# ============================================================
# SECTION 10: TASK CHECKBOXES
#
# KEY CONCEPT: st.checkbox()
# - Returns True if checked, False if not
# - 'key=' links it to st.session_state automatically
# - When user clicks it, Streamlit reruns the whole script
#   BUT session_state remembers the checkbox value!
#
# We show each task as:
#   [checkbox]   task name          [Done / Pending badge]
# ============================================================

st.markdown("<div class='section-title'>Today's Tasks</div>", unsafe_allow_html=True)

for task in TASKS:
    is_done = st.session_state[task]   # Current state: True or False

    # Build the HTML badge for the right side
    badge = (
        "<span class='badge-done'>✓ Done</span>"
        if is_done else
        "<span class='badge-pending'>○ Pending</span>"
    )

    # Row container (colored based on completion)
    row_class = "task-row done" if is_done else "task-row"

    # We use 2 columns: left for checkbox, right for badge
    left_col, right_col = st.columns([6, 1])

    with left_col:
        # st.checkbox with key= means its value is stored in session_state[task]
        # When the user clicks, Streamlit reruns and the new value is saved
        st.checkbox(
            label=task,
            key=task,           # This links directly to st.session_state[task]
        )

    with right_col:
        # Show Done/Pending badge on the right
        st.markdown(
            f"<div style='padding-top:8px; text-align:right;'>{badge}</div>",
            unsafe_allow_html=True
        )

    # Horizontal divider between tasks (thin line)
    st.markdown(
        "<hr style='margin:2px 0; border-color:#2d3148;'>",
        unsafe_allow_html=True
    )


# ============================================================
# SECTION 11: ACTION BUTTONS
#
# st.button() returns True ONLY in the single rerun when
# the button is clicked. So we put our logic inside `if`.
#
# We use 3 columns to place buttons side by side.
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

btn_col1, btn_col2, btn_col3 = st.columns([2, 2, 2])

# --- SAVE BUTTON ---
with btn_col1:
    if st.button("💾  Save Progress", use_container_width=True):
        # Step 1: Copy checkbox values into our data dict
        sync_tasks_to_data()
        # Step 2: Write data dict to the JSON file
        save_data(st.session_state.all_data)
        # Step 3: Set a message to display
        done_now, _, pct_now, _ = calculate_stats()
        if pct_now == 100:
            st.session_state.message = ("success", "🎉 Amazing! All tasks completed! Streak updated!")
        else:
            st.session_state.message = ("info", f"✅ Progress saved! {done_now}/{total} tasks done.")

# --- RESET BUTTON ---
with btn_col2:
    if st.button("🔄  Reset Today", use_container_width=True):
        # Set all tasks back to False in session_state
        for task in TASKS:
            st.session_state[task] = False
        # Update the data dict and save
        sync_tasks_to_data()
        save_data(st.session_state.all_data)
        st.session_state.message = ("warning", "🔄 Today's tasks have been reset.")

# --- HISTORY TOGGLE BUTTON ---
with btn_col3:
    history_label = "🔼  Hide History" if st.session_state.show_history else "📊  View History"
    if st.button(history_label, use_container_width=True):
        # Toggle the show_history flag
        st.session_state.show_history = not st.session_state.show_history


# ============================================================
# SECTION 12: SHOW MESSAGES
# Display the saved message (success/warning/info banner).
# ============================================================

if st.session_state.message:
    msg_type, msg_text = st.session_state.message

    if msg_type == "success":
        st.success(msg_text)
    elif msg_type == "warning":
        st.warning(msg_text)
    else:
        st.info(msg_text)

    # Clear the message so it doesn't show again on next rerun
    st.session_state.message = None


# ============================================================
# SECTION 13: HISTORY SECTION
# Shows the last 7 days of progress.
# Only visible when show_history is True.
# ============================================================

if st.session_state.show_history:
    st.markdown("---")
    st.markdown(
        "<h3 style='color:#e2e8f0; margin-bottom:4px;'>📊 Study History</h3>"
        "<p style='color:#64748b; font-size:0.85rem;'>Last 7 days of your progress</p>",
        unsafe_allow_html=True
    )

    # Sync current checkbox state before showing history
    sync_tasks_to_data()

    for i in range(7):
        # Calculate the date going backwards
        date = datetime.date.today() - datetime.timedelta(days=i)
        date_key = date.strftime("%Y-%m-%d")
        day_name = "Today" if i == 0 else date.strftime("%A")
        date_str = date.strftime("%d %b")

        if date_key in st.session_state.all_data:
            day_tasks = st.session_state.all_data[date_key]
            day_done = sum(1 for v in day_tasks.values() if v)
            day_total = len(day_tasks)
            day_pct = int((day_done / day_total) * 100) if day_total > 0 else 0
            all_done = day_done == day_total

            # Choose badge text and color
            if all_done:
                badge_html = "<span style='color:#4ade80; font-weight:700;'>✅ Perfect!</span>"
            elif day_pct > 0:
                badge_html = f"<span style='color:#7c6af7; font-weight:700;'>⚡ {day_pct}%</span>"
            else:
                badge_html = "<span style='color:#ef4444; font-weight:700;'>❌ Missed</span>"
        else:
            day_done, day_total, day_pct = 0, len(TASKS), 0
            badge_html = "<span style='color:#64748b;'>— No data</span>"

        # Display the history row using columns
        h_col1, h_col2, h_col3 = st.columns([2, 4, 2])

        with h_col1:
            st.markdown(
                f"<div style='padding:10px 0;'>"
                f"<div style='font-weight:700; color:#e2e8f0;'>{day_name}</div>"
                f"<div style='font-size:0.78rem; color:#64748b;'>{date_str}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

        with h_col2:
            # Show a mini progress bar using st.progress
            if day_pct > 0:
                st.progress(day_pct / 100)
            else:
                st.progress(0)

        with h_col3:
            st.markdown(
                f"<div style='padding:10px 0; text-align:right;'>{badge_html}</div>",
                unsafe_allow_html=True
            )


# ============================================================
# SECTION 14: FOOTER
# ============================================================

st.markdown("---")
st.markdown(
    f"<div class='footer-quote'>"
    f"\"{quote}\""
    f"</div>",
    unsafe_allow_html=True
)
st.markdown(
    "<div style='text-align:center; color:#2d3148; font-size:0.72rem; padding-bottom:16px;'>"
    "JEE/PW Study Tracker · Built with Python & Streamlit"
    "</div>",
    unsafe_allow_html=True
)
