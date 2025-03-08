# Dashboard Laporan Cuaca

## Deskripsi

Dashboard ini merupakan aplikasi berbasis Streamlit untuk menganalisis dan memvisualisasikan data kualitas udara serta faktor cuaca seperti suhu dan curah hujan. Dashboard menampilkan grafik tren polusi udara, analisis pengaruh arah angin terhadap polutan, serta visualisasi geospasial dengan peta interaktif.

## Fitur

- **Grafik Tren Polusi Udara**: Menampilkan rata-rata konsentrasi polutan per bulan.
- **Grafik Suhu dan Curah Hujan**: Visualisasi rata-rata suhu dan total curah hujan per bulan.
- **Peta Interaktif**: Menampilkan kualitas udara berdasarkan lokasi stasiun pemantauan menggunakan peta Folium.
- **Analisis Arah Angin**: Menunjukkan bagaimana arah angin mempengaruhi konsentrasi polutan tertentu.
- **Analisis Curah Hujan**: Menunjukkan dampak curah hujan terhadap konsentrasi PM2.5 dan PM10.

## Instalasi

### 1. Clone Repository

```sh
git clone <repository-url>
cd <nama-folder-proyek>
```

### 2. Install Dependencies

```sh
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi

```sh
streamlit run dashboard.py
```

## Struktur Folder

```
proyek_akhir/
│── dashboard/
│   ├── dashboard.py  # Kode utama Streamlit
│   ├── cleaned_air_quality_data.csv  # Dataset yang digunakan
│── requirements.txt  # Daftar dependencies
│── README.md  # Dokumentasi proyek
```

## Dataset

Dataset yang digunakan adalah **cleaned_air_quality_data.csv**, yang berisi data kualitas udara dan parameter cuaca seperti suhu, curah hujan, dan arah angin. Data ini harus ditempatkan di dalam folder `dashboard/` agar aplikasi dapat berjalan dengan baik.

## Teknologi yang Digunakan

- **Python** (Pandas, NumPy, Matplotlib, Seaborn, Folium)
- **Streamlit** (Untuk membuat dashboard interaktif)
- **Folium** (Untuk peta interaktif)

## Catatan

- Pastikan dataset sudah tersedia di dalam folder `dashboard/` sebelum menjalankan aplikasi.
- Jika ada masalah terkait dependencies, gunakan `pip install -r requirements.txt` untuk memastikan semua pustaka terinstal dengan benar.

## Kontributor

- **Refa Muhammad** - Mahasiswa Teknik Informatika, UIN Bandung

---

🚀 Selamat mencoba dan semoga bermanfaat!
