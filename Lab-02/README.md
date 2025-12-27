# Image Similarity Search using Histogram

Ứng dụng tìm kiếm ảnh tương tự sử dụng phương pháp so khớp Histogram.

## Cài đặt

```bash
pip install -r requirements.txt
```

## Chạy ứng dụng

```bash
streamlit run app.py
```

## Hướng dẫn sử dụng

1. Chạy lệnh `streamlit run app.py`
2. Upload một ảnh từ thư mục `seg_test`
3. Xem histogram của ảnh và top 10 ảnh tương tự nhất từ thư mục `seg`

## Cấu trúc thư mục

```
dataset/
├── seg/           # Thư mục chứa ảnh để truy vấn
├── seg_test/      # Thư mục chứa ảnh test
├── app.py         # Ứng dụng chính
└── requirements.txt
```
