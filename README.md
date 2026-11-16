# Proyek Analisis Data: E-Commerce Public Dataset

Proyek ini merupakan hasil analisis data menggunakan **E-Commerce Public Dataset (Olist)**. Analisis dilakukan untuk menjawab pertanyaan bisnis terkait performa penjualan berdasarkan wilayah pelanggan serta pengaruh ketepatan waktu pengiriman terhadap ulasan pelanggan.

Hasil analisis disajikan dalam bentuk dashboard interaktif menggunakan Streamlit.

## Struktur Direktori

```text
submission/
├── dashboard/
│   ├── main_data.csv
│   └── dashboard.py
├── data/
│   ├── data_1.csv
│   └── data_2.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

Keterangan:
- `dashboard/`: Berisi file aplikasi Streamlit (`dashboard.py`) dan dataset yang telah dibersihkan (`main_data.csv`).
- `data/`: Berisi dataset mentah yang digunakan dalam proses analisis.
- `notebook.ipynb`: Berisi proses analisis data, mulai dari Data Wrangling, Exploratory Data Analysis (EDA), hingga visualisasi.
- `requirements.txt`: Berisi daftar library Python beserta versi yang dibutuhkan.
- `url.txt`: Berisi tautan untuk mengakses dashboard secara online.

## Persiapan Environment

Sebelum menjalankan proyek, pastikan Python sudah terinstal pada komputer. Selanjutnya, clone repository atau ekstrak ZIP proyek, kemudian buka terminal pada direktori utama proyek (`submission/`), yaitu direktori yang berisi file `requirements.txt`.

### 1. Membuat Virtual Environment

Buat virtual environment dengan menjalankan perintah berikut:

```bash
python -m venv venv
```

### 2. Mengaktifkan Virtual Environment

**Windows (Command Prompt):**

```bash
venv\Scripts\activate
```

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

Setelah berhasil diaktifkan, nama environment (`venv`) akan muncul pada terminal.

## Instalasi Dependensi

Pastikan terminal masih berada di direktori utama proyek (`submission/`) dan virtual environment sudah aktif.

Instal seluruh library yang dibutuhkan menggunakan perintah:

```bash
pip install -r requirements.txt
```

## Menjalankan Dashboard

Setelah seluruh dependensi berhasil diinstal, jalankan aplikasi Streamlit menggunakan perintah berikut dari direktori utama proyek:

```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka secara otomatis melalui browser. Jika tidak terbuka secara otomatis, salin alamat lokal yang ditampilkan pada terminal ke browser.

## Dataset

Dataset yang digunakan merupakan E-Commerce Public Dataset dari Olist. Dataset mentah disimpan di dalam direktori `data/`, sedangkan dataset yang telah melalui proses pengolahan dan digunakan oleh dashboard disimpan di dalam direktori `dashboard/` dengan nama `main_data.csv`.

Dashboard membaca dataset yang telah dibersihkan menggunakan path:

```python
dashboard/main_data.csv
```

Pastikan file tersebut tersedia sebelum menjalankan aplikasi.

## Fitur Dashboard

Dashboard menyediakan beberapa visualisasi dan informasi interaktif, yaitu:

1. **Daily Orders**: Menampilkan jumlah pesanan dan total pendapatan berdasarkan rentang waktu yang dipilih.
2. **Top 5 States by Order & Revenue**: Menampilkan lima wilayah dengan jumlah pesanan dan pendapatan tertinggi.
3. **Delivery Delay Impact on Review Score**: Membandingkan rata-rata skor ulasan dan komposisi ulasan berdasarkan status pengiriman.
4. **Delivery Delay Clustering Analysis**: Menampilkan rata-rata skor ulasan berdasarkan kategori keterlambatan pengiriman.

Pengguna dapat memilih rentang waktu melalui filter pada sidebar untuk menyesuaikan data yang ditampilkan pada dashboard.

## Dashboard Online

Dashboard juga dapat diakses secara online melalui tautan yang tercantum pada file `url.txt`.