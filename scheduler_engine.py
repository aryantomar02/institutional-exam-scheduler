
import pandas as pd
import networkx as nx
import math
from collections import defaultdict
from datetime import datetime, timedelta

def next_monday():
    today = datetime.today()
    days_ahead = (7 - today.weekday()) % 7
    if days_ahead == 0:
        days_ahead = 7
    return today + timedelta(days=days_ahead)

def generate_exam_dates(num_days):
    start_date = next_monday()
    dates = []
    current = start_date
    while len(dates) < num_days:
        if current.weekday() < 5:
            dates.append(current.date())
        current += timedelta(days=1)
    return dates

def filter_students(df):
    return df[(df["Attendance"] >= 75) & (df["Debarred"] == "No")]

def build_subject_map(students):
    subject_students = defaultdict(set)
    for _, row in students.iterrows():
        for sub in row["Subjects"].split(","):
            subject_students[sub.strip()].add(row["Student_ID"])
    return subject_students

def build_graph(subject_students):
    G = nx.Graph()
    G.add_nodes_from(subject_students.keys())
    student_map = defaultdict(list)
    for subject, studs in subject_students.items():
        for s in studs:
            student_map[s].append(subject)
    for subs in student_map.values():
        for i in range(len(subs)):
            for j in range(i+1,len(subs)):
                G.add_edge(subs[i],subs[j])
    return G

def assign_days(G):
    subject_day = {}
    sorted_nodes = sorted(G.nodes(), key=lambda x: G.degree(x), reverse=True)
    for node in sorted_nodes:
        used_days = {subject_day[n] for n in G.neighbors(node) if n in subject_day}
        day = 1
        while day in used_days:
            day += 1
        subject_day[node] = day
    return subject_day

def allocate_rooms(subject_day, subject_students, students_df, rooms_df):
    allocation = []
    seating = []
    capacity = 30
    
    max_day = max(subject_day.values())
    exam_dates = generate_exam_dates(max_day)
    
    for subject, day in subject_day.items():
        studs = list(subject_students.get(subject, []))
        date = exam_dates[day-1]
        
        for i in range(0,len(studs),capacity):
            room = rooms_df.iloc[(i//capacity)%len(rooms_df)]["Room_ID"]
            chunk = studs[i:i+capacity]
            allocation.append([date,day,subject,room,len(chunk)])
            
            for seat_no, sid in enumerate(chunk,1):
                student_info = students_df[students_df["Student_ID"]==sid].iloc[0]
                seating.append([sid,student_info["Name"],student_info["Department"],
                                subject,date,room,seat_no])
    
    alloc_df = pd.DataFrame(allocation, columns=["Date","Day_No","Subject","Room","Student_Count"])
    seat_df = pd.DataFrame(seating, columns=[
        "Student_ID","Name","Department","Subject","Date","Room","Seat_No"
    ])
    
    return alloc_df, seat_df
