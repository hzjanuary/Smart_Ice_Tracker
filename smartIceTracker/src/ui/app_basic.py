"""
Smart Ice Tracker - Streamlit Application (Basic Version)
Ứng dụng với 2 trang: Xem Camera và Quản Lý Dữ Liệu Firebase
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
from collections import defaultdict
import io

# ===============================
# ⚙️ Cấu hình Streamlit
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
            return True
        except Exception as e:
            st.error(f"❌ Lỗi kết nối Firebase: {e}")
            return False
    return True

# ===============================
# 📊 Hàm lấy dữ liệu từ Firebase
# ===============================
@st.cache_data(ttl=30)
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
    
    col1, col2 = st.columns(2)
    
    # Camera 1: Đếm Bao
    with col1:
        st.subheader("📦 Camera Đếm Bao")
        st.info("Chế độ: Live Stream từ Camera 1 (Bag Counter)")
        
        # Placeholder cho video
        camera1_placeholder = st.empty()
        info1_placeholder = st.empty()
        
        # Thông tin biển số Camera 1
        with info1_placeholder.container():
            st.markdown("""
            <div class="count-info">
                <h4>📊 Thông Tin Thực Thời</h4>
                <p><strong>Số Bao Phát Hiện:</strong> 0</p>
                <p><strong>Trạng Thái:</strong> ⏸️ Chưa kết nối</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Hiển thị sample frame
        camera1_placeholder.image("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==", 
                                 caption="Camera 1 - Đếm Bao", use_container_width=True)
    
    # Camera 2: Nhận diện Biển Số
    with col2:
        st.subheader("🚗 Camera Nhận Diện Biển Số")
        st.info("Chế độ: Live Stream từ Camera 2 (License Plate)")
        
        # Placeholder cho video
        camera2_placeholder = st.empty()
        info2_placeholder = st.empty()
        
        # Thông tin Camera 2
        with info2_placeholder.container():
            st.markdown("""
            <div class="plate-info">
                <h4>🔍 Thông Tin Biển Số</h4>
                <p><strong>Biển Số Hiện Tại:</strong> Chưa phát hiện</p>
                <p><strong>Độ Chính Xác:</strong> 0%</p>
                <p><strong>Trạng Thái:</strong> ⏸️ Chưa kết nối</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Hiển thị sample frame
        camera2_placeholder.image("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
                                 caption="Camera 2 - Biển Số", use_container_width=True)
    
    # Thống kê thực thời
    st.divider()
    st.subheader("📈 Thống Kê Thực Thời")
    
    col_stats1, col_stats2, col_stats3 = st.columns(3)
    
    with col_stats1:
        st.metric(label="📦 Tổng Bao Đếm (Hôm Nay)", value=0, delta="")
    
    with col_stats2:
        st.metric(label="🚗 Biển Số Phát Hiện (Hôm Nay)", value=0, delta="")
    
    with col_stats3:
        st.metric(label="⏱️ Cập Nhật Lần Cuối", value="--:--:--")

# ===============================
# 📊 Trang 2: Quản Lý Dữ Liệu Firebase
# ===============================
def page_data_management():
    st.title("📊 Quản Lý Dữ Liệu Firebase")
    
    # Sidebar - Bộ lọc
    st.sidebar.subheader("🔍 Bộ Lọc Dữ Liệu")
    
    time_range = st.sidebar.selectbox(
        "Chọn khoảng thời gian:",
        ["1 Ngày", "7 Ngày", "30 Ngày"],
        index=0
    )
    
    days_map = {"1 Ngày": 1, "7 Ngày": 7, "30 Ngày": 30}
    days = days_map[time_range]
    
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
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📦 Tổng Bao", df['Số Bao'].sum())
        with col2:
            st.metric("🚗 Biển Số Duy Nhất", df['Biển Số'].nunique())
        with col3:
            st.metric("📝 Tổng Bản Ghi", len(df))
        
        st.divider()
        
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
            top_plates = df.groupby('Biển Số')['Số Bao'].sum().sort_values(ascending=False).head(10)
            st.bar_chart(top_plates)
        
        with col2:
            st.markdown("### 📅 Bao Đếm Theo Ngày")
            daily_bags = df.groupby('Ngày')['Số Bao'].sum().sort_index()
            st.line_chart(daily_bags)
        
        st.divider()
        
        # Chi tiết từng biển số
        st.markdown("### 🔍 Chi Tiết Biển Số")
        
        selected_plate = st.selectbox(
            "Chọn biển số:",
            df['Biển Số'].unique(),
            key="plate_select"
        )
        
        plate_data = df[df['Biển Số'] == selected_plate].sort_values('Ngày', ascending=False)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📦 Tổng Bao", plate_data['Số Bao'].sum())
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
            # Xuất Excel (nếu có openpyxl)
            try:
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='License Plates')
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
    if not init_firebase():
        st.stop()
    
    # Sidebar navigation
    st.sidebar.title("🧊 Smart Ice Tracker")
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
        - **Trạng Thái:** ✅ Hoạt Động
        """
    )
    
    # Chuyển trang
    if page == "🎥 Xem Camera":
        page_camera()
    elif page == "📊 Quản Lý Dữ Liệu":
        page_data_management()

if __name__ == "__main__":
    main()
