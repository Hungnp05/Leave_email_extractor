import random
import json
from datetime import datetime, timedelta

# DATA POOLS
ho = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Vũ", "Đỗ", "Bùi", "Đặng", "Phan", "Dương", "Trịnh", "Đinh", "Lý", "Hồ"]
dem = ["Văn", "Thị", "Minh", "Quang", "Hữu", "Đức", "Gia", "Thanh", "Phú", "Đình", "Ngọc", "Hồng", "Kim"]
ten = ["Anh", "Bình", "Chi", "Dũng", "Hà", "Huy", "Lan", "Phúc", "Tuấn", "Vy", "Hùng", "Hưng", "Bách", "Mai", "Thảo", "Khang"]

ly_do_list = [
    ["bị", "ốm"],
    ["ốm", "nặng"],
    ["có", "việc", "gia", "đình"],
    ["đi", "khám", "bệnh"],
    ["chăm", "sóc", "con", "nhỏ"],
    ["giải", "quyết", "việc", "riêng"],
    ["nhà", "có", "đám", "cưới"],
    ["nhà", "có", "đám", "tang"],
    ["đi", "công", "tác"],
    ["bị", "tai", "nạn", "nhẹ"],
    ["con", "ốm"],
    ["về", "quê", "có", "việc"],
    ["đi", "du", "lịch", "gia", "đình"]
]

relative_dates = [
    ["hôm", "nay"],
    ["ngày", "mai"],
    ["ngày", "kia"],
    ["hôm", "qua"],
    ["cuối", "tuần", "này"],
    ["đầu", "tuần", "sau"],
    ["thứ", "hai", "tuần", "tới"],
    ["thứ", "ba", "tuần", "sau"],
    ["thứ", "tư", "tuần", "này"],
    ["thứ", "năm", "tuần", "tới"],
    ["thứ", "sáu", "tuần", "này"],
    ["cuối", "tháng", "này"],
    ["đầu", "tháng", "sau"]
]

sessions = [
    ["sáng"],
    ["chiều"],
    ["cả", "ngày"],
    ["sáng", "nay"],
    ["chiều", "mai"],
    ["cả", "ngày", "thứ", "sáu"]
]

session_map = {
    "sáng": "morning",
    "chiều": "afternoon",
    "cả ngày": "full_day",
    "sáng nay": "morning",
    "chiều mai": "afternoon",
    "cả ngày thứ sáu": "full_day"
}


# DATE GENERATOR
BASE_DATE = datetime(2025, 1, 1)

def random_absolute_date():
    delta = random.randint(0, 365)
    return BASE_DATE + timedelta(days=delta)

def format_absolute(date):
    formats = [
        date.strftime("%d/%m/%Y"),
        date.strftime("%d-%m-%Y"),
        f"ngày {date.day} tháng {date.month}",
        date.strftime("%d/%m")
    ]
    return random.choice(formats)

def random_relative_date():
    return " ".join(random.choice(relative_dates))

def generate_date_text():
    if random.random() < 0.6:
        date_obj = random_absolute_date()
        return format_absolute(date_obj), date_obj.strftime("%d/%m/%Y")
    else:
        text = random_relative_date()
        return text, text 

def generate_date_range():
    start = random_absolute_date()
    end = start + timedelta(days=random.randint(0, 5))
    return start, end


# TEMPLATE POOLS
templates_single = [
    "Tôi là {name} ({emp_id}) xin nghỉ phép {session} ngày {date} vì {reason}.",
    "Xin chào, tôi {name} mã {emp_id} xin nghỉ {session} {date} do {reason}.",
    "{name} ({emp_id}) xin phép nghỉ {session} {date} vì {reason}."
]

templates_range = [
    "Tôi là {name} ({emp_id}) xin nghỉ phép {session} từ {start} đến {end} vì {reason}.",
    "{name} mã {emp_id} xin nghỉ {session} từ {start} đến {end} do {reason}.",
    "Xin nghỉ phép từ {start} đến {end} ({session}), tôi là {name} ({emp_id}) vì {reason}."
]

# SAMPLE CREATOR
def create_sample(i):
    name = f"{random.choice(ho)} {random.choice(dem)} {random.choice(ten)}"
    emp_id = f"nv{1000+i}"
    reason = " ".join(random.choice(ly_do_list))

    session_tokens = random.choice(sessions)
    session_text = " ".join(session_tokens)
    session_label = session_map.get(session_text, "full_day")

    use_range = random.random() < 0.5

    if use_range:
        start_obj, end_obj = generate_date_range()
        start_text = format_absolute(start_obj)
        end_text = format_absolute(end_obj)

        template = random.choice(templates_range)
        email_text = template.format(
            name=name,
            emp_id=emp_id,
            session=session_text,
            start=start_text,
            end=end_text,
            reason=reason
        )

        leave_obj = {
            "start_date": start_obj.strftime("%d/%m/%Y"),
            "end_date": end_obj.strftime("%d/%m/%Y"),
            "start_session": session_label,
            "end_session": session_label
        }

    else:
        date_text, normalized_date = generate_date_text()

        template = random.choice(templates_single)
        email_text = template.format(
            name=name,
            emp_id=emp_id,
            session=session_text,
            date=date_text,
            reason=reason
        )

        leave_obj = {
            "start_date": normalized_date,
            "end_date": normalized_date,
            "start_session": session_label,
            "end_session": session_label
        }

    output = {
        "employee_name": name,
        "employee_id": emp_id,
        "leave_periods": [leave_obj]
    }

    return {
        "input_text": f"trích xuất nghỉ phép: {email_text}",
        "target_text": json.dumps(output, ensure_ascii=False)
    }

# GENERATE DATA
data = [create_sample(i) for i in range(5000)]

with open("data/training_data_phot5.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Đã tạo dataset sạch và đa dạng.")
print("Mẫu cuối:", data[-1])