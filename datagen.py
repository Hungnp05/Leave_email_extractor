import random
import json

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

def random_absolute_date():
    d = random.randint(1, 28)
    m = random.randint(1, 12)
    y = random.choice([None, random.randint(2024, 2026)])
    if y:
        return [str(d), "/", str(m), "/", str(y)]
    return [str(d), "/", str(m)]

def random_date():
    if random.random() < 0.6:
        return random_absolute_date()
    return random.choice(relative_dates)

def random_date_range():
    start = random_date()
    end = random_date()
    return start, end

def create_sample(i):
    tokens = []
    # Tạo email text
    name = random.choice(ho) + " " + random.choice(dem) + " " + random.choice(ten)
    id_nv = f"nv{1000+i}"
    email_parts = [f"Tôi là {name} ({id_nv}) xin nghỉ phép"]

    # Session
    if random.random() < 0.7:
        session = " ".join(random.choice(sessions))
        email_parts.append(session)

    # Date
    if random.random() < 0.5:
        start, end = random_date_range()
        email_parts.append(f"từ {start} đến {end}")
    else:
        email_parts.append(" ".join(random_date()))

    # Lý do
    reason = " ".join(random.choice(ly_do_list))
    email_parts.append(f"vì {reason}")

    email_text = " ".join(email_parts)

    # Output JSON
    output = {
        "employee_name": name,
        "employee_id": id_nv,
        "leave_periods": []
    }

    # Thêm leave_periods (đơn giản hóa để dễ train)
    if "từ" in email_text:
        output["leave_periods"].append({
            "start_date": " ".join(start),
            "end_date": " ".join(end),
            "start_session": "full_day",
            "end_session": "full_day"
        })
    else:
        date = " ".join(random_date())
        output["leave_periods"].append({
            "start_date": date,
            "end_date": date,
            "start_session": "full_day",
            "end_session": "full_day"
        })

    return {
        "input_text": f"trích xuất nghỉ phép: {email_text}",
        "target_text": json.dumps(output, ensure_ascii=False)
    }

# Tạo data
data = [create_sample(i) for i in range(3000)]

with open("data/training_data_phot5.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Đã tạo data cho PhoT5 vào data/training_data_phot5.json")
print("Mẫu cuối:", data[-1])