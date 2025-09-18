# # models.py
# from dataclasses import dataclass
# from db import DB
# from typing import Optional, List, Dict
# from datetime import date

# db = DB()

# @dataclass
# class Student:
#     roll: str
#     first_name: str
#     last_name: Optional[str] = ''
#     class_name: Optional[str] = ''
#     section: Optional[str] = ''
#     student_id: Optional[int] = None

#     @staticmethod
#     def add(student: 'Student') -> int:
#         q = "INSERT INTO students (roll, first_name, last_name, class, section) VALUES (%s,%s,%s,%s,%s)"
#         cursor = db.execute(q, (student.roll, student.first_name, student.last_name, student.class_name, student.section))
#         return cursor.lastrowid

#     @staticmethod
#     def get_all() -> List[Dict]:
#         return db.fetchall("SELECT * FROM students ORDER BY roll")

#     @staticmethod
#     def find_by_roll(roll: str) -> Optional[Dict]:
#         return db.fetchone("SELECT * FROM students WHERE roll=%s", (roll,))

# @dataclass
# class Teacher:
#     username: str
#     full_name: str
#     email: Optional[str] = None
#     teacher_id: Optional[int] = None

#     @staticmethod
#     def get_by_username(username: str):
#         return db.fetchone("SELECT * FROM teachers WHERE username=%s", (username,))

# @dataclass
# class AttendanceRecord:
#     student_id: int
#     date: date
#     status: str = 'present'
#     teacher_id: Optional[int] = None
#     remarks: Optional[str] = None

#     def save(self):
#         # Upsert logic: try update, else insert
#         existing = db.fetchone("SELECT * FROM attendance WHERE student_id=%s AND date=%s", (self.student_id, self.date))
#         if existing:
#             q = "UPDATE attendance SET status=%s, teacher_id=%s, remarks=%s WHERE attendance_id=%s"
#             db.execute(q, (self.status, self.teacher_id, self.remarks, existing['attendance_id']))
#             return existing['attendance_id']
#         else:
#             q = "INSERT INTO attendance (student_id, teacher_id, date, status, remarks) VALUES (%s,%s,%s,%s,%s)"
#             cursor = db.execute(q, (self.student_id, self.teacher_id, self.date, self.status, self.remarks))
#             return cursor.lastrowid

#     @staticmethod
#     def get_by_date(d):
#         return db.fetchall("SELECT a.*, s.roll, s.first_name, s.last_name FROM attendance a JOIN students s ON a.student_id=s.student_id WHERE a.date=%s ORDER BY s.roll", (d,))

from db import Database

db = Database()

class Student:
    def __init__(self, roll, first_name, last_name, class_name="", section=""):
        self.roll = roll
        self.first_name = first_name
        self.last_name = last_name
        self.class_name = class_name
        self.section = section

    @staticmethod
    def add(student):
        q = "INSERT INTO students (roll, first_name, last_name, class_name, section) VALUES (%s, %s, %s, %s, %s)"
        db.execute(q, (student.roll, student.first_name, student.last_name, student.class_name, student.section))

    @staticmethod
    def view_all():
        q = "SELECT * FROM students"
        return db.fetchall(q)


class Attendance:
    @staticmethod
    def mark(roll, date, status):
        q = "INSERT INTO attendance (roll, date, status) VALUES (%s, %s, %s)"
        db.execute(q, (roll, date, status))

    @staticmethod
    def view(roll):
        q = "SELECT * FROM attendance WHERE roll=%s"
        return db.fetchall(q, (roll,))

    # ✅ Added for GUI
    @staticmethod
    def view_attendance_gui(roll):
        q = "SELECT date, status FROM attendance WHERE roll=%s ORDER BY date DESC"
        return db.fetchall(q, (roll,))
