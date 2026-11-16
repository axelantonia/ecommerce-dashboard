# Proyek Analisis Data: E-Commerce Public Dataset 

Proyek ini merupakan hasil analisis data pada **E-Commerce Public Dataset** (Olist) untuk menjawab pertanyaan bisnis terkait performa penjualan berdasarkan kota dan pengaruh ketepatan waktu pengiriman terhadap ulasan pelanggan, yang kemudian disajikan dalam bentuk dashboard interaktif menggunakan Streamlit.

## Struktur Direktori
- `dashboard/`: Berisi file utama aplikasi Streamlit (`dashboard.py`) dan dataset yang telah dibersihkan.
- `data/`: Berisi dataset mentah E-Commerce Public Dataset.
- `notebook.ipynb`: Berisi keseluruhan proses analisis data (Data Wrangling, EDA, hingga Visualisasi).
- `README.md`: Panduan dokumentasi proyek.
- `requirements.txt`: Daftar library beserta versinya yang digunakan dalam proyek.

## Setup Environment & Cara Menjalankan Dashboard Secara Lokal

1. **Clone repository atau ekstrak folder proyek ini**, lalu buka terminal/command prompt dan arahkan ke direktori utama proyek.

2. **Buat dan aktifkan virtual environment (opsional namun disarankan):**
   ```bash
   python -m venv venv
   # Untuk Windows:
   venv\Scripts\activate
   # Untuk macOS/Linux:
   source venv/bin/activate