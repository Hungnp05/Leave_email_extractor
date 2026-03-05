# Leave Extractor - Trích xuất thông tin nghỉ phép từ email

Dự án sử dụng mô hình ngôn ngữ tiếng Việt (ViT5) để trích xuất thông tin nghỉ phép từ email tiếng Việt (tên nhân viên, mã NV, khoảng thời gian nghỉ, ca nghỉ, lý do)

### Tính năng chính
- Trích xuất tự động: employee_name, employee_id, leave_periods (start_date, end_date, start_session, end_session)
- Tóm tắt lý do xin nghỉ phép ngắn gọn từ phần "vì..." trong email
- Giao diện web đơn giản bằng FastAPI + HTML
- Hỗ trợ chạy trên GPU (CUDA) hoặc CPU

### Công nghệ sử dụng
- **Model trích xuất**: VietAI/vit5-base (fine-tune cho task text-to-text JSON)
- **Model tóm tắt lý do**: vinai/bartpho-syllable (BART tiếng Việt chuyên tóm tắt)
- **Framework**: FastAPI, Uvicorn, Jinja2
- **Thư viện**: transformers, torch, preprocess

## Chuẩn bị môi trường

### Yêu cầu hệ thống
- Python 3.8–3.11
- GPU NVIDIA (khuyến nghị) hoặc CPU (chậm hơn)  
- Dung lượng RAM: ≥8GB (GPU) hoặc ≥16GB (CPU)  

### Cài đặt
1. Clone dự án (hoặc mở thư mục hiện có):  
   ```bash  
   git clone <url-repo>  
   cd leave_extractor  

Tạo môi trường ảo và kích hoạt:  
python -m venv .venv  
# Windows  
.venv\Scripts\activate  
# Linux/Mac  
source .venv/bin/activate  
Cài đặt các thư viện cần thiết:Bashpip install --upgrade pip  
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121  # nếu dùng CUDA 12.1  
# hoặc CPU: pip install torch torchvision torchaudio  
pip install transformers datasets accelerate sentencepiece fastapi uvicorn jinja2 python-multipart regex  
(Tùy chọn) Đăng nhập Hugging Face để tải model nhanh hơn:Bashhuggingface-cli login(dán token từ https://huggingface.co/settings/tokens)  

Hướng dẫn train model (ViT5 cho trích xuất JSON)  

Tạo dữ liệu huấn luyện (nếu chưa có):python datagen.py→ File data/training_data_phot5.json sẽ được tạo (có thể tùy chỉnh số mẫu trong code).  
Train model (dùng GPU):python train_gpu.py  
Train model (dùng CPU):python train.py  

Model sẽ lưu vào thư mục models/vit5_finetuned_gpu.  

Thời gian train: 1–4 giờ tùy GPU (RTX 3060/4070 khoảng 1–2 giờ).  
Nếu VRAM hết: giảm per_device_train_batch_size=2 trong train_gpu.py.  

(Tùy chọn) Train lại nếu cần cải thiện:  
Xóa thư mục cũ:  
rmdir /s /q models\vit5_finetuned_gpu  
Chạy lại train_gpu.py.  
 
Hướng dẫn chạy ứng dụng  

Chạy server FastAPI:uvicorn main_api:app --reload hoặc python main_api.py  
Mở trình duyệt:texthttp://127.0.0.1:8000  
Sử dụng:  
Dán toàn bộ nội dung email vào textarea.  
Nhấn Trích xuất.  
Kết quả sẽ hiển thị:  
Thông tin trích xuất (JSON) – dù có lỗi parse vẫn hiển thị raw output.  
Tóm tắt lý do xin nghỉ (ngắn gọn 5–10 từ).  

Ví dụ input text  
Kính gửi Anh Trưởng phòng,  
Tôi tên là Nguyễn Phú Hùng, mã nhân viên NV001...  
Lý do xin nghỉ là vì con tôi bị ốm nặng...  
Kết quả mong đợi  

Trích xuất: employee_name, employee_id, leave_periods  
Tóm tắt lý do: "con bị ốm nặng" hoặc "chăm sóc con ốm nặng"  

