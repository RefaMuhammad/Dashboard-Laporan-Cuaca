import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import branca.colormap as cm

# Set judul dashboard
st.title("Dashboard Laporan Cuaca")

# Path file data
data_path = "https://github.com/RefaMuhammad/Dashboard-Laporan-Cuaca/blob/main/dashboard/cleaned_air_quality_data.csv"

# Cek apakah file data ada
try:
    df_combined = pd.read_csv(data_path)
    df_combined['date'] = pd.to_datetime(df_combined[['year', 'month', 'day']])
    
    # Fitur interaktif: Filtering berdasarkan rentang tanggal
    st.sidebar.subheader("Filter Data")
    min_date, max_date = df_combined['date'].min(), df_combined['date'].max()
    date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [min_date, max_date], min_value=min_date, max_value=max_date)
    
    if len(date_range) == 2:
        df_filtered = df_combined[(df_combined['date'] >= pd.Timestamp(date_range[0])) & (df_combined['date'] <= pd.Timestamp(date_range[1]))]
    else:
        df_filtered = df_combined
    
    # Fitur interaktif: Filtering berdasarkan stasiun pengamatan
    stations = df_filtered['station'].unique()
    selected_stations = st.sidebar.multiselect("Pilih Stasiun", stations, default=stations)
    df_filtered = df_filtered[df_filtered['station'].isin(selected_stations)]
    
    # Visualisasi dengan Seaborn
    st.subheader("Grafik Tren Polusi Udara")
    numeric_cols = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    df_filtered.groupby("month")[numeric_cols].mean().plot(ax=ax)
    plt.xlabel("Bulan")
    plt.ylabel("Konsentrasi (µg/m³)")
    plt.title("Rata-rata Konsentrasi Polutan per Bulan")
    plt.legend(title="Polutan")
    st.pyplot(fig)
    
    # Peta Interaktif jika ada koordinat
    st.subheader("Geospatial Analysis Air Quality")
    station_locations = {
        "Dingling": [40.290, 116.220],
        "Aotizhongxin": [40.000, 116.407],
        "Changping": [40.220, 116.234],
        "Guanyuan": [39.930, 116.362],
        "Huairou": [40.320, 116.630],
        "Nongzhanguan": [39.933, 116.467],
        "Shunyi": [40.130, 116.653],
        "Tiantan": [39.881, 116.414],
        "Wanshouxigong": [39.888, 116.349],
        "Dongsi": [39.928, 116.417]
    }
    
    df_latest = df_filtered[df_filtered['year'] == df_filtered['year'].max()].groupby('station').mean(numeric_only=True).reset_index()
    df_latest['latitude'] = df_latest['station'].map(lambda x: station_locations.get(x, [None, None])[0])
    df_latest['longitude'] = df_latest['station'].map(lambda x: station_locations.get(x, [None, None])[1])
    map_data = df_latest.dropna(subset=['latitude', 'longitude', 'PM2.5'])
    
    m = folium.Map(location=[39.9, 116.4], zoom_start=10)
    
    # Menambahkan legenda warna
    colormap = cm.LinearColormap(colors=['green', 'orange', 'red'], vmin=0, vmax=150)
    colormap.caption = 'PM2.5 Concentration (µg/m³)'
    m.add_child(colormap)

    for _, row in map_data.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=8,
            color='red' if row['PM2.5'] > 100 else 'orange' if row['PM2.5'] > 50 else 'green',
            fill=True,
            fill_color='red' if row['PM2.5'] > 100 else 'orange' if row['PM2.5'] > 50 else 'green',
            fill_opacity=0.7,
            popup=folium.Popup(f"{row['station']}: {row['PM2.5']} µg/m³", parse_html=True)
        ).add_to(m)
    
    heat_data = [[row['latitude'], row['longitude'], row['PM2.5']] for _, row in map_data.iterrows()]
    HeatMap(heat_data).add_to(m)
    
    folium_static(m)

    # Analisis Pengaruh Arah Angin terhadap Polutan
    st.subheader("Pengaruh Arah Angin terhadap Konsentrasi Polutan")
    
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    for i, col in enumerate(numeric_cols):
        ax = axes[i // 3, i % 3]
        mean_polutan_by_wd = df_filtered.groupby('wd')[col].mean().reset_index()
        sns.barplot(x='wd', y=col, data=mean_polutan_by_wd, palette='viridis', ax=ax)
        ax.set_title(f'Rata-rata {col} Berdasarkan Arah Angin')
        ax.set_xlabel('Arah Angin (wd)')
        ax.set_ylabel(f'Rata-rata {col}')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.write("Polutan PM2.5, PM10, SO2, NO2, dan CO memiliki konsentrasi tertinggi saat angin bertiup dari timur dan selatan, mengindikasikan adanya sumber emisi di wilayah tersebut, seperti kawasan industri atau lalu lintas padat. Sebaliknya, konsentrasi lebih rendah saat angin berasal dari barat dan barat laut, yang kemungkinan memiliki lebih sedikit sumber pencemaran atau lebih banyak area hijau.")
    st.write("Berbeda dengan polutan lainnya, Ozon (O3) justru lebih tinggi saat angin berasal dari selatan dan lebih rendah saat angin dari timur dan utara, yang dapat dipengaruhi oleh reaksi kimia di atmosfer. Pola ini memberikan wawasan penting untuk kebijakan pengendalian polusi, seperti pembatasan emisi di area tertentu dan pemanfaatan ruang hijau guna meningkatkan kualitas udara.")
    
    # Analisis Pengaruh Curah Hujan terhadap Polutan
    st.subheader("Pengaruh Curah Hujan terhadap PM2.5 dan PM10")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(x='RAIN', y='PM2.5', data=df_filtered, scatter_kws={'alpha': 0.3}, line_kws={'color': 'red'}, ax=ax)
    ax.set_title('Hubungan Curah Hujan (RAIN) dan Konsentrasi PM2.5')
    ax.set_xlabel('Curah Hujan (RAIN)')
    ax.set_ylabel('Konsentrasi PM2.5')
    st.pyplot(fig)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(x='RAIN', y='PM10', data=df_filtered, scatter_kws={'alpha': 0.3}, line_kws={'color': 'blue'}, ax=ax)
    ax.set_title('Hubungan Curah Hujan (RAIN) dan Konsentrasi PM10')
    ax.set_xlabel('Curah Hujan (RAIN)')
    ax.set_ylabel('Konsentrasi PM10')
    st.pyplot(fig)
    
    st.write("Curah hujan memiliki hubungan negatif dengan konsentrasi PM10, di mana semakin tinggi curah hujan, semakin rendah konsentrasi PM10. Konsentrasi tertinggi PM10 terjadi saat curah hujan mendekati nol, sementara pada curah hujan di atas 30 mm, kadar PM10 jarang melebihi 200 μg/m³. Hal ini menunjukkan bahwa hujan berperan dalam mengurangi PM10 melalui proses deposisi basah.")
    st.write("Sebaliknya, hubungan antara hujan dan PM2.5 lebih lemah, kemungkinan karena ukuran partikel yang lebih kecil membuatnya tidak mudah mengendap akibat hujan. Selain itu, peningkatan kelembapan akibat hujan dapat memicu reaksi kimia di atmosfer yang menghasilkan PM2.5 sekunder, yang bisa menjelaskan mengapa curah hujan tidak selalu menurunkan kadar PM2.5 secara signifikan.")
    
except FileNotFoundError:
    st.error("File data tidak ditemukan. Harap pastikan lokasi file benar.")
