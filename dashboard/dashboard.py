import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import io

# Set judul dashboard
st.title("Dashboard Laporan Cuaca")

# Path file data
data_path = "cleaned_air_quality_data.csv"

# Cek apakah file data ada
try:
    df_combined = pd.read_csv(data_path)
    
    # Visualisasi dengan Seaborn
    st.subheader("Grafik Tren Polusi Udara")
    numeric_cols = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    df_combined.groupby("month")[numeric_cols].mean().plot(ax=ax)
    plt.xlabel("Bulan")
    plt.ylabel("Konsentrasi (µg/m³)")
    plt.title("Rata-rata Konsentrasi Polutan per Bulan")
    plt.legend(title="Polutan")
    st.pyplot(fig)
    
    # Grafik Temperatur
    st.subheader("Grafik Suhu dan Curah Hujan")
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()
    
    df_combined.groupby("month")["TEMP"].mean().plot(ax=ax1, color="tab:red", label="Suhu (°C)")
    df_combined.groupby("month")["RAIN"].sum().plot(ax=ax2, color="tab:blue", label="Curah Hujan (mm)", linestyle="dashed")
    
    ax1.set_xlabel("Bulan")
    ax1.set_ylabel("Suhu (°C)", color="tab:red")
    ax2.set_ylabel("Curah Hujan (mm)", color="tab:blue")
    plt.title("Rata-rata Suhu dan Curah Hujan per Bulan")
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")
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
    
    df_latest = df_combined[df_combined['year'] == df_combined['year'].max()].groupby('station').mean(numeric_only=True).reset_index()
    df_latest['latitude'] = df_latest['station'].map(lambda x: station_locations.get(x, [None, None])[0])
    df_latest['longitude'] = df_latest['station'].map(lambda x: station_locations.get(x, [None, None])[1])
    map_data = df_latest.dropna(subset=['latitude', 'longitude', 'PM2.5'])
    
    m = folium.Map(location=[39.9, 116.4], zoom_start=10)
    
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
    
    # Analisis Pengaruh Arah Angin terhadap Polusi
    st.subheader("Pengaruh Arah Angin terhadap Konsentrasi Polutan")
    num_cols = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    axes = axes.flatten()
    
    for i, col in enumerate(num_cols):
        mean_polutan_by_wd = df_combined.groupby('wd')[col].mean().reset_index()
        sns.barplot(x='wd', y=col, data=mean_polutan_by_wd, palette='viridis', ax=axes[i])
        axes[i].set_title(f'Rata-rata {col} Berdasarkan Arah Angin')
        axes[i].set_xlabel('Arah Angin (wd)')
        axes[i].set_ylabel(f'Rata-rata {col}')
        axes[i].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    st.pyplot(fig)

    st.write("**Kesimpulan:** Arah angin mempengaruhi penyebaran polutan. Polutan seperti PM2.5, PM10, SO2, NO2, dan CO lebih tinggi saat angin bertiup dari timur, sedangkan O3 cenderung lebih tinggi saat angin berasal dari selatan.")
    
    st.subheader("Pengaruh Curah Hujan terhadap Konsentrasi Polutan")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(x='RAIN', y='PM2.5', data=df_combined, scatter_kws={'alpha': 0.3}, line_kws={'color': 'red'}, ax=ax)
    plt.title('Hubungan Curah Hujan (RAIN) dan Konsentrasi PM2.5')
    st.pyplot(fig)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(x='RAIN', y='PM10', data=df_combined, scatter_kws={'alpha': 0.3}, line_kws={'color': 'blue'}, ax=ax)
    plt.title('Hubungan Curah Hujan (RAIN) dan Konsentrasi PM10')
    st.pyplot(fig)
    
    st.write("**Kesimpulan:** Curah hujan memiliki efek signifikan dalam menurunkan konsentrasi polutan PM10 dan PM2.5 di udara melalui proses deposisi basah.")
    
except FileNotFoundError:
    st.error("File data tidak ditemukan. Harap pastikan lokasi file benar.")