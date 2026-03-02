from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import re

class ReasonSummarizer:
    def __init__(self, model_name="vinai/bartpho-syllable"):
        print(f"[ReasonSummarizer] Loading {model_name}...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device.upper()}")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()
        print("[ReasonSummarizer] Loaded successfully")

    def summarize(self, reason_text: str, max_length=50) -> str:
        if not reason_text or not reason_text.strip():
            return "Không có lý do"

        prompt = f"tóm tắt lý do xin nghỉ bằng tiếng Việt trong 1 câu ngắn gọn (10–20 từ), giữ nguyên ý chính như ốm nặng, nhập viện, chăm sóc con, không thêm chữ thừa: {reason_text}"

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            max_length=256,
            truncation=True
        ).to(self.device)

        outputs = self.model.generate(
            **inputs,
            max_length=50,
            min_length=15,
            num_beams=6,
            early_stopping=True,
            no_repeat_ngram_size=4,
            temperature=0.7,
            repetition_penalty=1.2
        )

        summary = self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        summary = re.sub(r'^(tóm tắt.*?:|Tóm tắt:|Lý do:)\s*', '', summary, flags=re.IGNORECASE).strip()
        summary = summary.strip('"').strip("'").strip('[]{}').strip()
        summary = re.sub(r'\s*\.+$', '', summary).strip()

        if len(summary.split()) < 5:
            words = reason_text.split()
            short_fallback = ' '.join(words[:10]) if words else "Lý do không rõ ràng"
            summary = short_fallback

        return summary if summary else "Lý do không rõ ràng"