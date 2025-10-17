
# 🧪 Lab-03: Image Enhancing  
**Môn:** Xử lý ảnh số  
**Mục tiêu:** Xây dựng ứng dụng nâng cao chất lượng ảnh (Image Enhancement App)

---

## 🖼️ Mô tả bài lab
Ứng dụng cho phép người dùng **tải lên một ảnh màu** từ máy tính và thực hiện 3 bước xử lý ảnh:
1. **Denoising / Smoothing** – khử nhiễu, làm mượt ảnh  
2. **Sharpening** – làm nét ảnh  
3. **Edge Detection** – phát hiện biên cạnh bằng 3 bộ lọc:
   - Sobel  
   - Prewitt  
   - Canny  

Kết quả hiển thị gồm:
- Ảnh gốc  
- Ảnh sau smoothing  
- Ảnh sau sharpening  
- 3 ảnh biên cạnh (Sobel, Prewitt, Canny)

---

## 📂 Cấu trúc thư mục
```
Lab03_ImageEnhancing/
│
├── lab03_app.py          # Mã nguồn chính (Streamlit + OpenCV)
├── requirements.txt      # Danh sách thư viện cần cài
└── README.md             # File hướng dẫn
```

---

## ⚙️ Cài đặt môi trường (Windows)

### 1️⃣ Bước 1: Tạo môi trường ảo
Mở **Command Prompt (hoặc PowerShell)** tại thư mục chứa file `lab03_app.py`, rồi gõ:
```bash
python -m venv venv
```

### 2️⃣ Bước 2: Kích hoạt môi trường ảo
```bash
venv\Scripts\activate
```
Lúc này terminal sẽ hiện `(venv)` ở đầu dòng.

### 3️⃣ Bước 3: Cài các thư viện cần thiết
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ▶️ Chạy ứng dụng
Sau khi cài đặt xong, chạy:
```bash
streamlit run lab03_app.py
```

- Trình duyệt web sẽ tự mở trang:  
  👉 [http://localhost:8501](http://localhost:8501)
- Tại đây bạn có thể:
  - **Upload ảnh** (PNG/JPG/BMP/TIFF)  
  - Chọn bộ lọc **Smoothing / Sharpening / Edge Detection**  
  - Quan sát và **tải xuống ảnh kết quả**

---

## 🧠 Các kỹ thuật chính sử dụng
| Nhóm chức năng | Mô tả kỹ thuật | Thư viện |
|-----------------|----------------|-----------|
| **Smoothing** | Gaussian Blur, Median Blur, Bilateral Filter | OpenCV |
| **Sharpening** | Unsharp Masking, Laplacian Kernel | OpenCV |
| **Edge Detection** | Sobel, Prewitt (tự cài kernel), Canny | OpenCV |
| **Giao diện web** | Upload file, hiển thị ảnh, download kết quả | Streamlit |
| **Xử lý ảnh** | Chuyển đổi giữa PIL ↔ OpenCV (BGR/RGB/Gray) | Pillow, NumPy |

---

## 📘 Gợi ý báo cáo
- Giải thích vai trò từng bộ lọc.  
- So sánh ảnh gốc và ảnh sau khi xử lý.  
- Minh họa ảnh biên bằng từng phương pháp (Sobel, Prewitt, Canny).  
- Nhận xét ưu – nhược điểm của từng kỹ thuật.

---

## 👨‍💻 Người thực hiện
- **Tên:** (Điền tên sinh viên)  
- **MSSV:** (Điền mã số sinh viên)  
- **Lớp:** (Điền lớp học phần)  
