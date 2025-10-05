# 📁 Portofolio Pribadi (Milligram CSS) - Versi Terbaru

![Portofolio Web](https://res.cloudinary.com/dzsqaauqn/image/upload/v1754627248/Screenshot_2025-08-08_111921_tdddvc.jpg)

## Deskripsi Proyek

Ini adalah proyek portofolio pribadi yang dibangun menggunakan **Python** dan framework web **Flask**. Tujuan utama proyek ini adalah untuk menampilkan pekerjaan dan kemampuan Anda sebagai pengembang web *full-stack*, dengan fitur dinamis seperti daftar proyek, blog, formulir kontak, ulasan, dan pesan pengguna. Proyek ini dirancang agar mudah dikelola, aman, dan siap untuk di-*deploy* ke platform modern seperti Vercel atau menggunakan Docker untuk kontainerisasi.

### Fitur Unggulan:
* **Sistem Manajemen Konten (CMS) Sederhana**: Dasbor admin yang dilindungi kata sandi untuk menambah, mengedit, dan menghapus proyek, postingan blog, serta ulasan.
* **Database NoSQL**: Menggunakan MongoDB Atlas untuk penyimpanan data proyek, blog, kontak, pesan, dan ulasan.
* **Penyimpanan Media Cloud**: Integrasi Cloudinary untuk mengelola gambar proyek dengan aman dan cepat.
* **Optimasi SEO**: Dilengkapi dengan `sitemap.xml` dan `robots.txt` dinamis untuk meningkatkan visibilitas di mesin pencari.
* **Pengalaman Pengguna (UX) yang Baik**: Mode gelap/terang, desain responsif, paginasi untuk proyek dan pesan, serta tombol "Scroll Up".
* **Otomatisasi Email**: Flask-Mail untuk mengirim notifikasi email dari formulir kontak.
* **Fitur Tambahan**: Halaman tools, services, reviews publik, dan manajemen pesan kontak.
* **Keamanan**: Hashing kata sandi admin menggunakan Werkzeug, serta Flask-Login untuk autentikasi.
* **Kontainerisasi**: Dukungan Docker dan Nginx untuk deployment produksi yang skalabel.

---

## Tumpukan Teknologi
* **Bahasa Pemrograman**: Python 3.12
* **Framework Backend**: Flask
* **Templating Engine**: Jinja2
* **Styling**: Milligram.css (kerangka kerja CSS minimalis), CSS kustom
* **Interaksi Frontend**: JavaScript kustom
* **Database**: MongoDB (melalui PyMongo)
* **Penyimpanan Media**: Cloudinary
* **Email**: Flask-Mail
* **Autentikasi**: Flask-Login
* **Deployment**: Gunicorn (untuk produksi), Vercel, Docker, Nginx
* **Lainnya**: `python-dotenv` untuk variabel lingkungan, `Flask-PyMongo`, `bidict` untuk SocketIO (jika diperlukan di masa depan)

---

## Struktur Direktori
```
📦 flask-docker-nginx
┣ 📂 templates/
┃ ┣ 📜 admin_blog_dashboard.html
┃ ┣ 📜 admin_dashboard.html
┃ ┣ 📜 admin_login.html
┃ ┣ 📜 admin_reviews.html
┃ ┣ 📜 add_blog.html
┃ ┣ 📜 add_project.html
┃ ┣ 📜 add_review.html
┃ ┣ 📜 edit_blog.html
┃ ┣ 📜 edit_project.html
┃ ┣ 📜 about.html
┃ ┣ 📜 base.html
┃ ┣ 📜 blog_post.html
┃ ┣ 📜 blog.html
┃ ┣ 📜 contact.html
┃ ┣ 📜 index.html
┃ ┣ 📜 message_detail.html
┃ ┣ 📜 messages.html
┃ ┣ 📜 projects.html
┃ ┣ 📜 reviews.html
┃ ┣ 📜 services.html
┃ ┣ 📜 tools.html
┃ ┣ 📜 robots.txt (template)
┃ ┗ 📜 sitemap.xml (template)
┣ 📂 static/
┃ ┣ 📂 css/
┃ ┃ ┣ 📜 custom.css
┃ ┃ ┗ 📜 milligram.css
┃ ┗ 📂 js/
┃   ┗ 📜 custom.js
┣ 📜 .env
┣ 📜 .python-version
┣ 📜 app.py
┣ 📜 docker-compose.yml
┣ 📜 Dockerfile
┣ 📜 nginx.conf
┣ 📜 README.md
┣ 📜 requirements.txt
┗ 📜 vercel.json
```

---

## Persiapan dan Instalasi

### 1. Kloning Repositori
```bash
git clone https://github.com/IshikawaUta/flask-docker-nginx
cd flask-docker-nginx
```

### 2. Buat Virtual Environment
Pastikan Anda berada di direktori proyek, lalu jalankan perintah berikut:
```bash
python -m venv venv
```
Untuk mengaktifkan virtual environment:

* **Windows**: `venv\Scripts\activate`
* **macOS/Linux**: `source venv/bin/activate`

### 3. Instal Ketergantungan
Instal semua pustaka yang diperlukan dari file `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Variabel Lingkungan
Buat file `.env` di direktori utama proyek dan tambahkan konfigurasi berikut:
```
MONGO_URI=<URI_MONGODB_ATLAS_ANDA>
FLASK_SECRET_KEY=<KUNCI_RAHASIA_FLASK_ANDA>
CLOUDINARY_CLOUD_NAME=<NAMA_CLOUD_CLOUDINARY>
CLOUDINARY_API_KEY=<API_KEY_CLOUDINARY>
CLOUDINARY_API_SECRET=<API_SECRET_CLOUDINARY>
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=<EMAIL_PENGIRIM_ANDA>
MAIL_PASSWORD=<KATA_SANDI_EMAIL_ANDA>
MAIL_DEFAULT_SENDER=<EMAIL_DEFAULT_ANDA>
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=<HASH_KATA_SANDI_ADMIN>
```
**Catatan**: Gunakan `werkzeug.security.generate_password_hash('password_anda')` untuk membuat hash kata sandi admin.

### 5. Menjalankan Proyek Secara Lokal
Setelah semua persiapan selesai, Anda dapat menjalankan aplikasi Flask:
```bash
flask run
```
Aplikasi akan berjalan di `http://127.0.0.1:5000`.

---

## Deployment ke Vercel
Proyek ini telah dikonfigurasi untuk di-*deploy* dengan mudah menggunakan Vercel. File `vercel.json` sudah disiapkan untuk mengarahkan semua rute ke `app.py`. 

1. Sambungkan repositori Git Anda ke Vercel.
2. Tambahkan variabel lingkungan dari `.env` ke pengaturan Vercel.
3. Vercel akan otomatis mendeteksi dan melakukan deployment.

---

## Deployment dengan Docker
Proyek ini mendukung kontainerisasi menggunakan Docker untuk lingkungan produksi. File `Dockerfile`, `docker-compose.yml`, dan `nginx.conf` sudah disediakan.

### Persyaratan:
- Instal Docker dan Docker Compose.

### Langkah-langkah:
1. Bangun dan jalankan kontainer:
   ```bash:disable-run
   docker-compose up -d --build
   ```
2. Aplikasi akan tersedia di `http://localhost:80`.
3. Untuk produksi, sesuaikan `nginx.conf` dan variabel lingkungan di `.env`.

**Catatan**: Pastikan `.env` dimuat dengan benar di Docker. Gunakan `restart: always` untuk ketahanan.

---

## Kontribusi
Jika Anda ingin berkontribusi, silakan fork repositori ini dan buat pull request. Pastikan untuk mengikuti standar coding Python (PEP 8).

## Lisensi
Proyek ini dilisensikan di bawah MIT License. Lihat file LICENSE untuk detail lebih lanjut.

Terima kasih telah mengunjungi proyek ini! Jika ada pertanyaan, hubungi melalui formulir kontak di situs. 🚀