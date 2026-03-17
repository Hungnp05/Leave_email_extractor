import random
import json
from datetime import datetime, timedelta

# DATA POOLS - Tên người
ho = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Vũ", "Đỗ", "Bùi", "Đặng", "Phan", "Dương", "Trịnh", "Đinh", "Lý", "Hồ"]
dem = ["Văn", "Thị", "Minh", "Quang", "Hữu", "Đức", "Gia", "Thanh", "Phú", "Đình", "Ngọc", "Hồng", "Kim"]
ten = ["Anh", "Bình", "Chi", "Dũng", "Hà", "Huy", "Lan", "Phúc", "Tuấn", "Vy", "Hùng", "Hưng", "Bách", "Mai", "Thảo", "Khang"]

# DATAPOOL LÝ DO ĐA DẠNG (làm giàu hơn, thực tế, phân nhóm)
reason_groups = {
    "child": [
        "con tôi bị ốm nặng phải chăm sóc tại nhà",
        "con bị viêm phổi cấp phải nhập viện",
        "con bị sốt xuất huyết cần theo dõi",
        "chăm sóc con bị tai nạn giao thông nhẹ",
        "con bị thủy đậu phải cách ly",
        "con bị quai bị cần điều trị tại nhà",
        "con bị viêm ruột thừa phải phẫu thuật",
        "con bị chấn thương đầu do ngã cần theo dõi"
    ],
    "spouse": [
        "vợ mang thai tháng cuối cần hỗ trợ",
        "chăm sóc vợ bị tai nạn giao thông",
        "vợ bị đau bụng dữ dội phải đi viện",
        "vợ đang hậu sản cần chăm sóc",
        "vợ bị viêm họng nặng cần nghỉ",
        "vợ bị viêm xoang cấp cần theo dõi",
        "chăm sóc vợ bị viêm khớp nặng",
        "vợ bị mất ngủ kéo dài cần hỗ trợ"
    ],
    "elder": [
        "bố bị tai biến cần chăm sóc",
        "mẹ bị đột quỵ phải nhập viện",
        "ông bà bị gãy xương do té ngã",
        "chăm sóc bố mẹ bị huyết áp cao",
        "người thân lớn tuổi bị suy tim",
        "bố mẹ bị suy thận mãn cần theo dõi",
        "chăm sóc ông bà bị Parkinson",
        "người thân bị Alzheimer giai đoạn đầu"
    ],
    "self": [
        "tôi bị tai nạn giao thông nhẹ",
        "tôi bị chấn thương chân cần nghỉ",
        "tôi bị đau lưng cấp phải điều trị",
        "tôi bị viêm họng nặng",
        "tôi bị mất ngủ kéo dài cần nghỉ ngơi",
        "tôi bị đau dạ dày cấp phải nghỉ",
        "tôi bị viêm khớp cần điều trị",
        "tôi bị viêm xoang cấp cần nghỉ"
    ],
    "family": [
        "việc gia đình đám tang",
        "về quê lo hậu sự người thân",
        "gia đình có đám cưới đột xuất",
        "nhà có chuyện đột xuất cần hỗ trợ",
        "gia đình bị lũ lụt cần xử lý",
        "gia đình có đám hỏi con trai",
        "gia đình có đám giỗ lớn",
        "gia đình bị cháy nhà cần sắp xếp"
    ],
    "work": [
        "đi công tác khẩn cấp",
        "công ty cử đi đào tạo đột xuất",
        "chuyển công tác chi nhánh mới",
        "tham gia họp quan trọng ở xa",
        "đi học tập huấn chuyên môn",
        "tham gia kỳ thi quan trọng",
        "đi thi bằng lái xe",
        "tham gia lễ hội gia đình đột xuất"
    ]
}

def get_reason():
    group = random.choice(list(reason_groups.keys()))
    short_reason = random.choice(reason_groups[group])
    
    # Tạo lý do dài từ short_reason, giống email thực tế
    long_templates = {
        "child": f"con tôi bị {short_reason.split(' ')[-2]} {short_reason.split(' ')[-1]}, cần tôi nghỉ để chăm sóc và theo dõi tại nhà/viện.",
        "spouse": f"vợ/chồng tôi bị {short_reason.split(' ')[-2]} {short_reason.split(' ')[-1]}, cần tôi nghỉ để hỗ trợ và chăm sóc.",
        "elder": f"bố/mẹ tôi bị {short_reason.split(' ')[-2]} {short_reason.split(' ')[-1]}, cần tôi nghỉ để chăm sóc và lo viện phí.",
        "self": f"tôi bị {short_reason.split(' ')[-2]} {short_reason.split(' ')[-1]}, bác sĩ khuyên nghỉ ngơi và điều trị.",
        "family": f"nhà có {short_reason.split(' ')[-1]}, cần tôi nghỉ để lo hậu sự và hỗ trợ gia đình.",
        "work": f"tôi phải {short_reason}, không thể sắp xếp người thay thế trong thời gian này."
    }
    long_reason = long_templates[group]

    return long_reason, short_reason

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
BASE_DATE = datetime(2026, 1, 1)

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
    end = start + timedelta(days=random.randint(1, 5))
    return start, end

# TEMPLATE POOLS
templates_single = [
    "Tôi là {name} ({emp_id}) xin nghỉ phép {session} ngày {date} vì {reason}.",
    "Xin chào, tôi {name} mã {emp_id} xin nghỉ {session} {date} do {reason}.",
    "{name} ({emp_id}) xin phép nghỉ {session} {date} vì {reason}."
]

templates_range = [
    "Tôi là {name} ({emp_id}) xin nghỉ phép từ {start_session} {start} đến {end_session} {end} vì {reason}.",
    "{name} mã {emp_id} xin nghỉ từ {start_session} {start} đến {end_session} {end} do {reason}.",
    "Xin nghỉ phép từ {start_session} {start} đến {end_session} {end}, tôi là {name} ({emp_id}) vì {reason}."
]

# SAMPLE CREATOR
def create_sample(i):
    name = f"{random.choice(ho)} {random.choice(dem)} {random.choice(ten)}"
    emp_id = f"nv{1000 + i:04d}"

    # Lấy lý do đa dạng
    long_reason, short_reason = get_reason()

    use_range = random.random() < 0.5

    if use_range:
        start_session_tokens = random.choice(sessions)
        end_session_tokens = random.choice(sessions)
        start_session_text = " ".join(start_session_tokens)
        end_session_text = " ".join(end_session_tokens)
        start_session_label = session_map.get(start_session_text, "full_day")
        end_session_label = session_map.get(end_session_text, "full_day")

        start_obj, end_obj = generate_date_range()
        start_text = format_absolute(start_obj)
        end_text = format_absolute(end_obj)

        template = random.choice(templates_range)
        email_text = template.format(
            name=name,
            emp_id=emp_id,
            start_session=start_session_text,
            start=start_text,
            end_session=end_session_text,
            end=end_text,
            reason=long_reason
        )

        leave_obj = {
            "start_date": start_obj.strftime("%d/%m/%Y"),
            "end_date": end_obj.strftime("%d/%m/%Y"),
            "start_session": start_session_label,
            "end_session": end_session_label,
            "reason": short_reason  # Lý do ngắn gọn
        }

    else:
        session_tokens = random.choice(sessions)
        session_text = " ".join(session_tokens)
        session_label = session_map.get(session_text, "full_day")

        date_text, normalized_date = generate_date_text()

        template = random.choice(templates_single)
        email_text = template.format(
            name=name,
            emp_id=emp_id,
            session=session_text,
            date=date_text,
            reason=long_reason
        )

        leave_obj = {
            "start_date": normalized_date,
            "end_date": normalized_date,
            "start_session": session_label,
            "end_session": session_label,
            "reason": short_reason  # Lý do ngắn gọn
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
if __name__ == "__main__":
    random.seed(42)
    data = [create_sample(i) for i in range(3000)]

    with open("data/test.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Đã tạo dataset mới với lý do đa dạng và có field reason")
    print("Mẫu cuối cùng:")
    print(json.dumps(data[-1], ensure_ascii=False, indent=2))