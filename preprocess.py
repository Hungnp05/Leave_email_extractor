# preprocess.py - làm sạch text trước khi đưa vào PhoT5
import re
import unicodedata

def clean_text(text: str) -> str:
    """
    Làm sạch văn bản email trước khi đưa vào PhoT5:
    - Chuẩn hóa Unicode
    - Loại ký tự thừa
    - Giảm khoảng trắng
    - Lowercase (PhoT5 hoạt động tốt với lowercase tiếng Việt)
    """
    if text is None or not isinstance(text, str):
        print("[clean_text] Input invalid or None → return empty string")
        return ""

    print(f"[clean_text] Original length: {len(text)} chars")

    try:
        # Chuẩn hóa Unicode
        text = unicodedata.normalize('NFKC', text)

        # Loại bỏ ký tự đặc biệt thừa, giữ chữ cái, số, dấu câu cơ bản
        text = re.sub(r'[^\w\s.,!?]', '', text)

        # Thay nhiều khoảng trắng bằng một
        text = re.sub(r'\s+', ' ', text)

        # Loại bỏ khoảng trắng đầu cuối
        text = text.strip()

        # Lowercase để đồng nhất
        text = text.lower()

        print(f"[clean_text] Cleaned length: {len(text)} chars")
        return text

    except Exception as e:
        print(f"[clean_text] ERROR: {str(e)}")
        return text.strip().lower()  # fallback về input gốc đã lower