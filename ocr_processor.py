from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from PIL import Image
from pdf2image import convert_from_path
import torch
import re
import os

class OCRProcessor:
    def __init__(self):
        print("[OCR] Initializing VietOCR...")

        config = Cfg.load_config_from_name('vgg_transformer')
        config['cnn']['pretrained'] = True

        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        config['device'] = device

        print(f"[OCR] Using device: {device}")

        self.detector = Predictor(config)
        print("[OCR] VietOCR Ready")

    def extract_text(self, file_path: str) -> str:
        """Hỗ trợ ảnh (png/jpg) và PDF - trả về text ghép"""

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File không tồn tại: {file_path}")

        if file_path.lower().endswith('.pdf'):
            images = convert_from_path(file_path)
        else:
            images = [Image.open(file_path).convert("RGB")]

        full_text = []

        for img in images:
            try:
                text = self.detector.predict(img)
                full_text.append(text)
            except Exception as e:
                print(f"[OCR ERROR] {e}")

        result = " ".join(full_text)
        result = re.sub(r'\s+', ' ', result).strip()

        return result