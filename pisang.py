# Tangkap Pisang
# pip install pygame
# jalankan: python tangkap_pisang.py

import math
import random
import pygame

pygame.init()

# ubah angka di sini kalau mau mainnya lebih susah atau lebih santai
PELUANG_BOM = 0.3
KECEPATAN_MIN = 3
KECEPATAN_MAKS = 11
PENAMBAH_KECEPATAN = 0.08
NAMA_FILE_SKOR = "highscore.txt"

LEBAR, TINGGI = 600, 500
FPS = 60
NYAWA_AWAL = 3

LANGIT = (25, 30, 60)
HORIZON = (120, 82, 92)
PUTIH = (240, 240, 245)
KUNING_PISANG = (255, 225, 60)
GARIS_PISANG = (200, 150, 20)
COKELAT = (110, 75, 30)
COKELAT_MUDA = (196, 150, 104)
MERAH = (235, 70, 70)
BIRU = (70, 140, 240)
ABU_GELAP = (45, 45, 55)
ORANYE = (255, 150, 40)

layar = pygame.display.set_mode((LEBAR, TINGGI))
pygame.display.set_caption("Tangkap Pisang")
jam = pygame.time.Clock()

font_besar = pygame.font.SysFont("arial", 56, bold=True)
font_biasa = pygame.font.SysFont("arial", 24, bold=True)
font_kecil = pygame.font.SysFont("arial", 18)


def baca_skor_tertinggi():
    try:
        with open(NAMA_FILE_SKOR, encoding="utf-8") as file_skor:
            return max(0, int(file_skor.read().strip()))
    except (OSError, ValueError):
        # file belum ada atau isinya rusak, anggap belum punya rekor
        return 0


def simpan_skor_tertinggi(skor_baru):
    try:
        with open(NAMA_FILE_SKOR, "w", encoding="utf-8") as file_skor:
            file_skor.write(str(skor_baru))
    except OSError:
        # folder read-only? nggak apa-apa, yang penting game tetap jalan
        pass


keranjang = pygame.Rect(LEBAR // 2 - 45, TINGGI - 50, 90, 22)
benda = []
skor = 0
nyawa = NYAWA_AWAL
status = "main"
timer_muncul = 0
berjalan = True
skor_tertinggi = baca_skor_tertinggi()
rekor_baru = False
kilat_cepat = 0


def campur_warna(warna_awal, warna_akhir, posisi):
    return tuple(
        int(awal + (akhir - awal) * posisi)
        for awal, akhir in zip(warna_awal, warna_akhir)
    )


def mulai_ulang():
    global benda, skor, nyawa, status, timer_muncul, rekor_baru, kilat_cepat
    keranjang.centerx = LEBAR // 2
    benda = []
    skor = 0
    nyawa = NYAWA_AWAL
    status = "main"
    timer_muncul = 30
    rekor_baru = False
    kilat_cepat = 0


def buat_benda():
    jenis = "bom" if random.random() < PELUANG_BOM else "pisang"
    return {
        "x": random.randint(30, LEBAR - 30),
        "y": -20,
        "jenis": jenis,
        # makin tinggi skor makin cepat, tapi ada batasnya
        "kecepatan": min(
            random.uniform(KECEPATAN_MIN, 5) + skor * PENAMBAH_KECEPATAN,
            KECEPATAN_MAKS,
        ),
    }


def gambar_pisang(x, y):
    # dua busur ditumpuk biar ujung pisangnya menipis
    pusat_x, pusat_y = x, y - 16
    sisi_luar = []
    sisi_dalam = []

    for langkah in range(13):
        bagian = langkah / 12
        sudut = math.radians(25 + bagian * 130)
        tebal = 1 + 6 * math.sin(math.pi * bagian)
        titik_x = pusat_x + math.cos(sudut) * 18
        titik_y = pusat_y + math.sin(sudut) * 18
        sisi_luar.append((titik_x + math.cos(sudut) * tebal, titik_y + math.sin(sudut) * tebal))
        sisi_dalam.append((titik_x - math.cos(sudut) * tebal, titik_y - math.sin(sudut) * tebal))

    bentuk = sisi_luar + sisi_dalam[::-1]
    pygame.draw.polygon(layar, KUNING_PISANG, bentuk)
    pygame.draw.polygon(layar, GARIS_PISANG, bentuk, 2)
    pygame.draw.circle(layar, COKELAT, (int(sisi_luar[-1][0]), int(sisi_luar[-1][1])), 3)


def gambar_bom(x, y):
    pygame.draw.circle(layar, ABU_GELAP, (x, y), 14)
    pygame.draw.circle(layar, PUTIH, (x - 5, y - 5), 3)
    pygame.draw.line(layar, PUTIH, (x + 6, y - 11), (x + 12, y - 18), 2)
    pygame.draw.circle(layar, ORANYE, (x + 12, y - 18), 3)


def gambar_monyet(x, y):
    # y itu garis atas keranjang, jadi monyetnya nempel pas di situ
    pygame.draw.line(layar, COKELAT, (x - 16, y - 30), (x - 40, y - 3), 7)
    pygame.draw.line(layar, COKELAT, (x + 16, y - 30), (x + 40, y - 3), 7)

    pygame.draw.ellipse(layar, COKELAT, (x - 21, y - 42, 42, 38))
    pygame.draw.ellipse(layar, COKELAT_MUDA, (x - 13, y - 36, 26, 26))
    pygame.draw.ellipse(layar, (90, 60, 40), (x - 14, y - 8, 13, 7))
    pygame.draw.ellipse(layar, (90, 60, 40), (x + 1, y - 8, 13, 7))

    # telinga dulu, kepala digambar belakangan biar menutupinya
    pygame.draw.circle(layar, COKELAT, (x - 19, y - 55), 9)
    pygame.draw.circle(layar, COKELAT, (x + 19, y - 55), 9)
    pygame.draw.circle(layar, COKELAT_MUDA, (x - 19, y - 55), 4)
    pygame.draw.circle(layar, COKELAT_MUDA, (x + 19, y - 55), 4)

    pygame.draw.circle(layar, COKELAT, (x, y - 54), 20)
    pygame.draw.ellipse(layar, COKELAT_MUDA, (x - 14, y - 60, 28, 26))
    pygame.draw.circle(layar, ABU_GELAP, (x - 6, y - 53), 2)
    pygame.draw.circle(layar, ABU_GELAP, (x + 6, y - 53), 2)
    pygame.draw.circle(layar, (90, 60, 40), (x, y - 47), 2)
    pygame.draw.arc(layar, (90, 60, 40), (x - 8, y - 48, 16, 12), math.pi, 2 * math.pi, 2)


def gambar_pohon(permukaan, x, dasar_y, ukuran, warna_batang, warna_daun):
    lebar_batang = max(4, int(ukuran * 0.16))
    tinggi_batang = int(ukuran * 0.9)
    pygame.draw.rect(
        permukaan,
        warna_batang,
        (x - lebar_batang // 2, dasar_y - tinggi_batang, lebar_batang, tinggi_batang),
    )

    # kanopi dari tiga lingkaran, yang paling atas jadi puncaknya
    puncak = dasar_y - tinggi_batang
    pygame.draw.circle(permukaan, warna_daun, (x, puncak - int(ukuran * 0.18)), int(ukuran * 0.46))
    pygame.draw.circle(permukaan, warna_daun, (x - int(ukuran * 0.26), puncak + int(ukuran * 0.04)), int(ukuran * 0.34))
    pygame.draw.circle(permukaan, warna_daun, (x + int(ukuran * 0.26), puncak + int(ukuran * 0.04)), int(ukuran * 0.34))

    warna_sorot = campur_warna(warna_daun, PUTIH, 0.14)
    pygame.draw.circle(
        permukaan,
        warna_sorot,
        (x - int(ukuran * 0.12), puncak - int(ukuran * 0.24)),
        int(ukuran * 0.22),
    )


def gambar_hutan():
    permukaan = pygame.Surface((LEBAR, TINGGI))

    # langitnya gradien, makin ke bawah makin hangat
    for y in range(TINGGI):
        posisi = y / (TINGGI - 1)
        pygame.draw.line(permukaan, campur_warna(LANGIT, HORIZON, posisi), (0, y), (LEBAR, y))

    # bukit bertumpuk, yang depan lebih terang
    pygame.draw.ellipse(permukaan, (38, 66, 70), (-180, 245, 560, 300))
    pygame.draw.ellipse(permukaan, (44, 82, 72), (230, 270, 560, 280))
    pygame.draw.ellipse(permukaan, (50, 96, 78), (-60, 305, 520, 250))

    pygame.draw.rect(permukaan, (34, 86, 54), (0, TINGGI - 80, LEBAR, 80))
    pygame.draw.rect(permukaan, (26, 68, 44), (0, TINGGI - 80, LEBAR, 10))

    pohon_belakang = [
        (70, 372, 62),
        (300, 344, 46),
        (540, 374, 66),
    ]
    for x, dasar_y, ukuran in pohon_belakang:
        gambar_pohon(permukaan, x, dasar_y, ukuran, (52, 40, 28), (36, 74, 52))

    # pohon besar ditaruh di pinggir biar bagian tengah tetap lega
    pohon_depan = [
        (30, 420, 112),
        (95, 418, 86),
        (505, 418, 90),
        (572, 420, 120),
    ]
    for x, dasar_y, ukuran in pohon_depan:
        gambar_pohon(permukaan, x, dasar_y, ukuran, (78, 52, 30), (52, 118, 70))

    for x in (170, 240, 360, 430):
        pygame.draw.circle(permukaan, (40, 100, 62), (x, TINGGI - 78), 14)
        pygame.draw.circle(permukaan, (46, 112, 70), (x + 12, TINGGI - 74), 10)

    return permukaan


def gambar_hud():
    teks_skor = font_biasa.render(f"Pisang: {skor}", True, PUTIH)
    layar.blit(teks_skor, (15, 12))

    for nomor_nyawa in range(nyawa):
        pygame.draw.circle(layar, MERAH, (25 + nomor_nyawa * 28, 56), 10)

    teks_rekor = font_biasa.render(f"Tertinggi: {skor_tertinggi}", True, KUNING_PISANG)
    layar.blit(teks_rekor, (LEBAR - 15 - teks_rekor.get_width(), 12))

    if kilat_cepat > 0:
        teks_cepat = font_kecil.render("Makin cepat!", True, ORANYE)
        teks_cepat.set_alpha(min(255, kilat_cepat * 6))
        layar.blit(teks_cepat, (LEBAR // 2 - teks_cepat.get_width() // 2, 92))

    teks_info = font_kecil.render("Panah / A-D: gerak | R: ulang | ESC: keluar", True, (215, 220, 235))
    layar.blit(teks_info, (LEBAR // 2 - teks_info.get_width() // 2, TINGGI - 22))


def gambar_layar_akhir():
    lapisan = pygame.Surface((LEBAR, TINGGI), pygame.SRCALPHA)
    lapisan.fill((0, 0, 0, 175))
    layar.blit(lapisan, (0, 0))

    judul = font_besar.render("GAME OVER", True, MERAH)
    teks_skor = font_biasa.render(f"Pisang: {skor}", True, PUTIH)
    teks_rekor = font_biasa.render(f"Tertinggi: {skor_tertinggi}", True, KUNING_PISANG)
    teks_info = font_biasa.render("Tekan R untuk main lagi, ESC untuk keluar", True, PUTIH)

    layar.blit(judul, (LEBAR // 2 - judul.get_width() // 2, TINGGI // 2 - 110))
    layar.blit(teks_skor, (LEBAR // 2 - teks_skor.get_width() // 2, TINGGI // 2 - 35))
    layar.blit(teks_rekor, (LEBAR // 2 - teks_rekor.get_width() // 2, TINGGI // 2 - 2))

    if rekor_baru:
        teks_pujian = font_biasa.render("REKOR BARU!", True, ORANYE)
        layar.blit(teks_pujian, (LEBAR // 2 - teks_pujian.get_width() // 2, TINGGI // 2 + 32))

    layar.blit(teks_info, (LEBAR // 2 - teks_info.get_width() // 2, TINGGI // 2 + 85))


latar = gambar_hutan()

mulai_ulang()

while berjalan:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            berjalan = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                berjalan = False
            elif event.key == pygame.K_r:
                mulai_ulang()

    if status == "main":
        tombol = pygame.key.get_pressed()
        if tombol[pygame.K_LEFT] or tombol[pygame.K_a]:
            keranjang.x -= 8
        if tombol[pygame.K_RIGHT] or tombol[pygame.K_d]:
            keranjang.x += 8

        if keranjang.left < 0:
            keranjang.left = 0
        if keranjang.right > LEBAR:
            keranjang.right = LEBAR

        timer_muncul -= 1
        if timer_muncul <= 0:
            benda.append(buat_benda())
            timer_muncul = max(15, 40 - skor * 2)

        for barang in benda[:]:
            barang["y"] += barang["kecepatan"]
            kotak_benda = pygame.Rect(barang["x"] - 14, barang["y"] - 14, 28, 28)

            if kotak_benda.colliderect(keranjang):
                if barang["jenis"] == "pisang":
                    skor += 1
                    if skor > skor_tertinggi:
                        skor_tertinggi = skor
                        # langsung simpan, siapa tahu game ditutup paksa
                        simpan_skor_tertinggi(skor_tertinggi)
                        rekor_baru = True
                    if skor % 10 == 0:
                        kilat_cepat = 70
                else:
                    nyawa -= 1
                benda.remove(barang)
            elif barang["y"] > TINGGI + 20:
                benda.remove(barang)

        if kilat_cepat > 0:
            kilat_cepat -= 1

        if nyawa <= 0:
            status = "kalah"

    layar.blit(latar, (0, 0))

    for barang in benda:
        if barang["jenis"] == "pisang":
            gambar_pisang(barang["x"], barang["y"])
        else:
            gambar_bom(barang["x"], barang["y"])

    # monyet digambar dulu supaya keranjang terlihat menutupi bagian bawahnya
    gambar_monyet(keranjang.centerx, keranjang.top)
    pygame.draw.rect(layar, BIRU, keranjang, border_radius=8)
    pygame.draw.rect(layar, PUTIH, keranjang, 2, border_radius=8)

    gambar_hud()
    if status != "main":
        gambar_layar_akhir()

    pygame.display.flip()
    jam.tick(FPS)

pygame.quit()