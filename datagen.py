import random
import json
from datetime import datetime, timedelta

# DATA POOLS
ho = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Vũ", "Đỗ", "Bùi", "Đặng", "Phan", "Dương", "Trịnh", "Đinh", "Lý", "Hồ"]
dem = ["Văn", "Thị", "Minh", "Quang", "Hữu", "Đức", "Gia", "Thanh", "Phú", "Đình", "Ngọc", "Hồng", "Kim"]
ten = ["Anh", "Bình", "Chi", "Dũng", "Hà", "Huy", "Lan", "Phúc", "Tuấn", "Vy", "Hùng", "Hưng", "Bách", "Mai", "Thảo", "Khang"]

reason_groups = {
    "child": [
        {"short": "con bị ốm nặng phải chăm sóc", "long_suffix": "con tôi bị ốm nặng, sốt cao liên tục từ tối hôm qua và bác sĩ yêu cầu nhập viện theo dõi thêm vài ngày, nên tôi cần trực tiếp đưa cháu vào bệnh viện và chăm sóc trong thời gian điều trị. Gia đình hiện không có người thay thế nên tôi buộc phải xin nghỉ để xử lý việc này."},
        {"short": "con bị viêm phổi cấp phải nhập viện", "long_suffix": "con trai/con gái tôi bị viêm phổi cấp, phải nhập viện theo dõi và truyền dịch, cần tôi ở bên chăm sóc liên tục vì cháu còn nhỏ và rất sợ."},
        {"short": "con bị sốt xuất huyết cần theo dõi", "long_suffix": "con tôi bị sốt xuất huyết, bệnh diễn biến phức tạp hơn dự kiến, tôi cần nghỉ để đưa cháu đi khám chuyên khoa và theo dõi hàng ngày."},
        {"short": "chăm sóc con bị tai nạn nhẹ", "long_suffix": "cháu nội/ngoại tôi bị tai nạn nhẹ, bố mẹ cháu đi công tác xa, tôi phải nghỉ để chăm sóc và đưa đi viện."},
        {"short": "con bị thủy đậu phải cách ly", "long_suffix": "con tôi bị thủy đậu, cần tôi nghỉ để đưa đi khám bác sĩ nhi khoa và theo dõi tại nhà."},
        {"short": "con bị quai bị cần điều trị", "long_suffix": "con tôi bị quai bị, phải nghỉ học và ở nhà điều trị, tôi cần nghỉ để chăm sóc và học online cho cháu."},
        {"short": "con bị viêm ruột thừa cần phẫu thuật", "long_suffix": "con tôi bị viêm ruột thừa, bác sĩ yêu cầu phẫu thuật nhỏ, tôi phải nghỉ để đưa đi viện và chăm sóc hậu phẫu."},
        {"short": "con bị chấn thương đầu do ngã", "long_suffix": "con tôi bị chấn thương đầu do ngã, cần tôi nghỉ để theo dõi và chăm sóc liên tục."}
    ],
    "spouse": [
        {"short": "vợ mang thai tháng cuối cần hỗ trợ", "long_suffix": "vợ tôi đang mang thai tháng cuối, có dấu hiệu chuyển dạ sớm, cần tôi ở nhà hỗ trợ và đưa đi viện khẩn cấp nếu cần."},
        {"short": "chăm sóc vợ bị tai nạn giao thông", "long_suffix": "vợ tôi bị tai nạn giao thông, chấn thương chân phải, tôi cần nghỉ để chăm sóc và đưa đi tái khám."},
        {"short": "vợ bị đau bụng dữ dội phải đi viện", "long_suffix": "vợ tôi bị đau bụng dữ dội, đang nằm viện điều trị, tôi cần thay phiên chăm sóc vì không có người thân khác hỗ trợ."},
        {"short": "vợ đang hậu sản cần chăm sóc", "long_suffix": "vợ tôi đang trong giai đoạn hậu sản, cần tôi nghỉ để hỗ trợ chăm sóc con và việc nhà."},
        {"short": "vợ bị viêm họng nặng cần nghỉ", "long_suffix": "vợ tôi bị viêm họng nặng, sức khỏe yếu, tôi cần nghỉ để chăm sóc và lo thuốc thang."},
        {"short": "vợ bị viêm xoang cấp cần theo dõi", "long_suffix": "vợ tôi bị viêm xoang cấp, cần tôi nghỉ để đưa đi viện khám định kỳ và theo dõi."},
        {"short": "chăm sóc vợ bị viêm khớp nặng", "long_suffix": "vợ tôi bị viêm khớp nặng, phải phẫu thuật, cần tôi nghỉ để chăm sóc hậu phẫu và hỗ trợ sinh hoạt."},
        {"short": "vợ bị mất ngủ kéo dài cần hỗ trợ", "long_suffix": "vợ tôi bị mất ngủ kéo dài, cần tôi nghỉ để chăm sóc và theo dõi sức khỏe."}
    ],
    "elder": [
        {"short": "bố bị tai biến cần chăm sóc", "long_suffix": "bố tôi bị tai biến mạch máu não đột ngột, đang nằm viện cấp cứu, tôi cần về quê chăm sóc và hỗ trợ gia đình trong vài ngày."},
        {"short": "mẹ bị đột quỵ phải nhập viện", "long_suffix": "mẹ tôi bị đột quỵ, cần tôi nghỉ để đưa đi viện khám chuyên khoa và theo dõi."},
        {"short": "ông bà bị gãy xương do té ngã", "long_suffix": "ông/bà tôi bị gãy xương do té ngã, tuổi cao sức yếu, cần tôi về quê chăm sóc và lo thuốc men trong thời gian này."},
        {"short": "chăm sóc bố mẹ bị huyết áp cao", "long_suffix": "bố mẹ vợ/chồng bị huyết áp cao, cần tôi nghỉ để thay phiên chăm sóc vì con cái bận công việc."},
        {"short": "người thân lớn tuổi bị suy tim", "long_suffix": "người thân lớn tuổi bị suy tim, không có ai chăm sóc, tôi phải nghỉ để lo viện phí và thuốc thang."},
        {"short": "bố mẹ bị suy thận mãn cần theo dõi", "long_suffix": "bố mẹ tôi bị suy thận mãn, cần tôi nghỉ để chăm sóc tại nhà và theo dõi sức khỏe."},
        {"short": "chăm sóc ông bà bị Parkinson", "long_suffix": "ông bà tôi bị Parkinson, cần tôi nghỉ để hỗ trợ sinh hoạt và lo thuốc men hàng ngày."},
        {"short": "người thân bị Alzheimer giai đoạn đầu", "long_suffix": "người thân bị Alzheimer giai đoạn đầu, cần tôi nghỉ để lo hậu sự và chăm sóc."}
    ],
    "self": [
        {"short": "tôi bị tai nạn giao thông nhẹ", "long_suffix": ", chấn thương chân phải, phải nghỉ ngơi và điều trị tại nhà theo chỉ định của bác sĩ."},
        {"short": "tôi bị chấn thương chân cần nghỉ", "long_suffix": ", bác sĩ khuyên phải nghỉ ngơi tuyệt đối ít nhất 3 ngày để tránh biến chứng."},
        {"short": "tôi bị đau lưng cấp phải điều trị", "long_suffix": ", sức khỏe yếu, cần nghỉ để điều trị và phục hồi hoàn toàn."},
        {"short": "tôi bị viêm họng nặng", "long_suffix": ", ảnh hưởng nghiêm trọng đến công việc, bác sĩ yêu cầu nghỉ phép để theo dõi."},
        {"short": "tôi bị mất ngủ kéo dài cần nghỉ ngơi", "long_suffix": ", cần nghỉ để đi khám chuyên khoa và điều trị theo phác đồ."},
        {"short": "tôi bị viêm xoang cấp cần nghỉ", "long_suffix": ", cần nghỉ để cách ly và theo dõi sức khỏe tại nhà."}
    ],
    "family": [
        {"short": "việc gia đình đám tang", "long_suffix": ", tôi cần về quê lo hậu sự và hỗ trợ gia đình trong vài ngày."},
        {"short": "về quê lo hậu sự người thân", "long_suffix": ", cần tôi nghỉ để hỗ trợ lo lắng và sắp xếp mọi việc."},
        {"short": "gia đình có đám cưới đột xuất", "long_suffix": ", cần tôi nghỉ để lo chuẩn bị và đón khách."},
        {"short": "nhà có chuyện đột xuất cần hỗ trợ", "long_suffix": ", cần tôi nghỉ để xử lý và sắp xếp chỗ ở tạm thời."},
        {"short": "gia đình bị lũ lụt cần xử lý", "long_suffix": ", cần tôi nghỉ để xử lý và sắp xếp chỗ ở tạm thời."},
        {"short": "gia đình có đám hỏi con trai", "long_suffix": ", cần tôi nghỉ để hỗ trợ chuẩn bị và tổ chức."},
        {"short": "gia đình có đám giỗ lớn", "long_suffix": ", cần tôi nghỉ để về quê lo lễ và hỗ trợ người thân."}
    ],
    "work": [
        {"short": "đi công tác khẩn cấp", "long_suffix": " đột xuất vì công việc, không thể sắp xếp người thay thế trong thời gian này."},
        {"short": "công ty cử đi đào tạo đột xuất", "long_suffix": " {days} ngày, tôi cần xin nghỉ phép để hoàn thành nhiệm vụ."},
        {"short": "chuyển công tác chi nhánh mới", "long_suffix": ", cần nghỉ để sắp xếp chuyển nhà và gia đình."},
        {"short": "tham gia họp quan trọng ở xa", "long_suffix": ", cần xin nghỉ phép để tham dự."},
        {"short": "đi học tập huấn chuyên môn", "long_suffix": " ở xa, tôi cần xin nghỉ phép."},
        {"short": "tham gia kỳ thi quan trọng", "long_suffix": " {days} ngày, cần xin nghỉ phép để tập trung."},
        {"short": "đi thi bằng lái xe", "long_suffix": ", cần xin nghỉ phép để tham gia kỳ thi."},
        {"short": "tham gia lễ hội gia đình đột xuất", "long_suffix": ", cần nghỉ để hỗ trợ gia đình."}
    ]
}

def get_reason():
    group = random.choice(list(reason_groups.keys()))
    pair = random.choice(reason_groups[group])
    short_reason = pair["short"]
    long_suffix = pair["long_suffix"]
    if "{days}" in long_suffix:
        long_suffix = long_suffix.format(days=random.randint(3, 5))
    long_reason = long_suffix
    return long_reason, short_reason

# SESSIONS
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
            "reason": short_reason
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
            "reason": short_reason
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
    data = [create_sample(i) for i in range(6000)]

    with open("data/training_data_phot5.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Đã tạo dataset mới với lý do đa dạng và đồng bộ")
    print("Mẫu cuối cùng:")
    print(json.dumps(data[-1], ensure_ascii=False, indent=2))