
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scheduler_engine import *

st.set_page_config(layout="wide")
st.title("Elite Institutional Exam Scheduling System")

if st.button("Generate Realistic Dummy Dataset"):
    import data_generator
    data_generator.generate_data()
    st.success("Dataset generated inside data folder")

students_file = st.file_uploader("Upload Students File", type=["xlsx"])
rooms_file = st.file_uploader("Upload Rooms File", type=["xlsx"])

if students_file and rooms_file:
    students = pd.read_excel(students_file)
    rooms = pd.read_excel(rooms_file)

    eligible = filter_students(students)
    subject_students = build_subject_map(eligible)
    G = build_graph(subject_students)
    subject_day = assign_days(G)
    alloc_df, seat_df = allocate_rooms(subject_day, subject_students, eligible, rooms)

    st.success("Scheduling Completed Successfully")

    st.subheader("Exam Days Distribution")
    day_counts = pd.Series(subject_day).value_counts()
    fig = plt.figure()
    plt.bar(day_counts.index, day_counts.values)
    st.pyplot(fig)

    st.subheader("Master Schedule Preview")
    st.dataframe(alloc_df.head(20))

    st.subheader("Student Exam Calendar Preview")
    st.dataframe(seat_df.head(20))

    alloc_df.to_excel("output/Master_Schedule.xlsx", index=False)
    seat_df.to_excel("output/Student_Exam_Calendar.xlsx", index=False)

    st.download_button("Download Master Schedule", open("output/Master_Schedule.xlsx","rb"), file_name="Master_Schedule.xlsx")
    st.download_button("Download Student Calendar", open("output/Student_Exam_Calendar.xlsx","rb"), file_name="Student_Exam_Calendar.xlsx")
