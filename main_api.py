from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from vit5_predict import LeaveExtractor
from preprocess import clean_text
import uvicorn

app = FastAPI(
    title="Leave Extractor - ViT5 GPU",
    description="Trích xuất thông tin nghỉ phép từ email tiếng Việt",
    version="1.0"
)

templates = Jinja2Templates(directory="templates")

# Load model một lần khi khởi động (dùng GPU nếu có)
extractor = LeaveExtractor(model_path="models/vit5_finetuned_gpu")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": None}
    )

@app.post("/", response_class=HTMLResponse)
async def extract_from_form(request: Request, email_text: str = Form(...)):
    if not email_text.strip():
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "result": {"error": "Vui lòng nhập nội dung email"}}
        )

    try:
        cleaned = clean_text(email_text)
        print(f"[API] Cleaned: {cleaned[:100]}...")

        result = extractor.predict(cleaned)
        print(f"[API] Result: {result}")

        return templates.TemplateResponse(
            "index.html",
            {"request": request, "result": result}
        )

    except Exception as e:
        error_msg = f"Lỗi xử lý: {str(e)}"
        print("[API ERROR]", error_msg)
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "result": {"error": error_msg}}
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "device": extractor.device}

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )