import random
import json
import re

# Danh sách bệnh theo đối tượng
child_diseases = [
    "ốm nặng", "viêm phổi cấp", "sốt xuất huyết", "sốt cao liên tục", "nhiễm khuẩn đường hô hấp",
    "tiêu chảy cấp", "thủy đậu", "quai bị", "viêm não", "gãy tay do ngã", "cúm nặng", "viêm màng não",
    "viêm ruột thừa", "chấn thương đầu do ngã"
]

adult_diseases = [
    "tai nạn giao thông nhẹ", "chấn thương chân", "bỏng tay", "đau lưng cấp", "viêm họng nặng",
    "đau dạ dày cấp", "viêm khớp", "mất ngủ kéo dài", "huyết áp cao đột ngột", "đau đầu migraine",
    "viêm xoang cấp", "thoát vị đĩa đệm", "đau thần kinh tọa", "viêm gan cấp", "viêm tụy"
]

elder_diseases = [
    "tai biến mạch máu não", "đột quỵ", "huyết áp cao", "đái tháo đường biến chứng", "gãy xương đùi do té ngã",
    "viêm khớp nặng", "suy tim", "thoái hóa cột sống", "Parkinson", "Alzheimer giai đoạn đầu",
    "viêm phổi do tuổi cao", "suy thận mãn", "loãng xương", "đục thủy tinh thể"
]

# Các template lý do dài
reason_templates = [
    # Con cái
    {"type": "child", "long": "con tôi bị {disease}, sốt cao liên tục từ tối hôm qua và bác sĩ yêu cầu nhập viện theo dõi thêm vài ngày, nên tôi cần trực tiếp đưa cháu vào bệnh viện và chăm sóc trong thời gian điều trị. Gia đình hiện không có người thay thế nên tôi buộc phải xin nghỉ để xử lý việc này.", "short_base": "con bị {disease}"},
    {"type": "child", "long": "con trai/con gái tôi bị {disease}, phải nhập viện theo dõi và truyền dịch, cần tôi ở bên chăm sóc liên tục vì cháu còn nhỏ và rất sợ.", "short_base": "chăm sóc con bị {disease}"},
    {"type": "child", "long": "con tôi bị {disease}, bệnh diễn biến phức tạp hơn dự kiến, tôi cần nghỉ để đưa cháu đi khám chuyên khoa và theo dõi hàng ngày.", "short_base": "con bị {disease} cần theo dõi"},
    {"type": "child", "long": "cháu nội/ngoại tôi bị {disease}, bố mẹ cháu đi công tác xa, tôi phải nghỉ để chăm sóc và đưa đi viện.", "short_base": "chăm sóc cháu bị {disease}"},
    {"type": "child", "long": "con tôi bị {disease}, cần tôi nghỉ để đưa đi khám bác sĩ nhi khoa và theo dõi tại nhà.", "short_base": "con bị {disease} cần khám"},
    {"type": "child", "long": "con tôi bị {disease}, phải nghỉ học và ở nhà điều trị, tôi cần nghỉ để chăm sóc và học online cho cháu.", "short_base": "chăm sóc con bị {disease} ở nhà"},
    {"type": "child", "long": "con tôi bị {disease}, bác sĩ yêu cầu cách ly tại nhà, tôi phải nghỉ để theo dõi và chăm sóc.", "short_base": "con bị {disease} cách ly"},
    {"type": "child", "long": "con tôi bị {disease}, cần phẫu thuật nhỏ, tôi phải nghỉ để đưa đi viện và chăm sóc hậu phẫu.", "short_base": "con bị {disease} cần phẫu thuật"},

    # Vợ/chồng
    {"type": "adult", "long": "vợ/chồng tôi đang mang thai tháng {month}, có dấu hiệu {symptom}, cần tôi ở nhà hỗ trợ và đưa đi viện khẩn cấp nếu cần.", "short_base": "vợ/chồng mang thai tháng cuối cần hỗ trợ"},
    {"type": "adult", "long": "vợ/chồng tôi bị {disease}, đang nằm viện điều trị, tôi cần thay phiên chăm sóc vì không có người thân khác hỗ trợ.", "short_base": "chăm sóc vợ/chồng bị {disease}"},
    {"type": "adult", "long": "vợ/chồng tôi phải phẫu thuật {disease}, cần tôi nghỉ để chăm sóc hậu phẫu và hỗ trợ sinh hoạt.", "short_base": "chăm sóc vợ/chồng phẫu thuật"},
    {"type": "adult", "long": "vợ/chồng tôi bị tai nạn {accident}, chấn thương {body_part}, tôi cần nghỉ để chăm sóc và đưa đi tái khám.", "short_base": "chăm sóc vợ/chồng bị tai nạn"},
    {"type": "adult", "long": "vợ/chồng tôi bị {disease}, cần tôi nghỉ để đưa đi khám chuyên khoa và theo dõi điều trị.", "short_base": "chăm sóc vợ/chồng bị {disease}"},
    {"type": "adult", "long": "vợ/chồng tôi đang trong giai đoạn hậu sản, cần tôi nghỉ để hỗ trợ chăm sóc con và việc nhà.", "short_base": "hỗ trợ vợ/chồng hậu sản"},
    {"type": "adult", "long": "vợ/chồng tôi bị {disease}, sức khỏe yếu, tôi cần nghỉ để chăm sóc và lo thuốc thang.", "short_base": "chăm sóc vợ/chồng bị {disease}"},
    {"type": "adult", "long": "vợ/chồng tôi bị {disease}, cần tôi nghỉ để đưa đi viện khám định kỳ và theo dõi.", "short_base": "vợ/chồng bị {disease} cần theo dõi"},

    # Bố mẹ / người thân lớn tuổi
    {"type": "elder", "long": "bố/mẹ tôi bị {disease} đột ngột, đang nằm viện cấp cứu, tôi cần về quê chăm sóc và hỗ trợ gia đình trong vài ngày.", "short_base": "bố/mẹ bị {disease} cần chăm sóc"},
    {"type": "elder", "long": "ông/bà tôi bị {disease}, tuổi cao sức yếu, cần tôi về quê chăm sóc và lo thuốc men trong thời gian này.", "short_base": "chăm sóc ông/bà bị {disease}"},
    {"type": "elder", "long": "bố/mẹ vợ/chồng bị {disease}, cần tôi nghỉ để thay phiên chăm sóc vì con cái bận công việc.", "short_base": "chăm sóc bố/mẹ vợ/chồng bị {disease}"},
    {"type": "elder", "long": "người thân lớn tuổi bị {disease}, không có ai chăm sóc, tôi phải nghỉ để lo viện phí và thuốc thang.", "short_base": "chăm sóc người thân bị {disease}"},
    {"type": "elder", "long": "bố/mẹ tôi bị {disease}, cần tôi nghỉ để đưa đi viện khám chuyên khoa và theo dõi.", "short_base": "bố/mẹ bị {disease} cần khám"},
    {"type": "elder", "long": "ông bà tôi bị {disease}, cần tôi nghỉ để hỗ trợ sinh hoạt và lo thuốc men hàng ngày.", "short_base": "hỗ trợ ông bà bị {disease}"},
    {"type": "elder", "long": "bố/mẹ tôi bị {disease}, cần tôi nghỉ để chăm sóc tại nhà và theo dõi sức khỏe.", "short_base": "chăm sóc bố/mẹ bị {disease} tại nhà"},
    {"type": "elder", "long": "người thân bị {disease}, tuổi cao, tôi cần nghỉ để lo hậu sự và chăm sóc.", "short_base": "chăm sóc người thân bị {disease}"},

    # Bản thân
    {"type": "self", "long": "tôi bị {disease} nhẹ, chấn thương {body_part}, phải nghỉ ngơi và điều trị tại nhà theo chỉ định của bác sĩ.", "short_base": "tôi bị {disease}"},
    {"type": "self", "long": "tôi bị {disease}, bác sĩ khuyên phải nghỉ ngơi tuyệt đối ít nhất 3 ngày để tránh biến chứng.", "short_base": "tôi bị {disease} cần nghỉ ngơi"},
    {"type": "self", "long": "tôi bị {disease}, sức khỏe yếu, cần nghỉ để điều trị và phục hồi hoàn toàn.", "short_base": "tôi bị {disease} cần điều trị"},
    {"type": "self", "long": "tôi bị {disease}, ảnh hưởng nghiêm trọng đến công việc, bác sĩ yêu cầu nghỉ phép để theo dõi.", "short_base": "tôi bị {disease} cần theo dõi"},
    {"type": "self", "long": "tôi bị {disease}, cần nghỉ để đi khám chuyên khoa và điều trị theo phác đồ.", "short_base": "tôi bị {disease} cần khám"},
    {"type": "self", "long": "tôi bị {disease}, cần nghỉ để cách ly và theo dõi sức khỏe tại nhà.", "short_base": "tôi bị {disease} cần cách ly"},

    # Việc gia đình
    {"type": "family", "long": "nhà có việc đột xuất: {family_event}, tôi cần về quê lo hậu sự và hỗ trợ gia đình trong {days} ngày.", "short_base": "việc gia đình {family_event}"},
    {"type": "family", "long": "gia đình tôi có {family_event} đột xuất, cần tôi về quê hỗ trợ lo lắng và sắp xếp mọi việc.", "short_base": "gia đình có việc đột xuất"},
    {"type": "family", "long": "nhà tôi bị {family_event} (thiên tai, cháy nhà...), cần tôi nghỉ để xử lý và sắp xếp chỗ ở tạm thời.", "short_base": "gia đình gặp {family_event}"},
    {"type": "family", "long": "con tôi sắp kết hôn/đám cưới, cần tôi nghỉ để lo chuẩn bị và đón khách.", "short_base": "con sắp đám cưới cần lo"},
    {"type": "family", "long": "gia đình tôi có đám hỏi/đám cưới đột xuất, cần tôi nghỉ để hỗ trợ chuẩn bị và tổ chức.", "short_base": "gia đình có đám hỏi/cưới"},
    {"type": "family", "long": "gia đình tôi có đám giỗ lớn, cần tôi nghỉ để về quê lo lễ và hỗ trợ người thân.", "short_base": "gia đình có đám giỗ lớn"},

    # Công tác / Việc đột xuất
    {"type": "work", "long": "tôi phải đi {travel_reason} đột xuất vì {reason}, không thể sắp xếp người thay thế trong thời gian này.", "short_base": "đi {travel_reason} đột xuất"},
    {"type": "work", "long": "công ty cử tôi đi công tác khẩn cấp {days} ngày, tôi cần xin nghỉ phép để hoàn thành nhiệm vụ.", "short_base": "đi công tác khẩn cấp"},
    {"type": "work", "long": "tôi phải tham gia kỳ thi quan trọng/đào tạo bắt buộc {days} ngày, cần xin nghỉ phép để tập trung.", "short_base": "tham gia thi/đào tạo"},
    {"type": "work", "long": "tôi bị chuyển công tác đột xuất đến chi nhánh mới, cần nghỉ để sắp xếp chuyển nhà và gia đình.", "short_base": "chuyển công tác đột xuất"},
    {"type": "work", "long": "công ty yêu cầu tôi đi học tập huấn chuyên môn {days} ngày ở xa, tôi cần xin nghỉ phép.", "short_base": "đi học tập huấn chuyên môn"},
    {"type": "work", "long": "tôi phải tham gia hội nghị/doanh nghiệp {days} ngày, cần xin nghỉ phép để tham dự.", "short_base": "tham gia hội nghị/doanh nghiệp"},
]

symptoms = ["chuyển dạ sớm", "đau bụng dữ dội", "xuất huyết nhẹ", "co thắt tử cung"]
body_parts = ["chân phải", "tay trái", "lưng", "đầu gối", "cổ tay"]
family_events = ["đám tang người thân", "đám giỗ cụ", "chuyện gia đình đột xuất", "đám cưới con gái", "chuyển nhà khẩn cấp", "thiên tai lũ lụt", "cháy nhà", "đám hỏi con trai"]
travel_reasons = ["công tác khẩn cấp", "về quê có việc", "đưa người thân đi viện xa", "họp chi nhánh đột xuất", "đào tạo chuyên môn", "thi bằng lái xe", "tham gia lễ hội gia đình"]
reasons = ["gia đình không ai thay thế", "bệnh diễn biến phức tạp", "cần chăm sóc trực tiếp", "công việc đột xuất", "thi cử quan trọng", "chuyển nhà đột xuất"]

def generate_sample():
    template = random.choice(reason_templates)
    long_reason = template["long"]
    short_base = template["short_base"]

    format_kwargs = {}

    if template["type"] == "child":
        disease = random.choice(child_diseases)
        format_kwargs["disease"] = disease
        short_summary = short_base.format(disease=disease)

    elif template["type"] == "elder":
        disease = random.choice(elder_diseases)
        format_kwargs["disease"] = disease
        short_summary = short_base.format(disease=disease)

    elif template["type"] == "self":
        disease = random.choice(adult_diseases)
        body_part = random.choice(body_parts)
        format_kwargs["disease"] = disease
        format_kwargs["body_part"] = body_part
        short_summary = short_base.format(disease=disease)

    elif template["type"] == "adult":
        month = random.randint(7, 9)
        symptom = random.choice(symptoms)
        format_kwargs["month"] = month
        format_kwargs["symptom"] = symptom
        short_summary = short_base

    elif template["type"] == "family":
        event = random.choice(family_events)
        days = random.randint(3, 5)
        format_kwargs["family_event"] = event
        format_kwargs["days"] = days
        short_summary = short_base.format(family_event=event)

    elif template["type"] == "work":
        travel = random.choice(travel_reasons)
        reason = random.choice(reasons)
        days = random.randint(3, 5)
        format_kwargs["travel_reason"] = travel
        format_kwargs["reason"] = reason
        format_kwargs["days"] = days
        short_summary = short_base.format(travel_reason=travel)

    existing_placeholders = re.findall(r'\{(\w+)\}', long_reason)
    filtered_kwargs = {k: v for k, v in format_kwargs.items() if k in existing_placeholders}

    if filtered_kwargs:
        long_reason = long_reason.format(**filtered_kwargs)

    # Đảm bảo tóm tắt ngắn 5–10 từ
    words = short_summary.split()
    if len(words) > 10:
        short_summary = " ".join(words[:10])
    elif len(words) < 5:
        short_summary += " cần nghỉ"

    return {
        "input_text": f"tóm tắt lý do xin nghỉ bằng tiếng Việt chỉ 5–10 từ: {long_reason}",
        "target_text": short_summary
    }

data = [generate_sample() for _ in range(5000)]

with open("data/summary_training_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Đã tạo {len(data)} mẫu dữ liệu tóm tắt lý do xin nghỉ phép (đa dạng và logic).")
print("Mẫu cuối:", data[-1])