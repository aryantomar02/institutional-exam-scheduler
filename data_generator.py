
import pandas as pd
import random
import numpy as np

def generate_data():
    departments = ["CSE","ECE","ME","CE","EE","IT","AI"]
    sections = ["A","B","C","D","E","F"]
    
    common_subjects = ["Engineering_Math_IV","Environmental_Studies","Professional_Ethics"]
    
    dept_core = {
        "CSE":["DSA","OS","DBMS","CN"],
        "ECE":["Signals","Control","Microprocessors","Analog"],
        "ME":["Thermodynamics","Fluid_Mechanics","Kinematics","Manufacturing"],
        "CE":["Structural","Geotechnical","Hydrology","Transportation"],
        "EE":["Power_Systems","Electrical_Machines","Power_Electronics","Control_Theory"],
        "IT":["Web_Tech","Cloud","Cyber_Security","Data_Analytics"],
        "AI":["ML","Deep_Learning","AI_Planning","Computer_Vision"]
    }
    
    electives = ["Elective1","Elective2","Elective3","Elective4"]
    
    students = []
    student_id = 1000
    
    for dept in departments:
        for sec in sections:
            for _ in range(60):
                name = f"Student_{student_id}"
                subjects = common_subjects + dept_core[dept] + random.sample(electives,1)
                attendance = int(np.clip(np.random.normal(82,8),60,100))
                debarred = "Yes" if random.random() < 0.05 else "No"
                students.append([student_id,name,dept,sec,"2nd","4",
                                 ",".join(subjects),attendance,debarred])
                student_id += 1

    students_df = pd.DataFrame(students, columns=[
        "Student_ID","Name","Department","Section",
        "Year","Semester","Subjects","Attendance","Debarred"
    ])

    rooms = []
    for i in range(1,121):
        rooms.append([f"R{i}","Block-"+str((i%5)+1),(i%4)+1,30])
    rooms_df = pd.DataFrame(rooms, columns=["Room_ID","Building","Floor","Capacity"])

    students_df.to_excel("data/students.xlsx", index=False)
    rooms_df.to_excel("data/rooms.xlsx", index=False)

if __name__ == "__main__":
    generate_data()
