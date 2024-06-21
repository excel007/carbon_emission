import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
st.title('ระบบเปรียบเทียบรถยนต์ตามปริมาณ CO2')

# ฟังก์ชันสำหรับเลือกข้อมูลรถยนต์
def select_car(prefix=""):
    car_brands = data['car_brand'].unique()
    selected_brand = st.selectbox(f'เลือกยี่ห้อรถ {prefix}', car_brands, key=f'{prefix}_brand')

    filtered_data = data[data['car_brand'] == selected_brand]
    car_series = filtered_data['car_series'].unique()
    selected_series = st.selectbox(f'เลือกรุ่นรถ {prefix}', car_series, key=f'{prefix}_series')

    filtered_data = filtered_data[filtered_data['car_series'] == selected_series]
    model_years = filtered_data['model_year'].unique()
    selected_year = st.selectbox(f'เลือกปีรุ่น {prefix}', model_years, key=f'{prefix}_year')

    filtered_data = filtered_data[filtered_data['model_year'] == selected_year]
    return filtered_data

# เลือกรถยนต์ 2 คัน
st.header("รถยนต์คันที่ 1")
car1 = select_car("คันที่ 1")
st.header("รถยนต์คันที่ 2")
car2 = select_car("คันที่ 2")

# กำหนดคอลัมน์ที่ต้องการแสดง
columns_to_display = ['car_brand', 'car_series', 'model_year', 'car_price', 'emissions_co2', 'car_capacity']

# สร้างปุ่มสำหรับประมวลผล
if st.button('เปรียบเทียบ'):
    if len(car1) > 0 and len(car2) > 0:
        # ข้อมูลรถยนต์คันที่ 1
        cluster1 = car1['pca_kmean_cluster'].values[0]
        cluster_name1 = cluster_names.get(cluster1, 'ไม่ทราบกลุ่ม')
        st.subheader(f'ผลลัพธ์สำหรับรถยนต์คันที่ 1: {car1["car_brand"].values[0]} {car1["car_series"].values[0]} ปี {car1["model_year"].values[0]}')
        st.write(f'กลุ่ม: {cluster_name1}')
        st.write(car1[columns_to_display].iloc[0])

        # ข้อมูลรถยนต์คันที่ 2
        cluster2 = car2['pca_kmean_cluster'].values[0]
        cluster_name2 = cluster_names.get(cluster2, 'ไม่ทราบกลุ่ม')
        st.subheader(f'ผลลัพธ์สำหรับรถยนต์คันที่ 2: {car2["car_brand"].values[0]} {car2["car_series"].values[0]} ปี {car2["model_year"].values[0]}')
        st.write(f'กลุ่ม: {cluster_name2}')
        st.write(car2[columns_to_display].iloc[0])

        # ฟังก์ชันสำหรับสร้างกราฟ
        def plot_comparison(feature, feature_name):
            fig, ax = plt.subplots()
            index = ['car no 1', 'car no 2']
            values = [car1[feature].values[0], car2[feature].values[0]]

            ax.bar(index, values, color=['blue', 'orange'])
            ax.set_xlabel('รถยนต์')
            ax.set_ylabel(feature_name)
            ax.set_title(f'การเปรียบเทียบ {feature_name}')

            st.pyplot(fig)

        # แสดงกราฟการเปรียบเทียบ
        plot_comparison('emissions_co2', ' CO2 Emission')
        plot_comparison('car_price', 'Price')
        plot_comparison('car_capacity', 'Engine Capacity')

    else:
        st.warning('กรุณาเลือกรถยนต์ให้ครบทั้งสองคัน')
