
import streamlit as st
import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Habit Tracker Heatmap", layout="wide")

# Title
st.title("📅 Habit Completion Heatmap Dashboard")
st.markdown("This dashboard visualizes each user's daily habit completion using a heatmap.")

# Load habit_data.json
try:
    with open("habit_data.json", "r") as f:
        data = json.load(f)
except:
    st.error("⚠️ Please upload the `habit_data.json` file below.")
    uploaded = st.file_uploader("Upload your `habit_data.json`", type="json")
    if uploaded:
        data = json.load(uploaded)
    else:
        st.stop()

# Flatten the data
records = []
for entry in data:
    user = entry.get('user')
    date = entry.get('date')
    logs = entry.get('daily_log', [])
    for log in logs:
        habit = log.get('habit')
        completed = 1 if log.get('completed') else 0
        records.append({
            'user': user,
            'date': date,
            'habit': habit,
            'completed': completed
        })

df = pd.DataFrame(records)

# Sidebar user selection
users = df['user'].unique()
selected_user = st.sidebar.selectbox("Select User", users)

# Filter data
user_df = df[df['user'] == selected_user]
user_df['date'] = pd.to_datetime(user_df['date'])

# Pivot table for heatmap
pivot_df = user_df.pivot_table(index='date', columns='habit', values='completed', fill_value=0)
pivot_df = pivot_df.sort_index()

# Show heatmap
st.write(f"### Heatmap for: `{selected_user}`")
fig, ax = plt.subplots(figsize=(12, len(pivot_df)*0.3))
sns.heatmap(pivot_df, cmap="Greens", linewidths=0.5, linecolor="gray", cbar=False, ax=ax)
st.pyplot(fig)
