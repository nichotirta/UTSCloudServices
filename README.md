# StokWarung
Aplikasi web sederhana untuk mencatat stok bahan warung dan menampilkan barang yang hampir habis.
dengan tujuan untuk membantu pemilik warung atau kantin mencatat stok bahan dan melihat barang yang hampir habis. Banyak warung kecil masih mencatat stok di buku atau mengandalkan ingatan, sehingga bahan sering baru disadari habis saat sedang dibutuhkan. Target penggunanya pemilik warung, kantin kampus, dan usaha makanan kecil.

Fitur inti(MVP): pengguna menambah barang lewat form (POST /items) dan melihat daftar barang yang stoknya sudah sama dengan atau di bawah batas minimum (GET /items/low). Ada juga GET /health untuk memeriksa status aplikasi dan database.
## Alasan Projek
Saya memilih projek ini karena masalahnya nyata dan sederhana, sehingga saya bisa fokus mempelajari containerization, bukan memperumit fitur. Projek ini juga melatih alur yang dipakai di dunia kerja: aplikasi multi-tier (web, backend, database) yang berjalan dalam container dengan Docker Compose, lengkap dengan healthcheck, volume untuk data, dan konfigurasi lewat environment variable.

## Arsitektur
Browser -> app (Flask + gunicorn, port 5000) -> db (PostgreSQL 16, named volume db_data), semua di network warung_net.

## Cara Menjalankan
git clone <https://github.com/nichotirta/UTSCloudServices>
cd <StokWarung>
cp .env.example .env
docker compose up -d --build
Buka http://localhost:5000
Opsional Adminer: docker compose --profile tools up -d (http://localhost:8080)

## Endpoint
GET /health, GET /items, GET /items/low, POST /items

## Artikel dan Video
Link demo: https://youtu.be/TAxW3vgPYKU
Link artikel: https://stokwarung.hashnode.dev/

## Sumber
Flask, psycopg2, gunicorn, image resmi python dan postgres.

## AI Usage Declaration
Alat: Claude.
Bagian yang dibantu: saran topik, alur kode app.py dan index.html, draf Dockerfile dan docker-compose.yml, debugging (indentasi, password database, port),
Contoh prompt:
1.berikan beberapa ide projek web atau AI berskala kecil dengan satu tabel database yang jarang dipilih mahasiswa.
2.contoh aplikasi Flask + PostgreSQL untuk mencatat stok barang, dengan endpoint GET /health, GET untuk daftar barang yang hampir habis, dan POST untuk menambah barang, lengkap dengan status code yang tepat.
3.appnya crash saat docker compose up,PS C:\Users\ASUS\Downloads\StokWarung\UTSCloudServices> docker compose logs app --tail 15
app-1  |   File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
app-1  |   File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
app-1  |   File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
app-1  |   File "<frozen importlib._bootstrap_external>", line 991, in exec_module
app-1  |   File "<frozen importlib._bootstrap_external>", line 1129, in get_code
app-1  |   File "<frozen importlib._bootstrap_external>", line 1059, in source_to_code
app-1  |   File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
app-1  |   File "/app/app.py", line 20
app-1  |     conn = get_conn()
app-1  |                      ^
app-1  | IndentationError: unindent does not match any outer indentation level
app-1  | [2026-11-09 09:56:03 +0000] [7] [INFO] Worker exiting (pid: 7)
app-1  | [2026-11-09 09:56:03 +0000] [1] [ERROR] Worker (pid:7) exited with code 3
app-1  | [2026-11-09 09:56:03 +0000] [1] [ERROR] Shutting down: Master 
apa penyebabnya dan bagaimana memperbaikinya?
