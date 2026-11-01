# Sistem Manajemen Perpustakaan

Aplikasi desktop berbasis Python untuk mengelola koleksi buku perpustakaan. Aplikasi menyediakan antarmuka CustomTkinter, menyimpan data pada MySQL, dan menerapkan pola Model-View-Controller (MVC). Pengguna masuk melalui halaman login; hak akses admin dan anggota diatur berdasarkan role pada akun.

## Struktur proyek

```text
Modul 3/
├── config/
│   └── database.py          # Pengaturan koneksi MySQL
├── controllers/
│   ├── auth_controller.py   # Alur login
│   ├── buku_controller.py   # Alur fitur buku
│   └── anggota_controller.py
├── models/
│   ├── user_model.py        # Autentikasi dan data pengguna
│   ├── buku_model.py        # Operasi data buku
│   └── anggota_model.py     # Operasi data anggota
├── views/
│   ├── login_view.py        # Antarmuka login
│   ├── buku_view.py         # Antarmuka koleksi buku
│   └── anggota_view.py      # Antarmuka anggota
├── test/                    # Unit test pytest
├── .github/workflows/       # Workflow GitHub Actions
├── main.py                  # Titik masuk aplikasi
└── requirements.txt         # Dependensi Python
```

Pada pola MVC, **Model** berisi logika data dan komunikasi dengan basis data, **View** mengatur komponen antarmuka, dan **Controller** menghubungkan aksi pengguna dengan Model serta View. `main.py` memulai aplikasi melalui `AuthController`.

## Persyaratan

- Python 3.11 atau versi yang kompatibel dengan dependensi proyek
- MySQL Server, misalnya yang disertakan dalam XAMPP
- Git (opsional, jika proyek akan diambil dari GitHub)

## Instalasi

Buka Terminal, lalu masuk ke direktori proyek. Buat dan aktifkan virtual environment, kemudian pasang dependensi:

```bash
cd "/Applications/XAMPP/xamppfiles/htdocs/Modul 3"
python3 -m venv env
source env/bin/activate
python -m pip install -r requirements.txt
```

Pada Windows, aktifkan environment dengan:

```powershell
env\Scripts\activate
```

## Konfigurasi basis data MySQL

1. Jalankan MySQL melalui XAMPP.
2. Buat basis data dan tabel yang digunakan aplikasi. Contoh skema:

   ```sql
   CREATE DATABASE IF NOT EXISTS perpustakaan;
   USE perpustakaan;

   CREATE TABLE IF NOT EXISTS books (
       id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
       isbn VARCHAR(20) NULL,
       title VARCHAR(255) NOT NULL,
       author VARCHAR(150) NOT NULL,
       category VARCHAR(100) NOT NULL,
       publication_year SMALLINT UNSIGNED NULL,
       stock INT UNSIGNED NOT NULL DEFAULT 0
   );

   CREATE TABLE IF NOT EXISTS users (
       id_user INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(100) NOT NULL UNIQUE,
       password CHAR(64) NOT NULL,
       role VARCHAR(20) NOT NULL DEFAULT 'anggota'
   );
   ```

3. Periksa `config/database.py`. Sesuaikan `host`, `db_name`, `username`, dan `password` dengan konfigurasi MySQL lokal. Konfigurasi bawaan proyek menggunakan host `localhost`, basis data `perpustakaan`, dan pengguna `root`; sesuaikan password jika MySQL Anda menggunakannya.
4. Siapkan akun pengguna pada tabel `users`. Password harus disimpan sebagai hash SHA-256 sesuai mekanisme di `models/user_model.py`, bukan sebagai teks biasa. Role yang dipakai aplikasi adalah `admin` atau `anggota`.

## Menjalankan aplikasi

Pastikan virtual environment aktif dan MySQL menyala, lalu jalankan dari root proyek:

```bash
python main.py
```

Aplikasi akan menampilkan jendela login. Setelah kredensial diverifikasi, tampilan dan fitur yang tersedia mengikuti role pengguna.

## Pemeriksaan kode dan pengujian

Jalankan pemeriksaan Flake8 dan unit test dari root proyek:

```bash
python -m flake8 models/ controllers/ --count --select=E9,F63,F7,F82 --show-source --statistics
python -m pytest -v
```

GitHub Actions menjalankan pemeriksaan tersebut otomatis pada push atau pull request ke branch `main`.

## Pemaketan aplikasi

PyInstaller dapat digunakan untuk membuat aplikasi mandiri pada sistem operasi yang menjalankan proses build. macOS menghasilkan aplikasi macOS; untuk menghasilkan `.exe` Windows, build perlu dijalankan pada Windows. Hasil build disimpan di `dist/`, sedangkan `build/` dan `dist/` sebaiknya tetap diabaikan oleh Git.
