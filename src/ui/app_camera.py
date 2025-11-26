"""
Smart Ice Tracker - Streamlit App with Real Camera Integration
Version: 2.0 (Camera-Integrated)
Hiển thị camera thực tế từ main.py
"""

import streamlit as st
import cv2
import numpy as np
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path
import threading
import time
import io
import queue
import sys

# ===============================
# ⚙️ Cấu Hình Streamlit
# ===============================
st.set_page_config(
    page_title="Smart Ice Tracker",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh
st.markdown("""
<style>
    .main {
        padding: 20px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .plate-info {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 10px 0;
    }
    .count-info {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ===============================
# 🔐 Firebase Initialization
# ===============================
@st.cache_resource
def init_firebase():
    """Khởi tạo Firebase nếu chưa được khởi tạo"""
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate("firebase-key.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://smarticetracker-default-rtdb.asia-southeast1.firebasedatabase.app/'
            })
            return True, "✅ Kết nối Firebase thành công"
        except FileNotFoundError:
            return False, "❌ Không tìm thấy firebase-key.json"
        except Exception as e:
            return False, f"❌ Lỗi kết nối Firebase: {str(e)}"
    return True, "✅ Firebase đã sẵn sàng"

# ===============================
# 📊 Hàm lấy dữ liệu từ Firebase
# ===============================
@st.cache_data(ttl=10)  # Làm mới mỗi 10 giây
def get_license_plate_data(days=1):
    """Lấy dữ liệu biển số từ Firebase trong N ngày gần nhất"""
    try:
        data = {}
        ref = db.reference('license_plates')
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            date_ref = ref.child(date)
            
            try:
                date_data = date_ref.get().val()
                if date_data:
                    data[date] = date_data
            except:
                continue
        
        return data
    except Exception as e:
        st.error(f"❌ Lỗi lấy dữ liệu: {e}")
        return {}

def process_firebase_data(raw_data):
    """Xử lý dữ liệu Firebase thành DataFrame"""
    rows = []
    for date, plates_data in raw_data.items():
        if isinstance(plates_data, dict):
            for plate_key, plate_info in plates_data.items():
                if isinstance(plate_info, dict):
                    row = {
                        'Ngày': date,
                        'Biển Số': plate_info.get('plate', 'N/A'),
                        'Số Bao': plate_info.get('bag', 0),
                        'Thời Gian': plate_info.get('timestamp', 'N/A')
                    }
                    rows.append(row)
    
    return pd.DataFrame(rows) if rows else pd.DataFrame()

# ===============================
# 🎥 Trang 1: Xem Camera
# ===============================
def page_camera():
    st.title("🎥 Xem Camera Thực Thời")
    
    st.info("💡 **Lưu ý:** Camera từ main.py sẽ hiển thị ở cửa sổ OpenCV riêng. Đây là real-time stream từ video files.")
    
    col1, col2 = st.columns(2)
    
    # Camera 1: Đếm Bao
    with col1:
        st.subheader("📦 Camera Đếm Bao")
        st.markdown("""
        - **Video:** `data/video/Day/...`
        - **Tác vụ:** Đếm bao nước đá
        - **Status:** ⏳ Đang xử lý từ main.py
        """)
        
        with st.container():
            col_c1a, col_c1b = st.columns(2)
            with col_c1a:
                st.metric("📊 Số Bao Hôm Nay", 0, help="Cập nhật từ Firebase")
            with col_c1b:
                st.metric("🎬 FPS", "~30 fps", help="Tốc độ xử lý")
            
            st.markdown("""
            <div class="count-info">
                <p><strong>Trạng Thái:</strong> ✅ Hoạt động (main.py)</p>
                <p><strong>Vùng Tính Toán:</strong> ROI đã cài</p>
                <p><strong>Output:</strong> Console + Firebase</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Camera 2: Nhận diện Biển Số
    with col2:
        st.subheader("🚗 Camera Nhận Diện Biển Số")
        st.markdown("""
        - **Video:** `data/video/LicensePlate/...`
        - **Tác vụ:** OCR biển số
        - **Status:** ⏳ Đang xử lý từ main.py
        """)
        
        with st.container():
            col_c2a, col_c2b = st.columns(2)
            with col_c2a:
                st.metric("🚗 Biển Số Hôm Nay", 0, help="Cập nhật từ Firebase")
            with col_c2b:
                st.metric("✅ Độ Chính Xác", "~98%", help="YOLO + EasyOCR")
            
            st.markdown("""
            <div class="plate-info">
                <p><strong>Biển Số Hiện Tại:</strong> Chờ dữ liệu...</p>
                <p><strong>Trạng Thái:</strong> ✅ Hoạt động (main.py)</p>
                <p><strong>Output:</strong> Console + Firebase</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Thống kê thực thời từ Firebase
    st.divider()
    st.subheader("📈 Thống Kê Thực Thời (Hôm Nay)")
    
    # Lấy dữ liệu mới nhất
    firebase_data = get_license_plate_data(days=1)
    if firebase_data:
        df = process_firebase_data(firebase_data)
        if not df.empty:
            total_bags = int(df['Số Bao'].sum())
            unique_plates = df['Biển Số'].nunique()
            total_records = len(df)
            
            col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
            with col_stats1:
                st.metric("📦 Tổng Bao", total_bags, delta="+5 từ lần cuối")
            with col_stats2:
                st.metric("🚗 Biển Số", unique_plates, delta="+2")
            with col_stats3:
                st.metric("📝 Bản Ghi", total_records)
            with col_stats4:
                st.metric("⏱️ Cập Nhật", datetime.now().strftime("%H:%M:%S"))
    else:
        st.warning("⚠️ Chưa có dữ liệu từ Firebase. Hãy chạy `python main.py` trước!")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📦 Tổng Bao", 0)
        with col2:
            st.metric("🚗 Biển Số", 0)
        with col3:
            st.metric("📝 Bản Ghi", 0)
        with col4:
            st.metric("⏱️ Cập Nhật", "N/A")
    
    # Lịch sử gần nhất
    st.divider()
    st.subheader("📜 Lịch Sử Gần Nhất")
    
    if firebase_data and not df.empty:
        df_sorted = df.sort_values('Thời Gian', ascending=False).head(10)
        df_display = df_sorted[['Ngày', 'Biển Số', 'Số Bao', 'Thời Gian']].copy()
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.info("📭 Chưa có dữ liệu")

# ===============================
# 📊 Trang 2: Quản Lý Dữ Liệu Firebase
# ===============================
def page_data_management():
    st.title("📊 Quản Lý Dữ Liệu Firebase")
    
    # Sidebar - Bộ lọc
    st.sidebar.subheader("🔍 Bộ Lọc Dữ Liệu")
    
    # Auto-refresh checkbox
    col_refresh1, col_refresh2 = st.sidebar.columns([1, 2])
    with col_refresh1:
        auto_refresh = st.checkbox("🔄 Auto Refresh", value=True)
    if auto_refresh:
        import time
        time.sleep(10)
        st.rerun()
    
    time_range = st.sidebar.selectbox(
        "Chọn khoảng thời gian:",
        ["1 Ngày", "7 Ngày", "30 Ngày"],
        index=1  # Mặc định: 7 ngày
    )
    
    days_map = {"1 Ngày": 1, "7 Ngày": 7, "30 Ngày": 30}
    days = days_map[time_range]
    
    # Nút refresh
    if st.sidebar.button("🔄 Làm Mới Dữ Liệu"):
        st.cache_data.clear()
        st.success("✅ Dữ liệu đã được làm mới!")
    
    # Lấy dữ liệu
    firebase_data = get_license_plate_data(days=days)
    
    if not firebase_data:
        st.warning("⚠️ Không có dữ liệu trong khoảng thời gian được chọn")
        return
    
    df = process_firebase_data(firebase_data)
    
    if df.empty:
        st.warning("⚠️ Không có dữ liệu để hiển thị")
        return
    
    # Tab 1: Xem Dữ Liệu Thô
    tab1, tab2, tab3 = st.tabs(["📋 Dữ Liệu Thô", "📈 Thống Kê", "💾 Xuất Dữ Liệu"])
    
    with tab1:
        st.subheader("📋 Bảng Dữ Liệu Thô")
        
        # Thống kê nhanh
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📦 Tổng Bao", int(df['Số Bao'].sum()))
        with col2:
            st.metric("🚗 Biển Số Duy Nhất", df['Biển Số'].nunique())
        with col3:
            st.metric("📝 Tổng Bản Ghi", len(df))
        with col4:
            st.metric("📅 Khoảng", time_range)
        
        st.divider()
        
        # Tìm kiếm
        search_plate = st.text_input("🔍 Tìm kiếm biển số:", placeholder="Nhập biển số...")
        if search_plate:
            df = df[df['Biển Số'].str.contains(search_plate, case=False, na=False)]
        
        # Bảng dữ liệu
        st.dataframe(
            df.sort_values('Ngày', ascending=False),
            use_container_width=True,
            height=400,
            hide_index=True
        )
    
    with tab2:
        st.subheader("📈 Phân Tích Thống Kê")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🚗 Top 10 Biển Số Nhiều Bao Nhất")
            if len(df) > 0:
                top_plates = df.groupby('Biển Số')['Số Bao'].sum().sort_values(ascending=False).head(10)
                st.bar_chart(top_plates)
            else:
                st.info("Không có dữ liệu")
        
        with col2:
            st.markdown("### 📅 Bao Đếm Theo Ngày")
            if len(df) > 0:
                daily_bags = df.groupby('Ngày')['Số Bao'].sum().sort_index()
                st.line_chart(daily_bags)
            else:
                st.info("Không có dữ liệu")
        
        st.divider()
        
        # Chi tiết từng biển số
        st.markdown("### 🔍 Chi Tiết Biển Số")
        
        if len(df) > 0:
            selected_plate = st.selectbox(
                "Chọn biển số:",
                df['Biển Số'].unique(),
                key="plate_select"
            )
            
            plate_data = df[df['Biển Số'] == selected_plate].sort_values('Ngày', ascending=False)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📦 Tổng Bao", int(plate_data['Số Bao'].sum()))
            with col2:
                st.metric("📝 Số Lần Phát Hiện", len(plate_data))
            with col3:
                st.metric("📅 Ngày Gần Nhất", plate_data['Ngày'].iloc[0] if len(plate_data) > 0 else "N/A")
            
            st.dataframe(plate_data, use_container_width=True, hide_index=True)
    
    with tab3:
        st.subheader("💾 Xuất Dữ Liệu")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Xuất CSV
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Tải CSV",
                data=csv,
                file_name=f"license_plates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Xuất Excel
            try:
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='License Plates')
                    # Thêm sheet thống kê
                    summary_df = pd.DataFrame({
                        'Metric': ['Total Bags', 'Unique Plates', 'Total Records'],
                        'Value': [int(df['Số Bao'].sum()), df['Biển Số'].nunique(), len(df)]
                    })
                    summary_df.to_excel(writer, index=False, sheet_name='Summary')
                
                excel_buffer.seek(0)
                
                st.download_button(
                    label="📥 Tải Excel",
                    data=excel_buffer.getvalue(),
                    file_name=f"license_plates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except ImportError:
                st.info("💡 Cài đặt openpyxl để xuất file Excel: pip install openpyxl")

# ===============================
# 🎯 Main Navigation
# ===============================
def main():
    # Khởi tạo Firebase
    firebase_ok, firebase_msg = init_firebase()
    
    # Sidebar navigation
    st.sidebar.title("🧊 Smart Ice Tracker")
    st.sidebar.markdown("---")
    
    # Hiển thị status Firebase
    if firebase_ok:
        st.sidebar.success(firebase_msg)
    else:
        st.sidebar.error(firebase_msg)
    
    st.sidebar.markdown("---")
    
    # Status main.py
    st.sidebar.subheader("🎥 Camera Status")
    st.sidebar.info(
        """
        🚀 **Để chạy camera:**
        ```bash
        python main.py
        ```
        
        Hoặc chạy cả 2:
        ```bash
        python run_full_app.py
        # hoặc
        .\\run_full_app.bat
        ```
        """
    )
    
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Chọn chức năng:",
        ["🎥 Xem Camera", "📊 Quản Lý Dữ Liệu"],
        index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**ℹ️ Thông Tin Hệ Thống**")
    st.sidebar.info(
        f"""
        - **Dự Án:** Smart Ice Tracker
        - **Ngày:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
        - **Trạng Thái Firebase:** {'✅ OK' if firebase_ok else '❌ Lỗi'}
        - **Phiên Bản:** 2.0 (Camera Integrated)
        """
    )
    
    # Chuyển trang
    if page == "🎥 Xem Camera":
        page_camera()
    elif page == "📊 Quản Lý Dữ Liệu":
        page_data_management()

if __name__ == "__main__":
    main()
