import streamlit as st
import cv2
import numpy as np
from pathlib import Path
import os
from PIL import Image
import matplotlib.pyplot as plt

# Cấu hình trang
st.set_page_config(page_title="Image Similarity Search", layout="wide")

# Đường dẫn dataset
SEG_TEST_PATH = Path("seg_test")
SEG_PATH = Path("seg")

def calculate_histogram(image_path):
    """Tính histogram cho ảnh"""
    img = cv2.imread(str(image_path))
    if img is None:
        return None
    
    # Chuyển sang HSV để so sánh tốt hơn
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Tính histogram cho các kênh H, S, V
    hist = cv2.calcHist([hsv], [0, 1, 2], None, [50, 60, 60], [0, 180, 0, 256, 0, 256])
    
    # Chuẩn hóa histogram
    cv2.normalize(hist, hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    
    return hist

def compare_histograms(hist1, hist2):
    """So sánh 2 histogram sử dụng phương pháp Correlation"""
    return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

def plot_histogram(image_path):
    """Vẽ histogram của ảnh"""
    img = cv2.imread(str(image_path))
    if img is None:
        return None
    
    # Chuyển từ BGR sang RGB để hiển thị đúng màu
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    # Hiển thị ảnh
    axes[0].imshow(img_rgb)
    axes[0].set_title('Ảnh gốc')
    axes[0].axis('off')
    
    # Vẽ histogram cho 3 kênh màu RGB
    colors = ('r', 'g', 'b')
    for i, color in enumerate(colors):
        hist = cv2.calcHist([img_rgb], [i], None, [256], [0, 256])
        axes[1].plot(hist, color=color, label=f'{color.upper()} channel')
    
    axes[1].set_title('Histogram RGB')
    axes[1].set_xlabel('Giá trị pixel')
    axes[1].set_ylabel('Số lượng pixel')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    return fig

def find_similar_images(query_image_path, top_k=10):
    """Tìm top K ảnh tương tự nhất"""
    query_hist = calculate_histogram(query_image_path)
    if query_hist is None:
        return []
    
    similarities = []
    
    # Duyệt qua tất cả ảnh trong thư mục seg
    for category in SEG_PATH.iterdir():
        if category.is_dir():
            for img_file in category.glob("*.jpg"):
                db_hist = calculate_histogram(img_file)
                if db_hist is not None:
                    similarity = compare_histograms(query_hist, db_hist)
                    similarities.append((img_file, similarity))
    
    # Sắp xếp theo độ tương đồng giảm dần
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    return similarities[:top_k]

def main():
    st.title("🔍 Tìm kiếm ảnh tương tự bằng Histogram")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Cài đặt")
        top_k = st.slider("Số ảnh tương tự:", min_value=1, max_value=20, value=10)
        st.markdown("---")
        st.info("**Hướng dẫn:**\n\n1. Upload ảnh từ tập test\n2. Hệ thống sẽ tìm ảnh tương tự trong tập seg\n3. Kết quả hiển thị theo độ tương đồng")
    
    # Upload file
    uploaded_file = st.file_uploader(
        "📤 Chọn ảnh từ tập test (seg_test)",
        type=['jpg', 'jpeg', 'png']
    )
    
    if uploaded_file is not None:
        # Lưu file tạm
        temp_path = Path("temp_upload.jpg")
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Hiển thị ảnh và histogram
        st.subheader("📊 Ảnh truy vấn và Histogram")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(str(temp_path), caption="Ảnh truy vấn", use_container_width=True)
        
        with col2:
            fig = plot_histogram(temp_path)
            if fig:
                st.pyplot(fig)
                plt.close()
        
        st.markdown("---")
        
        # Tìm ảnh tương tự
        with st.spinner(f"🔍 Đang tìm {top_k} ảnh tương tự nhất..."):
            similar_images = find_similar_images(temp_path, top_k=top_k)
        
        if similar_images:
            st.subheader(f"✨ Top {top_k} ảnh tương tự nhất")
            
            # Hiển thị kết quả theo grid
            cols_per_row = 5
            for i in range(0, len(similar_images), cols_per_row):
                cols = st.columns(cols_per_row)
                for j, col in enumerate(cols):
                    idx = i + j
                    if idx < len(similar_images):
                        img_path, similarity = similar_images[idx]
                        with col:
                            img = Image.open(img_path)
                            st.image(img, use_container_width=True)
                            st.caption(f"**#{idx+1}** - {similarity:.4f}")
                            st.caption(f"{img_path.parent.name}/{img_path.name}")
        else:
            st.warning("Không tìm thấy ảnh tương tự!")
        
        # Xóa file tạm
        if temp_path.exists():
            temp_path.unlink()
    
    else:
        st.info("👆 Vui lòng upload một ảnh để bắt đầu tìm kiếm")

if __name__ == "__main__":
    main()
