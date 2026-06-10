import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="EduLens Student Performance Analytics",
    page_icon="🎓",
    layout="wide"
)

# --------------------------------
# LOAD DATA
# --------------------------------
df = pd.read_csv("../data/student_clean.csv")

# --------------------------------
# DATA CLEANING
# --------------------------------
df["Math"] = pd.to_numeric(df["Math"])
df["Science"] = pd.to_numeric(df["Science"])
df["English"] = pd.to_numeric(df["English"])
df["Attendance"] = pd.to_numeric(df["Attendance"])

# Average Marks
df["AverageMarks"] = (
    df[["Math", "Science", "English"]]
    .mean(axis=1)
)

# Attendance Categories
df["Attendance Group"] = df["Attendance"].apply(
    lambda x:
    "Excellent" if x >= 90
    else "Good" if x >= 75
    else "Average"
)

# --------------------------------
# GREEN THEME
# --------------------------------
DARK_GREEN = "#3d6b5a"
MEDIUM_GREEN = "#6d9b8c"
LIGHT_GREEN = "#b7d5cc"
EXTRA_LIGHT_GREEN = "#dcebe6"

# --------------------------------
# SIDEBAR FILTER
# --------------------------------
st.sidebar.header("Student Filter")

selected_student = st.sidebar.selectbox(
    "Select Student",
    ["All"] + sorted(df["Name"].unique().tolist())
)

if selected_student != "All":
    df = df[df["Name"] == selected_student]

# --------------------------------
# KPI CALCULATIONS
# --------------------------------
avg_marks = df["AverageMarks"].mean()

top_score = df["AverageMarks"].max()

total_students = len(df)

avg_attendance = df["Attendance"].mean()

# --------------------------------
# TITLE
# --------------------------------
st.markdown(
    """
    <h1 style='text-align:center;
               color:#2f5e50;'>
    🎓 EduLens Student Performance Analytics
    </h1>
    """,
    unsafe_allow_html=True
)

# --------------------------------
# KPI ROW
# --------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average Marks",
        f"{avg_marks:.0f}"
    )

with col2:
    st.metric(
        "Top Score",
        f"{top_score:.0f}"
    )

with col3:
    st.metric(
        "Total Students",
        total_students
    )

with col4:
    st.metric(
        "Average Attendance %",
        f"{avg_attendance:.1f}%"
    )

st.markdown("---")

# --------------------------------
# ROW 2
# --------------------------------
col5, col6 = st.columns(2)

with col5:

    student_marks = (
        df[["Name", "AverageMarks"]]
        .sort_values(
            "AverageMarks",
            ascending=False
        )
    )

    fig1 = px.bar(
        student_marks,
        x="AverageMarks",
        y="Name",
        orientation="h",
        text="AverageMarks",
        color="AverageMarks",
        color_continuous_scale=[
            EXTRA_LIGHT_GREEN,
            LIGHT_GREEN,
            MEDIUM_GREEN,
            DARK_GREEN
        ]
    )

    fig1.update_traces(
        texttemplate="%{text:.0f}",
        textposition="inside",
        textfont_color="black"
    )

    fig1.update_layout(
        title="Average Marks by Student",
        xaxis_title="Average Marks",
        yaxis_title="Student Name",
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with col6:

    subject_df = pd.DataFrame({
        "Student": df["Name"],
        "Math": df["Math"],
        "Science": df["Science"],
        "English": df["English"]
    })

    fig2 = px.bar(
        subject_df,
        x="Student",
        y=[
            "Math",
            "Science",
            "English"
        ],
        barmode="group"
    )

    fig2.data[0].marker.color = "#b7d5cc"
    fig2.data[1].marker.color = "#6d9b8c"
    fig2.data[2].marker.color = "#3d6b5a"

    fig2.update_layout(
        title="Subject Performance",
        xaxis_title="Student Name",
        yaxis_title="Average of Subjects"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.markdown("---")

# --------------------------------
# ROW 3
# --------------------------------
col7, col8 = st.columns(2)

with col7:

    attendance_df = (
        df["Attendance Group"]
        .value_counts()
        .reset_index()
    )

    attendance_df.columns = [
        "Attendance Group",
        "Count"
    ]

    fig3 = px.pie(
        attendance_df,
        names="Attendance Group",
        values="Count",
        hole=0.58,
        color="Attendance Group",
        color_discrete_map={
            "Excellent": LIGHT_GREEN,
            "Good": DARK_GREEN,
            "Average": MEDIUM_GREEN
        }
    )

    fig3.update_traces(
        textinfo="value+percent"
    )

    fig3.update_layout(
        title="Attendance Distribution"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

with col8:

    student_dist = (
        df["Name"]
        .value_counts()
        .reset_index()
    )

    student_dist.columns = [
        "Name",
        "Count"
    ]

    fig4 = px.pie(
        student_dist,
        names="Name",
        values="Count",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig4.update_traces(
    textinfo="percent+label",
    texttemplate="%{label}<br>%{percent:.1%}"
)

    fig4.update_layout(
        title="Student Distribution"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

st.markdown("---")

# --------------------------------
# DATASET TABLE
# --------------------------------
st.subheader(
    "Student Dataset"
)

st.dataframe(
    df,
    use_container_width=True
)