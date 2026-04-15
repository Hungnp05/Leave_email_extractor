# Leave Extractor Pro

**Automatic Extraction of Leave Requests from Vietnamese Emails and Scanned Documents**

A powerful AI system that extracts structured leave information from Vietnamese emails, images, or scanned PDFs, and provides clean, usable JSON output.

Video demo: https://www.youtube.com/watch?v=fc7IRGaJ7Xo

## Features

- Supports **text**, **images** (PNG/JPG), and **PDF** inputs
- Accurate **OCR** using PaddleOCR for scanned documents and screenshots
- Structured information extraction using fine-tuned **ViT5** model
- Extracts: employee name, employee ID, leave periods (with dates and sessions), and reason
- Clean and user-friendly web interface
- GPU acceleration support (CUDA) with automatic CPU fallback
- Raw OCR text display for verification

## Technology Stack

- **NLP Model**: `VietAI/vit5-base` (fine-tuned for text-to-JSON)
- **OCR Engine**: PaddleOCR (with Vietnamese language support)
- **Backend**: FastAPI + Uvicorn
- **Frontend**: HTML + Jinja2 Templates
- **Libraries**: Transformers, Torch, PaddleOCR, PDF2Image, Pillow

## Project Structure
leave_extractorv2/
├── data/                          # Training datasets
├── models/vit5_finetuned_gpu/     # Fine-tuned ViT5 model
├── templates/index.html           # Web interface
├── vit5_predict.py                # ViT5 prediction class
├── ocr_processor.py               # OCR processing with PaddleOCR
├── preprocess.py                  # Text cleaning
├── datagen.py                     # Synthetic data generator
├── train_gpu.py                   # Training script (GPU)
├── main_api.py                    # FastAPI application
└── README.md


## Installation

### 1. Create and Activate Virtual Environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate


2. Install Dependencies
```bash
pip install --upgrade pip
pip install paddlepaddle paddleocr pdf2image pillow
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install fastapi uvicorn python-multipart transformers sentencepiece

3. (Optional) Login to Hugging Face
huggingface-cli login

Training the Model
- Generate training data:
```bash
python datagen.py
- Train the ViT5 model (recommended on GPU):
```bash
python train_gpu.py

The model will be saved in models/vit5_finetuned_gpu/.


Running the Application
```bash
uvicorn main_api:app --reload

Open your browser and navigate to:
http://127.0.0.1:8000