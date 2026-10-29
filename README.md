# Tangkap Pisang 🍌

Game arcade 2D santai berbasis Python dan Pygame. Di game ini, kamu mengendalikan keranjang (yang dipegang sama monyet) di bagian bawah layar untuk menangkap pisang dan item spesial yang berjatuhan dari langit sambil menghindari bom.

---

## 1. Deskripsi Singkat

**Tangkap Pisang** adalah script game interaktif sederhana yang berjalan pada frame rate stabil 60 FPS. Tujuan utamanya adalah mengumpulkan skor setinggi mungkin, bertahan hidup dari ledakan bom, dan memecahkan rekor skor tertinggi (*high score*) yang tersimpan secara lokal.

---

## 2. Fitur Utama

Berdasarkan isi kode logika di dalam `tangkap_pisang.py`, berikut fitur-fitur yang ada:

- **Pisang Biasa**: Item standar yang menambah **+1 skor**.
- **Pisang Emas**: Item langka dengan visual kelap-kelip emas yang memberi **poin ganda (+2 skor)**.
- **Item Hati**: Menambah **+1 nyawa** (maksimal 5 nyawa). Kalau nyawa sudah penuh, item ini otomatis ngasih bonus **+1 skor**.
- **Power-up Shield**: Mengaktifkan perisai pelindung selama 5 detik (300 frame). Saat perisai aktif, keranjang dilindungi aura gelembung cyan dan **kebal dari ledakan bom**.
- **Bom Bahaya**: Mengurangi **1 nyawa** jika terkena keranjang. Jika perisai pelindung sedang aktif, bom bakal tertahan tanpa mengurangi nyawa.
- **Sistem Pause [P]**: Game bisa dihentikan sementara kapan saja dengan menekan tombol **P**, dan dilanjutkan kembali dengan tombol yang sama.
- **Tingkat Kesulitan Bertahap**: Makin banyak pisang yang kamu kumpulkan, kecepatan jatuh item makin bertambah (`SPEED_BOOST = 0.08`) dan jeda kemunculan item makin rapat.
- **Penyimpanan Skor Tertinggi (High Score)**: Rekor skor disimpan otomatis ke file teks `highscore.txt`, jadi rekor kamu nggak bakal hilang walau game ditutup.
- **Grafis Murni Pygame Draw**: Semua elemen visual (hutan, pohon, monyet, keranjang kayu, pisang, hati, aura perisai) digambar langsung lewat koordinat matematika Pygame tanpa membutuhkan aset gambar eksternal.

---

## 3. Prasyarat (Prerequisites)

Sebelum menjalankan game, pastikan komputer kamu sudah terpasang:

- **Python**: Versi 3.8 ke atas (direkomendasikan Python 3.10 atau yang lebih baru).
- **Library Pygame**:
  ```bash
  pip install pygame
  ```
  *(Bisa juga menggunakan `pygame-ce` jika kamu memakai Pygame Community Edition).*
- **OS**: Windows, macOS, atau Linux yang mendukung tampilan GUI (layar desktop).

---

## 4. Instalasi (Installation)

Ikuti langkah-langkah simpel berikut untuk menyiapkan environment:

1. **Buka Terminal / Command Prompt**:
   Masuk ke folder proyek tempat file game berada:
   ```bash
   cd "d:\ALL CODE\semester3\codingcuy\cobasendiri\project\tangkep_pisang"
   ```

2. **Buat & Aktifkan Virtual Environment (Opsional tapi disarankan)**:
   - Di Windows:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - Di Linux / macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependensi**:
   ```bash
   pip install pygame
   ```

---

## 5. Cara Penggunaan (Usage)

### Menjalankan Game

Jalankan perintah ini di terminal:
```bash
python tangkap_pisang.py
```

Jendela game berukuran **600x500 piksel** akan terbuka langsung di layarmu.

### Kontrol Permainan

| Tombol Keyboard | Aksi |
| :--- | :--- |
| **Panah Kiri** / **A** | Menggerakkan keranjang ke arah kiri |
| **Panah Kanan** / **D** | Menggerakkan keranjang ke arah kanan |
| **P** | Menjeda permainan (*Pause*) / Melanjutkan kembali (*Resume*) |
| **R** | Mengulang permainan dari awal (*Restart*) |
| **ESC** | Menutup dan keluar dari game |

---

## 6. Penjelasan Kode & Struktur (Code Explanation & Structure)

Kode game disusun secara terstruktur dengan pendekatan OOP (*Object-Oriented Programming*) agar logikanya rapi dan mudah dimodifikasi.

### Struktur Penyusunan File (Dari Atas ke Bawah)

1. **Konfigurasi & Konstanta (Baris 1–46)**:
   - Inisialisasi awal Pygame (`pygame.init()`).
   - Penentuan parameter game seperti kecepatan jatuh (`SPEED_MIN`, `SPEED_MAX`, `SPEED_BOOST`), nyawa (`NYAWA_AWAL`, `NYAWA_MAX`), durasi perisai (`DURASI_SHIELD`), dimensi layar (`600x500`), dan target 60 FPS.
   - Definisi palet warna RGB (langit, kayu keranjang, monyet, emas, hati, shield) serta fungsi `campur_warna()` untuk efek gradasi warna langit.

2. **Kelas-Kelas Item Benda Jatuh (Baris 49–185)**:
   - `Item`: Kelas induk (*base class*) yang menyimpan koordinat `x`, `y`, `speed`, radius tabrakan, logika pergerakan `update()`, dan deteksi batas kotak `rect()`.
   - `Pisang`: Subclass untuk pisang biasa. Menggambar pisang lengkung kuning dan memberi +1 poin saat ditangkap.
   - `PisangEmas`: Subclass pisang bernilai ganda (+2 poin) dengan animasi kelap-kelip emas.
   - `Hati`: Subclass item nyawa berbentuk hati merah untuk memulihkan nyawa pemain.
   - `Shield`: Subclass item pelindung cyan yang mengaktifkan perisai keranjang.
   - `Bom`: Subclass bom abu-abu gelap dengan sumbu menyala. Mengurangi nyawa jika keranjang tidak terlindungi perisai.

3. **Kelas Keranjang / Pemain (Baris 187–263)**:
   - `Keranjang`: Mengelola posisi kotak keranjang kayu, mendeteksi input tombol keyboard kiri/kanan, membatasi keranjang agar tidak keluar dari tepi layar, menghitung mundur durasi perisai pelindung, serta menggambar monyet, anyaman kayu cokelat, dan visual gelembung perisai.

4. **Generator Visual Latar Belakang (Baris 265–306)**:
   - `gambar_pohon()`: Menggambar batang dan kanopi daun pohon rimbun.
   - `buat_latar()`: Membuat satu bidang `Surface` pemandangan hutan lengkap (langit senja gradien, bukit bertumpuk, semak, dan deretan pohon). Fungsi ini dipanggil sekali saat startup agar rendering sangat ringan tanpa membebani kartu grafis.

5. **Kelas Utama Game (Baris 308–523)**:
   - `Game`: Pusat kontrol seluruh permainan.
     - `baca_skor()` & `simpan_skor()`: Membaca dan menyimpan file `highscore.txt`.
     - `reset()`: Mengembalikan kondisi skor, nyawa, posisi pemain, dan list item ke keadaan awal.
     - `spawn_benda()`: Menentukan jenis item baru yang muncul secara acak berdasarkan peluang probabilitas (bom ~24%, emas ~12%, hati ~6%, shield ~7%, pisang biasa ~51%).
     - `handle_input()`: Menangkap event tombol keyboard (ESC, P untuk pause, R untuk restart).
     - `update()`: Menggerakkan keranjang dan item yang jatuh, mendeteksi tabrakan keranjang dengan item (`colliderect`), serta memicu status kalah saat nyawa habis.
     - `gambar_hud()`, `gambar_pause()`, `gambar_game_over()`, & `gambar()`: Menampilkan semua elemen teks, ikon nyawa, hitung mundur shield, overlay pause, dan tampilan Game Over.
     - `run()`: Game loop utama yang memanggil siklus input -> update -> gambar -> clock tick 60 FPS.

6. **Titik Masuk Utama (Baris 525–527)**:
   - Blok `if __name__ == "__main__":` yang membuat objek `Game()` lalu memanggil method `run()`.

---

## 7. Penanganan Error (Troubleshooting)

Beberapa kendala yang mungkin kamu temui dan cara mengatasinya:

1. **`ModuleNotFoundError: No module named 'pygame'`**:
   - **Penyebab**: Library Pygame belum terpasang di environment Python kamu.
   - **Solusi**: Jalankan perintah `pip install pygame` di terminal. Jika menggunakan virtual environment, pastikan environment sudah aktif terlebih dahulu.

2. **File Skor Tidak Terbaca / Rusak (`highscore.txt`)**:
   - **Penyebab**: File belum ada, kosong, atau ada karakter non-angka yang tidak sengaja tertulis.
   - **Solusi**: Kode sudah dibekali proteksi `try-except (OSError, ValueError)`. Jika file tidak valid, game otomatis menganggap rekor adalah 0 tanpa terjadi crash.

3. **Game Berjalan Terlalu Cepat atau Patah-Patah**:
   - **Penyebab**: Nilai tick rate atau monitor refresh rate yang tidak sinkron.
   - **Solusi**: Di dalam kode, kecepatan frame dikunci stabil pada baris `self.jam.tick(FPS)` (60 FPS). Pastikan tidak ada aplikasi berat lain yang menyedot resource CPU secara ekstrem.

4. **Layar Game Tidak Muncul di Linux / Server Headless**:
   - **Penyebab**: Pygame memerlukan server display grafis (X11 / Wayland).
   - **Solusi**: Jalankan game pada lingkungan desktop normal, bukan terminal server murni tanpa antarmuka grafis.

---

## 8. Contoh Tampilan (Output)

Saat script dijalankan, kamu akan melihat:
- **Tampilan Utama**: Jendela berlatar pemandangan hutan senja. Di bagian bawah terdapat monyet lucu yang memegang keranjang anyaman kayu berwarna cokelat.
- **HUD Atas Layar**:
  - Pojok kiri atas: Teks skor berjalan (misal: `Pisang: 8`) dan ikon hati merah penunjuk sisa nyawa.
  - Pojok kanan atas: Rekor tertinggi yang pernah diraih (misal: `Tertinggi: 42`).
  - Efek Shield: Jika menangkap item shield, muncul teks hitung mundur berwarna cyan (misal: `SHIELD: 4s`) dan keranjang diselimuti aura pelindung berdenyut.
- **Tampilan Pause**: Layar meredup dengan teks kuning besar bertuliskan `PAUSED` dan panduan `Tekan [P] untuk lanjut main`.
- **Tampilan Game Over**: Saat ketiga nyawa habis, layar menghitam transparan dengan tulisan merah `GAME OVER`, skor akhir yang kamu peroleh, dan ucapan `REKOR BARU!` jika kamu berhasil melampaui rekor sebelumnya.

---

## 9. Lisensi

Proyek ini bersifat open-source dan bebas digunakan untuk keperluan belajar, modifikasi, maupun pengembangan tugas pribadi.

