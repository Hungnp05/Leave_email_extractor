import re
import unicodedata

def clean_text(text: str) -> str:
    """
    Làm sạch văn bản email trước khi đưa vào PhoT5:
    - Chuẩn hóa Unicode
    - Giữ lại ký tự ngày tháng như / và -
    - Loại ký tự đặc biệt không cần thiết
    - Giảm khoảng trắng
    - Lowercase
    """

    if text is None or not isinstance(text, str):
        print("[clean_text] Input invalid or None → return empty string")
        return ""

    print(f"[clean_text] Original length: {len(text)} chars")

    try:
        text = unicodedata.normalize('NFKC', text)

        text = re.sub(r'[^\w\s.,!?/\-:]', '', text)

        text = re.sub(r'\s+', ' ', text)

        text = text.strip()

        text = text.lower()

        print(f"[clean_text] Cleaned length: {len(text)} chars")
        return text

    except Exception as e:
        print(f"[clean_text] ERROR: {str(e)}")
        return text.strip().lower()