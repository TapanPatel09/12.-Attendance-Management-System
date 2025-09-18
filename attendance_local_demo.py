# attendance_local_demo.py
import tkinter as tk
from tkinter import ttk, messagebox
import os, csv
from datetime import date

# Sample students — you can edit/add here or create students.csv with roll,first_name,last_name (optional)
SAMPLE_STUDENTS = [
    {'student_id': 1, 'roll': 'SE-001', 'first_name': 'Tapan', 'last_name': 'Patel'},
    {'student_id': 2, 'roll': 'SE-002', 'first_name': 'Rita', 'last_name': 'Shah'},
    {'student_id': 3, 'roll': 'SE-003', 'first_name': 'Amit', 'last_name': 'Patel'},
]

LOG_DIR = 'attendance_local_logs'
os.makedirs(LOG_DIR, exist_ok=True)

def load_students_from_csv(filename='students.csv'):
    if not os.path.isfile(filename):
        return SAMPLE_STUDENTS
    rows = []
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        sid = 1
        for r in reader:
            rows.append({
                'student_id': sid,
                'roll': r.get('roll') or f'R{sid:03}',
                'first_name': r.get('first_name') or '',
                'last_name': r.get('last_name') or ''
            })
            sid += 1
    return rows

class LocalAttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance — Local CSV Demo")
        self.students = load_students_from_csv()
        self.setup_ui()
        self.populate()

    def setup_ui(self):
        frm = ttk.Frame(self.root, padding=8)
        frm.pack(fill='both', expand=True)

        header = ttk.Frame(frm)
        header.pack(fill='x')
        ttk.Label(header, text=f"Date: {date.today().isoformat()}").pack(side='left')
        ttk.Button(header, text="Refresh", command=self.populate).pack(side='right')

        cols = ('roll', 'name', 'status', 'remarks')
        self.tree = ttk.Treeview(frm, columns=cols, show='headings', height=16)
        for c in cols:
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=140)
        self.tree.pack(fill='both', expand=True, pady=6)

        btns = ttk.Frame(frm)
        btns.pack(fill='x')
        for label, status in [('Present','present'), ('Absent','absent'), ('Late','late'), ('Excused','excused')]:
            ttk.Button(btns, text=label, command=lambda s=status: self.set_status(s)).pack(side='left', padx=4)
        ttk.Button(btns, text="Save (to CSV)", command=self.save_all).pack(side='right', padx=4)

    def populate(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for s in self.students:
            name = f"{s['first_name']} {s.get('last_name') or ''}".strip()
            self.tree.insert('', 'end', iid=str(s['student_id']), values=(s['roll'], name, 'present', ''))

    def set_status(self, status):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select", "Select at least one student.")
            return
        for iid in sel:
            vals = list(self.tree.item(iid, 'values'))
            vals[2] = status
            self.tree.item(iid, values=vals)

    def save_all(self):
        rows = []
        for iid in self.tree.get_children():
            roll, name, status, remarks = self.tree.item(iid, 'values')
            rows.append({
                'date': date.today().isoformat(),
                'roll': roll,
                'name': name,
                'status': status,
                'remarks': remarks
            })
        filename = os.path.join(LOG_DIR, f"attendance_{date.today().isoformat()}.csv")
        file_exists = os.path.isfile(filename)
        with open(filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['date','roll','name','status','remarks'])
            if not file_exists:
                writer.writeheader()
            for r in rows:
                writer.writerow(r)
        messagebox.showinfo("Saved", f"Saved {len(rows)} records to:\n{filename}")

if __name__ == '__main__':
    root = tk.Tk()
    app = LocalAttendanceApp(root)
    root.mainloop()
