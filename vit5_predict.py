from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import json
import torch
import re

class LeaveExtractor:
    def __init__(self, model_path="models/vit5_finetuned_gpu"):
        print(f"[LeaveExtractor] Loading model from {model_path}...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device.upper()}")

        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
        self.model.to(self.device)
        self.model.eval()
        print("[LeaveExtractor] Model loaded successfully")

    def predict(self, text: str) -> dict:
        print(f"[predict] Input text: {text[:100]}...")
        try:
            input_text = f"trích xuất nghỉ phép: {text}"
            inputs = self.tokenizer(
                input_text,
                return_tensors="pt",
                max_length=256,
                truncation=True
            ).to(self.device)

            outputs = self.model.generate(
                **inputs,
                max_length=128,
                num_beams=8,
                early_stopping=True,
                do_sample=False,
                temperature=0.7
            )

            result = self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

            # Clean output
            result = re.sub(r'^.*?\{', '{', result, flags=re.DOTALL).strip()
            result = re.sub(r'\}.*?$', '}', result, flags=re.DOTALL).strip()

            # Sửa JSON syntax
            result = re.sub(r'([a-z_]+)\s*:', r'"\1":', result)
            result = re.sub(r':\s*([^"{}\[\],]+?)(?=\s*[,}\]])', r': "\1"', result)
            result = re.sub(r'leave_periods":\s*\[([^]]+)\]', r'leave_periods": [{\1}]', result)
            result = re.sub(r',\s*([}\]])', r'\1', result)

            print("[predict] Raw decoded after syntax fix:", result)

            try:
                parsed = json.loads(result)
            except json.JSONDecodeError:
                print("[predict] JSON parse failed, trying fallback")
                return {"error": "Invalid JSON format", "raw_output": result}

            # Post-process nâng cao
            # 1. Tách mã nhân viên (tìm "nv" + số, loại bỏ khoảng trắng)
            if "employee_id" in parsed:
                eid = parsed["employee_id"]
                match = re.search(r'nv\s*(\d+)', eid, re.IGNORECASE)
                if match:
                    parsed["employee_id"] = f"nv{match.group(1)}"

            # 2. Chuẩn hóa start_date và end_date về dd/mm (xử lý "232" → "23/2")
            for period in parsed.get("leave_periods", []):
                for key in ["start_date", "end_date"]:
                    val = period.get(key, "")
                    if val and isinstance(val, str):
                        numbers = re.findall(r'\d+', val)
                        if len(numbers) >= 2:
                            day, month = numbers[0], numbers[1]
                            if int(day) > 31 or int(day) > int(month):
                                day, month = month, day
                            period[key] = f"{day.zfill(2)}/{month.zfill(2)}"
                        else:
                            period[key] = val.strip()

                start = period.get("start_date", "")
                end = period.get("end_date", "")
                if start and end and start > end:
                    period["start_date"], period["end_date"] = end, start

            print("[predict] Final parsed & normalized:", parsed)
            return parsed

        except Exception as e:
            print(f"[predict] ERROR: {str(e)}")
            return {"error": str(e)}