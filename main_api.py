from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from vit5_predict import LeaveExtractor
from ocr_processor import OCRProcessor
from preprocess import clean_text
import uvicorn
import os
from typing import Optional

app = FastAPI(title="Leave Extractor Pro - OCR + ViT5")

templates = Jinja2Templates(directory="templates")

extractor = None
ocr_processor = None

@app.on_event("startup")
def load_models():
    global extractor, ocr_processor
    print("[Startup] Loading models...")

    extractor = LeaveExtractor(model_path="models/vit5_finetuned_gpu")
    ocr_processor = OCRProcessor()

    print("[Startup] Models loaded successfully!")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})


@app.post("/", response_class=HTMLResponse)
async def extract_from_form(
    request: Request,
    email_text: Optional[str] = Form(None, description="Nội dung email dạng text"),
    file: Optional[UploadFile] = File(None, description="Ảnh hoặc PDF scan email")
):
    try:
        raw_text = ""

        if extractor is None or ocr_processor is None:
            raise Exception("Model chưa được load")

        if file and file.filename:
            if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf')):
                raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file .png, .jpg, .jpeg hoặc .pdf")

            os.makedirs("temp", exist_ok=True)
            file_path = os.path.join("temp", file.filename)

            with open(file_path, "wb") as f:
                f.write(await file.read())

            raw_text = ocr_processor.extract_text(file_path)

            try:
                os.remove(file_path)
            except:
                pass

        elif email_text and email_text.strip():
            raw_text = email_text.strip()

        else:
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "result": {"error": "Vui lòng cung cấp nội dung email hoặc upload file"}}
            )

        cleaned = clean_text(raw_text)
        result = extractor.predict(cleaned)

        return templates.TemplateResponse(
            "index.html",
            {"request": request, "result": result}
        )

    except HTTPException as he:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "result": {"error": he.detail}}
        )

    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "result": {"error": f"Lỗi xử lý: {str(e)}"}}
        )


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": extractor is not None
    }


if __name__ == "__main__":
    uvicorn.run(
        "main_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )