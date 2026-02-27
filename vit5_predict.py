from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import json
import torch

class LeaveExtractor:
    def __init__(self, model_path="models/vit5_finetuned_gpu"):
        print(f"[LeaveExtractor] Loading model from {model_path}...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[LeaveExtractor] Using device: {self.device.upper()}")

        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
        self.model.to(self.device)
        self.model.eval()  # Chế độ inference
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

            # Generate output
            outputs = self.model.generate(
                **inputs,
                max_length=128,
                num_beams=4,
                early_stopping=True,
                do_sample=False,
                temperature=0.7
            )

            result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Parse JSON
            try:
                parsed = json.loads(result)
                print("[predict] Parsed JSON success")
                return parsed
            except json.JSONDecodeError:
                print("[predict] JSON parse failed, returning raw")
                return {"error": "Invalid JSON format", "raw_output": result}

        except Exception as e:
            print(f"[predict] ERROR: {str(e)}")
            return {"error": str(e)}

# Test nhanh
if __name__ == "__main__":
    extractor = LeaveExtractor()
    test_text = "Tôi là Nguyễn Văn Hùng mã nhân viên NV001 xin nghỉ phép từ sáng ngày 23/2 đến chiều ngày 25/2"
    result = extractor.predict(test_text)
    print("Result:", json.dumps(result, ensure_ascii=False, indent=2))