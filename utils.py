# utils.py
import re
from datetime import date, datetime
import csv
import os

ROLL_REGEX = re.compile(r'^[A-Za-z0-9\-\/]+$')  # modify to fit your roll format

class ValidationError(Exception):
    pass

def validate_roll(roll: str):
    if not roll or not ROLL_REGEX.match(roll):
        raise ValidationError(f"Invalid roll format: '{roll}'")
    return True

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def log_attendance_csv(records, out_dir='attendance_logs'):
    """
    records: list of dicts with keys: roll, first_name, status, date, remarks
    """
    ensure_dir(out_dir)
    filename = os.path.join(out_dir, f"attendance_{date.today().isoformat()}.csv")
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['date','roll','first_name','status','remarks'])
        if not file_exists:
            writer.writeheader()
        for r in records:
            writer.writerow({
                'date': r.get('date', date.today().isoformat()),
                'roll': r.get('roll'),
                'first_name': r.get('first_name'),
                'status': r.get('status'),
                'remarks': r.get('remarks','')
            })
    return filename
