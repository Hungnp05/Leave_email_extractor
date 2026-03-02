from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from vit5_predict import LeaveExtractor
from reason_summarizer import ReasonSummarizer
from preprocess import clean_text
import uvicorn
import re

app = FastAPI(
    title="Leave Extractor - ViT5 GPU",
    description="Trích xuất thông tin nghỉ phép và tóm tắt lý do từ email tiếng Việt",
    version="1.0"
)

templates = Jinja2Templates(directory="templates")

# Load model
extractor = LeaveExtractor(model_path="models/vit5_finetuned_gpu")
reason_summarizer = ReasonSummarizer()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": None, "summarized_reasons": None}
    )

@app.post("/", response_class=HTMLResponse)
async def extract_from_form(request: Request, email_text: str = Form(...)):
    if not email_text.strip():
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "result": {"error": "Vui lòng nhập nội dung email"}, "summarized_reasons": None}
        )

    try:
        cleaned = clean_text(email_text)
        print(f"[API] Cleaned input: {cleaned[:100]}...")

        # 1. Trích xuất JSON bằng ViT5
        result = extractor.predict(cleaned)
        print(f"[API] ViT5 raw result: {result}")

        # 2. Tóm tắt lý do
        summarized_reasons = []
        reason_from_email = ""

        reason_keywords = ["vì", "do", "lý do", "nguyên nhân", "lý do xin nghỉ"]
        for kw in reason_keywords:
            if kw in cleaned:
                reason_part = cleaned.split(kw, 1)[-1].strip()
                stop_keywords = [
                    "trong thời gian nghỉ", "nếu có vấn đề", "kính mong", "trân trọng", 
                    "xin chân thành cảm ơn", "bàn giao", "đã bàn giao", "hỗ trợ từ xa",
                    "sau khi quay trở lại", "rất mong nhận được", "vậy tôi"
                ]
                for stop in stop_keywords:
                    if stop in reason_part:
                        reason_part = reason_part.split(stop)[0].strip()
                        break
                reason_from_email = reason_part
                break

        if reason_from_email:
            summary = reason_summarizer.summarize(reason_from_email)
            summarized_reasons.append(summary)
            print(f"[API] Extracted reason part: {reason_from_email[:100]}...")
            print(f"[API] Summarized reason: {summary}")


        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": result,
                "summarized_reasons": summarized_reasons
            }
        )

    except Exception as e:
        error_msg = f"Lỗi xử lý: {str(e)}"
        print("[API ERROR]", error_msg)
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "result": {"error": error_msg}, "summarized_reasons": None}
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "vit5_device": extractor.device}

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )