
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Road Accident Analysis", page_icon="🚦", layout="wide")

st.markdown("""
<style>
.stApp {background-color:#f4f6f9;}

.main-title {
    font-size:38px;
    font-weight:700;
    color:#172554;
    text-align:center;
    margin-bottom:25px;
}

.kpi-card {
    padding:14px 10px;
    border-radius:12px;
    color:white;
    height:92px;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    text-align:center;
    box-shadow:0 3px 10px rgba(0,0,0,.10);
    margin-bottom:18px;
}

.kpi-title {font-size:12px; font-weight:600; opacity:.9;}
.kpi-value {font-size:24px; font-weight:700; margin-top:5px;}

section[data-testid="stSidebar"] {background-color:#172554;}
section[data-testid="stSidebar"] * {color:white;}

section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    border-color:#93c5fd;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] > div:focus-within {
    border-color:#93c5fd;
    box-shadow:0 0 0 1px #93c5fd;
}

section[data-testid="stSidebar"] span[data-baseweb="tag"] {
    background-color:#93c5fd;
    color:#0f172a !important;
    font-weight:600;
}

.stDownloadButton > button:hover {
    background-color:#dc2626;
    color:white;
    border-color:#dc2626;
}

.footer {
    text-align:center;
    color:#64748b;
    font-size:13px;
    margin-top:12px;
}
</style>
""", unsafe_allow_html=True)

df = pd.read_csv("data/accident_data_cleaned.csv")
df["hour"] = df["hrmn"] // 100

def get_time_period(h):
    if 5 <= h < 12:
        return "Morning"
    elif 12 <= h < 17:
        return "Afternoon"
    elif 17 <= h < 21:
        return "Evening"
    return "Night"

df["time_period"] = df["hour"].apply(get_time_period)

st.markdown(
    '<div class="main-title">🚦 Road Accident Analysis in India</div>',
    unsafe_allow_html=True
)

st.sidebar.markdown("## 🔎 Dashboard Filters")

states = sorted(df["state"].unique())
severities = sorted(df["severity"].unique())
weather = sorted(df["weather"].unique())
vehicles = sorted(df["vehicle_type"].unique())
times = ["Morning", "Afternoon", "Evening", "Night"]

selected_states = st.sidebar.multiselect("State", states, default=states)
selected_severity = st.sidebar.multiselect("Severity", severities, default=severities)
selected_weather = st.sidebar.multiselect("Weather", weather, default=weather)
selected_vehicles = st.sidebar.multiselect("Vehicle Type", vehicles, default=vehicles)
selected_time = st.sidebar.multiselect("Time of Day", times, default=times)

filtered_df = df[
    df["state"].isin(selected_states) &
    df["severity"].isin(selected_severity) &
    df["weather"].isin(selected_weather) &
    df["vehicle_type"].isin(selected_vehicles) &
    df["time_period"].isin(selected_time)
]

total_accidents = len(filtered_df)
total_states = filtered_df["state"].nunique()
avg_driver = filtered_df["driver_age"].mean() if total_accidents else 0
avg_casualty = filtered_df["casualty_age"].mean() if total_accidents else 0

kpis = [
    ("TOTAL ACCIDENTS", f"{total_accidents:,} Accidents", "#2563eb"),
    ("STATES COVERED", f"{total_states} States", "#0f766e"),
    ("AVG DRIVER AGE", f"{avg_driver:.1f} Years", "#d97706"),
    ("AVG CASUALTY AGE", f"{avg_casualty:.1f} Years", "#7c3aed")
]

for col, (title, value, bg) in zip(st.columns(4), kpis):
    with col:
        st.markdown(
            f"""
            <div class="kpi-card" style="background:{bg};">
                <div class="kpi-title">{title}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

height = 300
margin = dict(l=20, r=20, t=50, b=20)

col1, col2 = st.columns(2)

with col1:
    data = filtered_df["state"].value_counts().reset_index()
    data.columns = ["state", "accidents"]

    fig = px.bar(
        data,
        x="accidents",
        y="state",
        orientation="h",
        title="Accidents by State",
        color="accidents",
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        height=height,
        margin=margin,
        showlegend=False,
        yaxis=dict(categoryorder="total ascending")
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    data = filtered_df["severity"].value_counts().reset_index()
    data.columns = ["severity", "accidents"]

    fig = px.pie(
        data,
        names="severity",
        values="accidents",
        title="Accidents by Severity",
        hole=.45
    )

    fig.update_layout(
        height=height,
        margin=margin,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-.15,
            xanchor="center",
            x=.5
        )
    )

    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    data = filtered_df["weather"].value_counts().reset_index()
    data.columns = ["weather", "accidents"]

    fig = px.bar(
        data,
        x="weather",
        y="accidents",
        title="Accidents by Weather",
        color="weather",
        color_discrete_sequence=[
            "#0ea5e9", "#6366f1", "#14b8a6", "#64748b", "#8b5cf6"
        ]
    )

    fig.update_layout(
        height=height,
        margin=margin,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    data = (
        filtered_df["time_period"]
        .value_counts()
        .reindex(times, fill_value=0)
        .reset_index()
    )
    data.columns = ["time_period", "accidents"]

    fig = px.line(
        data,
        x="time_period",
        y="accidents",
        title="Accidents by Time of Day",
        markers=True
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=9)
    )

    fig.update_layout(
        height=height,
        margin=margin,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    data = filtered_df["vehicle_type"].value_counts().reset_index()
    data.columns = ["vehicle_type", "accidents"]

    fig = px.pie(
        data,
        names="vehicle_type",
        values="accidents",
        title="Accidents by Vehicle Type",
        hole=.45
    )

    fig.update_layout(
        height=height,
        margin=margin,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-.15,
            xanchor="center",
            x=.5
        )
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    data = filtered_df["week_day"].value_counts().sort_index().reset_index()
    data.columns = ["day", "accidents"]

    fig = px.scatter(
        data,
        x="day",
        y="accidents",
        title="Accidents by Day",
        size="accidents"
    )

    fig.update_traces(
        marker=dict(size=18, line=dict(width=1))
    )

    fig.update_layout(
        height=height,
        margin=margin,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

try:
    with open("outputs/analysis_summary.txt", encoding="utf-8") as file:
        summary = file.read()
except FileNotFoundError:
    summary = (
        "Road Accident Analysis in India\n\n"
        f"Total Accidents: {total_accidents}\n"
        f"States Covered: {total_states}\n"
        f"Average Driver Age: {avg_driver:.1f} years\n"
        f"Average Casualty Age: {avg_casualty:.1f} years\n"
    )

st.download_button(
    "⬇️ Download Summary",
    summary,
    "road_accident_analysis_summary.txt",
    "text/plain"
)

st.markdown(
    '<div class="footer">'
    'Road Accident Analysis in India • Python Data Analytics Project'
    '<br><br><b>Developed by Parul Giri</b>'
    '</div>',
    unsafe_allow_html=True
)