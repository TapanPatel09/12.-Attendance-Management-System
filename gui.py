# # gui.py
# import tkinter as tk
# from tkinter import ttk, messagebox
# from models import Student, AttendanceRecord
# from utils import validate_roll, ValidationError, log_attendance_csv
# from datetime import date
# from db import DB

# class AttendanceApp:
#     def __init__(self, root, teacher=None):
#         self.root = root
#         self.teacher = teacher
#         self.root.title("Attendance Sheet")
#         self.db = DB()
#         self.build_ui()
#         self.load_students()

#     def build_ui(self):
#         frm = ttk.Frame(self.root, padding=10)
#         frm.pack(fill='both', expand=True)

#         top = ttk.Frame(frm)
#         top.pack(fill='x', pady=5)
#         ttk.Label(top, text=f"Date: {date.today().isoformat()}").pack(side='left')
#         ttk.Button(top, text="Refresh", command=self.load_students).pack(side='right')

#         # Treeview for students
#         cols = ('roll','name','status','remarks')
#         self.tree = ttk.Treeview(frm, columns=cols, show='headings', height=20)
#         for c in cols:
#             self.tree.heading(c, text=c.title())
#             self.tree.column(c, width=120)
#         self.tree.pack(fill='both', expand=True)

#         # Right-click or buttons to change status
#         btns = ttk.Frame(frm)
#         btns.pack(fill='x', pady=5)
#         ttk.Button(btns, text="Present", command=lambda: self.set_status('present')).pack(side='left', padx=4)
#         ttk.Button(btns, text="Absent", command=lambda: self.set_status('absent')).pack(side='left', padx=4)
#         ttk.Button(btns, text="Late", command=lambda: self.set_status('late')).pack(side='left', padx=4)
#         ttk.Button(btns, text="Excused", command=lambda: self.set_status('excused')).pack(side='left', padx=4)
#         ttk.Button(btns, text="Save", command=self.save_all).pack(side='right', padx=4)

#     def load_students(self):
#         for i in self.tree.get_children():
#             self.tree.delete(i)
#         students = Student.get_all()
#         for s in students:
#             name = f"{s['first_name']} {s.get('last_name') or ''}".strip()
#             self.tree.insert('', 'end', iid=s['student_id'], values=(s['roll'], name, 'present', ''))

#     def set_status(self, status):
#         sel = self.tree.selection()
#         if not sel:
#             messagebox.showinfo("Select", "Please select at least one student row.")
#             return
#         for iid in sel:
#             vals = list(self.tree.item(iid, 'values'))
#             vals[2] = status
#             self.tree.item(iid, values=vals)

#     def save_all(self):
#         rows = []
#         recs_for_log = []
#         for iid in self.tree.get_children():
#             student_id = int(iid)
#             roll, name, status, remarks = self.tree.item(iid, 'values')
#             rec = AttendanceRecord(student_id=student_id, date=date.today(), status=status, teacher_id=(self.teacher and self.teacher.get('teacher_id')), remarks=remarks)
#             try:
#                 rec.save()
#                 rows.append({'student_id': student_id, 'status': status})
#                 recs_for_log.append({'date': date.today().isoformat(), 'roll': roll, 'first_name': name, 'status': status, 'remarks': remarks})
#             except Exception as e:
#                 messagebox.showerror("Error", f"Failed to save for {roll}: {e}")
#                 return
#         csv_file = log_attendance_csv(recs_for_log)
#         messagebox.showinfo("Saved", f"Saved {len(rows)} records.\nCSV log: {csv_file}")


import tkinter as tk
from tkinter import ttk, messagebox
from models import Student, Attendance
import datetime

root = tk.Tk()
root.title("Attendance Management System")
root.geometry("700x500")

# ---------- Add Student ----------
def add_student_window():
    win = tk.Toplevel(root)
    win.title("Add Student")

    tk.Label(win, text="Roll").grid(row=0, column=0)
    tk.Label(win, text="First Name").grid(row=1, column=0)
    tk.Label(win, text="Last Name").grid(row=2, column=0)
    tk.Label(win, text="Class").grid(row=3, column=0)
    tk.Label(win, text="Section").grid(row=4, column=0)

    roll = tk.Entry(win); roll.grid(row=0, column=1)
    fn = tk.Entry(win); fn.grid(row=1, column=1)
    ln = tk.Entry(win); ln.grid(row=2, column=1)
    cl = tk.Entry(win); cl.grid(row=3, column=1)
    sec = tk.Entry(win); sec.grid(row=4, column=1)

    def save_student():
        try:
            Student.add(Student(roll.get(), fn.get(), ln.get(), cl.get(), sec.get()))
            messagebox.showinfo("Success", "Student Added Successfully")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Save", command=save_student).grid(row=5, column=0, columnspan=2)


# ---------- Mark Attendance ----------
def mark_attendance_window():
    win = tk.Toplevel(root)
    win.title("Mark Attendance")

    tk.Label(win, text="Roll").grid(row=0, column=0)
    roll = tk.Entry(win); roll.grid(row=0, column=1)

    tk.Label(win, text="Date (YYYY-MM-DD)").grid(row=1, column=0)
    date = tk.Entry(win); date.grid(row=1, column=1)
    date.insert(0, str(datetime.date.today()))

    tk.Label(win, text="Status").grid(row=2, column=0)
    status = ttk.Combobox(win, values=["Present", "Absent"])
    status.grid(row=2, column=1)
    status.current(0)

    def save_attendance():
        try:
            Attendance.mark(roll.get(), date.get(), status.get())
            messagebox.showinfo("Success", "Attendance Marked Successfully")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Save", command=save_attendance).grid(row=3, column=0, columnspan=2)


# ---------- Show Attendance ----------
frame = tk.Frame(root)
frame.pack(fill="both", expand=True, padx=10, pady=10)

tk.Label(frame, text="Enter Roll to View Attendance:").grid(row=0, column=0)
roll = tk.Entry(frame)
roll.grid(row=0, column=1)

tree = ttk.Treeview(frame, columns=("Date", "Status"), show="headings")
tree.heading("Date", text="Date")
tree.heading("Status", text="Status")
tree.grid(row=1, column=0, columnspan=3, pady=10)

def load():
    try:
        tree.delete(*tree.get_children())  # clear old data
        records = Attendance.view_attendance_gui(roll.get())
        for row in records:
            tree.insert("", "end", values=row)
    except Exception as e:
        messagebox.showerror("Error", str(e))

tk.Button(frame, text="Show Attendance", command=load).grid(row=0, column=2)


# ---------- Main Buttons ----------
tk.Button(root, text="Add Student", width=20, command=add_student_window).pack(pady=5)
tk.Button(root, text="Mark Attendance", width=20, command=mark_attendance_window).pack(pady=5)

root.mainloop()
