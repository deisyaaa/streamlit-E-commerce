# E-Commerce Public Dataset Dashboard 🛒

Proyek ini berisi analisis data pada E-Commerce Public Dataset dan *dashboard* interaktif yang dibuat menggunakan Streamlit

## Setup Environment

Sangat disarankan untuk menggunakan **Virtual Environment** agar versi *library* yang diinstal tidak berbenturan dengan proyek lain di komputer Anda. Anda bisa memilih salah satu dari dua cara di bawah ini:

### Cara 1: Menggunakan Venv (Bawaan Python)
1. Buka terminal/command prompt.
2. Buat virtual environment baru:
   ```bash
   python -m venv env
   ```
3. Aktifkan virtual environment:
   - Untuk **Windows**:
     ```bash
     .\env\Scripts\activate
     ```
   - Untuk **Mac/Linux**:
     ```bash
     source env/bin/activate
     ```
4. Install semua *library* pendukung:
   ```bash
   pip install -r requirements.txt
   ```

### Cara 2: Menggunakan Anaconda
1. Buka Anaconda Prompt.
2. Buat environment baru:
   ```bash
   conda create --name main-ds python=3.9
   ```
3. Aktifkan environment:
   ```bash
   conda activate main-ds
   ```
4. Install semua *library* pendukung:
   ```bash
   pip install -r requirements.txt
   ```

## Run Streamlit App

Setelah *environment* aktif dan semua *library* terinstal, jalankan perintah berikut untuk membuka dashboard:

```bash
cd dashboard
streamlit run dashboard.py
```