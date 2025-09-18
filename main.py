# # quick_add_student.py
# from models import Student
# from utils import validate_roll, ValidationError

# def add_sample():
#     r = input("Enter roll: ").strip()
#     try:
#         validate_roll(r)
#     except ValidationError as e:
#         print(e); return
#     fn = input("First name: ").strip()
#     ln = input("Last name: ").strip()
#     Student.add(Student(roll=r, first_name=fn, last_name=ln))
#     print("Added.")

# if __name__ == '__main__':
#     add_sample()



from models import Student, Attendance
from datetime import date

def add_student():
    r = input("Enter roll: ")
    fn = input("First name: ")
    ln = input("Last name: ")
    c = input("Class: ")
    s = input("Section: ")
    Student.add(Student(r, fn, ln, c, s))

def mark_attendance():
    r = input("Enter roll: ")
    d = input("Enter date (YYYY-MM-DD, leave empty for today): ")
    if not d:
        d = date.today().strftime("%Y-%m-%d")
    st = input("Enter status (Present/Absent): ")
    Attendance.mark_attendance(r, d, st)

def view_attendance():
    r = input("Enter roll: ")
    Attendance.view_attendance(r)


if __name__ == "__main__":
    while True:
        print("\n--- Attendance Management ---")
        print("1. Add Student")
        print("2. Mark Attendance")
        print("3. View Attendance")
        print("4. Exit")
        ch = input("Enter choice: ")

        if ch == "1":
            add_student()
        elif ch == "2":
            mark_attendance()
        elif ch == "3":
            view_attendance()
        elif ch == "4":
            break
        else:
            print("❌ Invalid choice!")
