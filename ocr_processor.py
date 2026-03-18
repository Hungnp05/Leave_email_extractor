from paddleocr import PaddleOCR
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import re
import os

class OCRProcessor:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='vi')

    def extract_text(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File không tồn tại: {file_path}")

        if file_path.lower().endswith('.pdf'):
            images = convert_from_path(file_path)
        else:
            images = [Image.open(file_path)]

        full_text = ""
        for img in images:
            img = img.convert('L')
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2.5)
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(2.0)
            img = img.filter(ImageFilter.SHARPEN)
            img = img.filter(ImageFilter.MedianFilter())

            w, h = img.size
            if w < 1200:
                img = img.resize((int(w*2.0), int(h*2.0)), Image.LANCZOS)

            result = self.ocr.ocr(img)
            for line in result:
                for word_info in line:
                    text = word_info[1][0]
                    full_text += text + " "

        full_text = re.sub(r'\s+', ' ', full_text).strip()
        return full_text