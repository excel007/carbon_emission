import streamlit as st
import pandas as pd

# โหลดข้อมูลจากไฟล์ CSV
data = pd.read_csv('kmean_ICE.csv')

# กำหนดชื่อกลุ่มสำหรับแต่ละค่า pca_kmean_cluster
cluster_names = {
    0: 'รถเป็นมิตรต่อสิ่งแวดล้อม',
    1: 'รถครอบครัวประหยัดพลังงาน',
    2: 'รถหรูสมรรถนะสูง',
    3: 'รถระดับกลาง'
}

# สร้างหน้าแอปพลิเคชัน
st.title('ค้นหากลุ่มรถยนต์')

# สร้าง Dropdown สำหรับเลือกยี่ห้อรถ
car_brands = data['car_brand'].unique()
selected_brand = st.selectbox('เลือกยี่ห้อรถ', car_brands)

# กรองข้อมูลตามยี่ห้อรถที่เลือก
filtered_data = data[data['car_brand'] == selected_brand]

# สร้าง Dropdown สำหรับเลือกรุ่นรถ
car_series = filtered_data['car_series'].unique()
selected_series = st.selectbox('เลือกรุ่นรถ', car_series)

# กรองข้อมูลตามรุ่นรถที่เลือก
filtered_data = filtered_data[filtered_data['car_series'] == selected_series]

# สร้าง Dropdown สำหรับเลือกปีรุ่น
model_years = filtered_data['model_year'].unique()
selected_year = st.selectbox('เลือกปีรุ่น', model_years)

# กรองข้อมูลตามปีรุ่นที่เลือก
filtered_data = filtered_data[filtered_data['model_year'] == selected_year]

# สร้างปุ่มสำหรับประมวลผล
if st.button('ประมวลผล'):
    if len(filtered_data) > 0:
        cluster = filtered_data['pca_kmean_cluster'].values[0]
        cluster_name = cluster_names[cluster]
        st.success(f'รถยนต์ {selected_brand} {selected_series} ปี {selected_year} อยู่ในกลุ่ม: {cluster_name}')
    else:
        st.warning('ไม่พบข้อมูลรถยนต์ที่ตรงกับเงื่อนไขที่เลือก')
