# Tangkap Pisang
# pip install pygame
# jalankan: python tangkap_pisang.py

import math
import random
import pygame

pygame.init()

# atur tingkat kesulitan di sini
SPEED_MIN = 3
SPEED_MAX = 11
SPEED_BOOST = 0.08
FILE_SKOR = "highscore.txt"

LEBAR, TINGGI = 600, 500
FPS = 60
NYAWA_AWAL = 3
NYAWA_MAX = 5
DURASI_SHIELD = 300  # sekitar 5 detik (pada 60 fps)

# palet warna
LANGIT = (25, 30, 60)
HORIZON = (120, 82, 92)
PUTIH = (240, 240, 245)
KUNING = (255, 225, 60)
GARIS_PISANG = (200, 150, 20)
EMAS = (255, 205, 20)
EMAS_TERANG = (255, 240, 120)
MERAH = (235, 70, 70)
MERAH_HATI = (245, 50, 75)
CYAN = (60, 220, 255)
ABU_GELAP = (45, 45, 55)
ORANYE = (255, 150, 40)

# warna keranjang kayu & monyet
COKELAT_KERANJANG = (150, 95, 45)
COKELAT_TUA = (85, 50, 25)
COKELAT_MUDA = (195, 140, 80)
COKELAT_MONYET = (110, 75, 30)
KULIT_MONYET = (196, 150, 104)


def campur_warna(c1, c2, pos):
    return tuple(int(a + (b - a) * pos) for a, b in zip(c1, c2))


class Item:
    def __init__(self, x, speed, jenis):
        self.x = x
        self.y = -20
        self.speed = speed
        self.jenis = jenis
        self.radius = 14

    def update(self):
        self.y += self.speed

    def rect(self):
        r = self.radius
        return pygame.Rect(self.x - r, self.y - r, r * 2, r * 2)

    def gambar(self, layar):
        pass

    def kena(self, game):
        pass


class Pisang(Item):
    def __init__(self, x, speed):
        super().__init__(x, speed, "pisang")

    def gambar(self, layar):
        # tumpuk dua busur biar ujungnya lancip
        cx, cy = self.x, self.y - 16
        luar, dalam = [], []
        for i in range(13):
            t = i / 12
            rad = math.radians(25 + t * 130)
            tebal = 1 + 6 * math.sin(math.pi * t)
            px = cx + math.cos(rad) * 18
            py = cy + math.sin(rad) * 18
            luar.append((px + math.cos(rad) * tebal, py + math.sin(rad) * tebal))
            dalam.append((px - math.cos(rad) * tebal, py - math.sin(rad) * tebal))

        bentuk = luar + dalam[::-1]
        pygame.draw.polygon(layar, KUNING, bentuk)
        pygame.draw.polygon(layar, GARIS_PISANG, bentuk, 2)
        pygame.draw.circle(layar, COKELAT_MONYET, (int(luar[-1][0]), int(luar[-1][1])), 3)

    def kena(self, game):
        game.tambah_skor(1)


class PisangEmas(Item):
    def __init__(self, x, speed):
        super().__init__(x, speed, "pisang_emas")
        self.tick = 0

    def update(self):
        super().update()
        self.tick += 1

    def gambar(self, layar):
        cx, cy = self.x, self.y - 16
        luar, dalam = [], []
        for i in range(13):
            t = i / 12
            rad = math.radians(25 + t * 130)
            tebal = 1.2 + 6.5 * math.sin(math.pi * t)
            px = cx + math.cos(rad) * 18
            py = cy + math.sin(rad) * 18
            luar.append((px + math.cos(rad) * tebal, py + math.sin(rad) * tebal))
            dalam.append((px - math.cos(rad) * tebal, py - math.sin(rad) * tebal))

        bentuk = luar + dalam[::-1]
        pygame.draw.polygon(layar, EMAS, bentuk)
        pygame.draw.polygon(layar, (190, 140, 0), bentuk, 2)
        pygame.draw.circle(layar, COKELAT_TUA, (int(luar[-1][0]), int(luar[-1][1])), 3)

        # efek kelap-kelip emas
        fase = (self.tick % 30) / 30.0
        r_kilau = int(2 + 2 * math.sin(fase * math.pi * 2))
        pygame.draw.circle(layar, EMAS_TERANG, (self.x - 4, self.y - 8), r_kilau)
        pygame.draw.circle(layar, PUTIH, (self.x + 6, self.y + 4), 2)

    def kena(self, game):
        game.tambah_skor(2)
        game.kasih_pesan("+2 PISANG EMAS!", EMAS)


class Hati(Item):
    def __init__(self, x, speed):
        super().__init__(x, speed, "hati")

    def gambar(self, layar):
        cx, cy = self.x, self.y
        pygame.draw.circle(layar, MERAH_HATI, (cx - 5, cy - 3), 6)
        pygame.draw.circle(layar, MERAH_HATI, (cx + 5, cy - 3), 6)
        pygame.draw.polygon(layar, MERAH_HATI, [(cx - 10, cy - 1), (cx + 10, cy - 1), (cx, cy + 10)])
        pygame.draw.circle(layar, PUTIH, (cx - 6, cy - 5), 2)

    def kena(self, game):
        if game.nyawa < NYAWA_MAX:
            game.nyawa += 1
            game.kasih_pesan("+1 NYAWA!", MERAH_HATI)
        else:
            game.tambah_skor(1)
            game.kasih_pesan("NYAWA FULL! (+1 Skor)", KUNING)


class Shield(Item):
    def __init__(self, x, speed):
        super().__init__(x, speed, "shield")

    def gambar(self, layar):
        cx, cy = self.x, self.y
        pygame.draw.circle(layar, CYAN, (cx, cy), 13)
        pygame.draw.circle(layar, (180, 245, 255), (cx, cy), 10)
        titik = [(cx - 5, cy - 6), (cx + 5, cy - 6), (cx + 5, cy), (cx, cy + 6), (cx - 5, cy)]
        pygame.draw.polygon(layar, (20, 100, 180), titik)

    def kena(self, game):
        game.keranjang.shield_timer = DURASI_SHIELD
        game.kasih_pesan("SHIELD AKTIF!", CYAN)


class Bom(Item):
    def __init__(self, x, speed):
        super().__init__(x, speed, "bom")

    def gambar(self, layar):
        pygame.draw.circle(layar, ABU_GELAP, (self.x, self.y), 14)
        pygame.draw.circle(layar, PUTIH, (self.x - 5, self.y - 5), 3)
        pygame.draw.line(layar, PUTIH, (self.x + 6, self.y - 11), (self.x + 12, self.y - 18), 2)
        pygame.draw.circle(layar, ORANYE, (self.x + 12, self.y - 18), 3)

    def kena(self, game):
        if game.keranjang.shield_aktif():
            game.kasih_pesan("BOM DITAHAN SHIELD!", CYAN)
        else:
            game.nyawa -= 1


class Keranjang:
    def __init__(self):
        self.rect = pygame.Rect(LEBAR // 2 - 45, TINGGI - 50, 90, 22)
        self.speed = 8
        self.shield_timer = 0
        self.tick_shield = 0

    def reset(self):
        self.rect.centerx = LEBAR // 2
        self.shield_timer = 0
        self.tick_shield = 0

    def shield_aktif(self):
        return self.shield_timer > 0

    def gerak(self, tombol):
        if tombol[pygame.K_LEFT] or tombol[pygame.K_a]:
            self.rect.x -= self.speed
        if tombol[pygame.K_RIGHT] or tombol[pygame.K_d]:
            self.rect.x += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LEBAR:
            self.rect.right = LEBAR

    def update(self):
        if self.shield_timer > 0:
            self.shield_timer -= 1
            self.tick_shield += 1

    def gambar_monyet(self, layar, x, y):
        # y itu pas di garis atas keranjang
        pygame.draw.line(layar, COKELAT_MONYET, (x - 16, y - 30), (x - 40, y - 3), 7)
        pygame.draw.line(layar, COKELAT_MONYET, (x + 16, y - 30), (x + 40, y - 3), 7)

        pygame.draw.ellipse(layar, COKELAT_MONYET, (x - 21, y - 42, 42, 38))
        pygame.draw.ellipse(layar, KULIT_MONYET, (x - 13, y - 36, 26, 26))
        pygame.draw.ellipse(layar, (90, 60, 40), (x - 14, y - 8, 13, 7))
        pygame.draw.ellipse(layar, (90, 60, 40), (x + 1, y - 8, 13, 7))

        pygame.draw.circle(layar, COKELAT_MONYET, (x - 19, y - 55), 9)
        pygame.draw.circle(layar, COKELAT_MONYET, (x + 19, y - 55), 9)
        pygame.draw.circle(layar, KULIT_MONYET, (x - 19, y - 55), 4)
        pygame.draw.circle(layar, KULIT_MONYET, (x + 19, y - 55), 4)

        pygame.draw.circle(layar, COKELAT_MONYET, (x, y - 54), 20)
        pygame.draw.ellipse(layar, KULIT_MONYET, (x - 14, y - 60, 28, 26))
        pygame.draw.circle(layar, ABU_GELAP, (x - 6, y - 53), 2)
        pygame.draw.circle(layar, ABU_GELAP, (x + 6, y - 53), 2)
        pygame.draw.circle(layar, (90, 60, 40), (x, y - 47), 2)
        pygame.draw.arc(layar, (90, 60, 40), (x - 8, y - 48, 16, 12), math.pi, 2 * math.pi, 2)

    def gambar(self, layar):
        self.gambar_monyet(layar, self.rect.centerx, self.rect.top)

        # keranjang kayu cokelat
        pygame.draw.rect(layar, COKELAT_KERANJANG, self.rect, border_radius=8)
        pygame.draw.rect(layar, COKELAT_TUA, self.rect, 2, border_radius=8)
        pygame.draw.line(layar, COKELAT_MUDA, (self.rect.left + 4, self.rect.top + 3), (self.rect.right - 4, self.rect.top + 3), 2)

        # motif anyaman kayu
        for gx in range(self.rect.left + 12, self.rect.right - 6, 14):
            pygame.draw.line(layar, COKELAT_TUA, (gx, self.rect.top + 5), (gx, self.rect.bottom - 4), 1)
        pygame.draw.line(layar, COKELAT_TUA, (self.rect.left + 4, self.rect.centery + 2), (self.rect.right - 4, self.rect.centery + 2), 1)

        # efek gelembung shield kalau lagi aktif
        if self.shield_aktif():
            denyut = math.sin(self.tick_shield * 0.15) * 3
            rad = int(58 + denyut)
            pos = (self.rect.centerx, self.rect.centery - 24)

            surf = pygame.Surface((rad * 2 + 10, rad * 2 + 10), pygame.SRCALPHA)
            pygame.draw.circle(surf, (60, 220, 255, 60), (rad + 5, rad + 5), rad)
            pygame.draw.circle(surf, (180, 245, 255, 180), (rad + 5, rad + 5), rad, 3)
            layar.blit(surf, (pos[0] - rad - 5, pos[1] - rad - 5))


def gambar_pohon(layar, x, dasar_y, ukuran, batang, daun):
    lebar_b = max(4, int(ukuran * 0.16))
    tinggi_b = int(ukuran * 0.9)
    pygame.draw.rect(layar, batang, (x - lebar_b // 2, dasar_y - tinggi_b, lebar_b, tinggi_b))

    puncak = dasar_y - tinggi_b
    pygame.draw.circle(layar, daun, (x, puncak - int(ukuran * 0.18)), int(ukuran * 0.46))
    pygame.draw.circle(layar, daun, (x - int(ukuran * 0.26), puncak + int(ukuran * 0.04)), int(ukuran * 0.34))
    pygame.draw.circle(layar, daun, (x + int(ukuran * 0.26), puncak + int(ukuran * 0.04)), int(ukuran * 0.34))
    pygame.draw.circle(layar, campur_warna(daun, PUTIH, 0.14), (x - int(ukuran * 0.12), puncak - int(ukuran * 0.24)), int(ukuran * 0.22))


def buat_latar():
    surf = pygame.Surface((LEBAR, TINGGI))

    # langit gradien
    for y in range(TINGGI):
        pos = y / (TINGGI - 1)
        pygame.draw.line(surf, campur_warna(LANGIT, HORIZON, pos), (0, y), (LEBAR, y))

    # bukit bertumpuk
    pygame.draw.ellipse(surf, (38, 66, 70), (-180, 245, 560, 300))
    pygame.draw.ellipse(surf, (44, 82, 72), (230, 270, 560, 280))
    pygame.draw.ellipse(surf, (50, 96, 78), (-60, 305, 520, 250))

    pygame.draw.rect(surf, (34, 86, 54), (0, TINGGI - 80, LEBAR, 80))
    pygame.draw.rect(surf, (26, 68, 44), (0, TINGGI - 80, LEBAR, 10))

    # pohon belakang
    for x, py, sz in [(70, 372, 62), (300, 344, 46), (540, 374, 66)]:
        gambar_pohon(surf, x, py, sz, (52, 40, 28), (36, 74, 52))

    # pohon depan di pinggir biar tengahnya lega
    for x, py, sz in [(30, 420, 112), (95, 418, 86), (505, 418, 90), (572, 420, 120)]:
        gambar_pohon(surf, x, py, sz, (78, 52, 30), (52, 118, 70))

    for x in (170, 240, 360, 430):
        pygame.draw.circle(surf, (40, 100, 62), (x, TINGGI - 78), 14)
        pygame.draw.circle(surf, (46, 112, 70), (x + 12, TINGGI - 74), 10)

    return surf


class Game:
    def __init__(self):
        self.layar = pygame.display.set_mode((LEBAR, TINGGI))
        pygame.display.set_caption("Tangkap Pisang")
        self.jam = pygame.time.Clock()

        self.font_besar = pygame.font.SysFont("arial", 54, bold=True)
        self.font_biasa = pygame.font.SysFont("arial", 24, bold=True)
        self.font_kecil = pygame.font.SysFont("arial", 18)

        self.latar = buat_latar()
        self.keranjang = Keranjang()
        self.benda = []

        self.skor = 0
        self.nyawa = NYAWA_AWAL
        self.status = "main"  # main, paused, kalah
        self.timer_spawn = 0
        self.jalan = True

        self.skor_tertinggi = self.baca_skor()
        self.rekor_baru = False
        self.kilat_cepat = 0

        self.pesan = ""
        self.warna_pesan = PUTIH
        self.timer_pesan = 0

    def baca_skor(self):
        try:
            with open(FILE_SKOR, encoding="utf-8") as f:
                return max(0, int(f.read().strip()))
        except (OSError, ValueError):
            return 0

    def simpan_skor(self, skor_baru):
        try:
            with open(FILE_SKOR, "w", encoding="utf-8") as f:
                f.write(str(skor_baru))
        except OSError:
            pass

    def reset(self):
        self.keranjang.reset()
        self.benda = []
        self.skor = 0
        self.nyawa = NYAWA_AWAL
        self.status = "main"
        self.timer_spawn = 30
        self.rekor_baru = False
        self.kilat_cepat = 0
        self.pesan = ""
        self.timer_pesan = 0

    def tambah_skor(self, n):
        self.skor += n
        if self.skor > self.skor_tertinggi:
            self.skor_tertinggi = self.skor
            self.simpan_skor(self.skor_tertinggi)
            self.rekor_baru = True
        if self.skor % 10 == 0:
            self.kilat_cepat = 70

    def kasih_pesan(self, teks, warna):
        self.pesan = teks
        self.warna_pesan = warna
        self.timer_pesan = 55

    def spawn_benda(self):
        pos_x = random.randint(30, LEBAR - 30)
        speed = min(random.uniform(SPEED_MIN, 5) + self.skor * SPEED_BOOST, SPEED_MAX)
        r = random.random()

        if r < 0.24:
            return Bom(pos_x, speed)
        if r < 0.36:
            return PisangEmas(pos_x, speed)
        if r < 0.42:
            return Hati(pos_x, speed)
        if r < 0.49:
            return Shield(pos_x, speed)
        return Pisang(pos_x, speed)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.jalan = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.jalan = False
                elif event.key == pygame.K_p:
                    if self.status == "main":
                        self.status = "paused"
                    elif self.status == "paused":
                        self.status = "main"
                elif event.key == pygame.K_r:
                    self.reset()

    def update(self):
        if self.status != "main":
            return

        tombol = pygame.key.get_pressed()
        self.keranjang.gerak(tombol)
        self.keranjang.update()

        self.timer_spawn -= 1
        if self.timer_spawn <= 0:
            self.benda.append(self.spawn_benda())
            self.timer_spawn = max(15, 40 - self.skor * 2)

        for b in self.benda[:]:
            b.update()
            if b.rect().colliderect(self.keranjang.rect):
                b.kena(self)
                self.benda.remove(b)
            elif b.y > TINGGI + 20:
                self.benda.remove(b)

        if self.kilat_cepat > 0:
            self.kilat_cepat -= 1

        if self.timer_pesan > 0:
            self.timer_pesan -= 1

        if self.nyawa <= 0:
            self.status = "kalah"

    def gambar_hud(self):
        teks_skor = self.font_biasa.render(f"Pisang: {self.skor}", True, PUTIH)
        self.layar.blit(teks_skor, (15, 12))

        # ikon nyawa
        for i in range(self.nyawa):
            cx = 25 + i * 26
            cy = 54
            pygame.draw.circle(self.layar, MERAH_HATI, (cx - 4, cy - 2), 6)
            pygame.draw.circle(self.layar, MERAH_HATI, (cx + 4, cy - 2), 6)
            pygame.draw.polygon(self.layar, MERAH_HATI, [(cx - 9, cy), (cx + 9, cy), (cx, cy + 9)])

        teks_rekor = self.font_biasa.render(f"Tertinggi: {self.skor_tertinggi}", True, KUNING)
        self.layar.blit(teks_rekor, (LEBAR - 15 - teks_rekor.get_width(), 12))

        if self.keranjang.shield_aktif():
            sisa_detik = (self.keranjang.shield_timer // FPS) + 1
            teks_shield = self.font_biasa.render(f"SHIELD: {sisa_detik}s", True, CYAN)
            self.layar.blit(teks_shield, (LEBAR - 15 - teks_shield.get_width(), 44))

        if self.timer_pesan > 0 and self.pesan:
            teks_popup = self.font_biasa.render(self.pesan, True, self.warna_pesan)
            self.layar.blit(teks_popup, (LEBAR // 2 - teks_popup.get_width() // 2, 54))

        if self.kilat_cepat > 0:
            teks_cepat = self.font_kecil.render("Makin cepat!", True, ORANYE)
            teks_cepat.set_alpha(min(255, self.kilat_cepat * 6))
            self.layar.blit(teks_cepat, (LEBAR // 2 - teks_cepat.get_width() // 2, 88))

        teks_bantuan = self.font_kecil.render("Panah / A-D: gerak | P: jeda | R: ulang | ESC: keluar", True, (215, 220, 235))
        self.layar.blit(teks_bantuan, (LEBAR // 2 - teks_bantuan.get_width() // 2, TINGGI - 22))

    def gambar_pause(self):
        lapisan = pygame.Surface((LEBAR, TINGGI), pygame.SRCALPHA)
        lapisan.fill((0, 0, 0, 160))
        self.layar.blit(lapisan, (0, 0))

        judul = self.font_besar.render("PAUSED", True, KUNING)
        sub = self.font_biasa.render("Tekan [P] untuk lanjut main", True, PUTIH)
        self.layar.blit(judul, (LEBAR // 2 - judul.get_width() // 2, TINGGI // 2 - 50))
        self.layar.blit(sub, (LEBAR // 2 - sub.get_width() // 2, TINGGI // 2 + 20))

    def gambar_game_over(self):
        lapisan = pygame.Surface((LEBAR, TINGGI), pygame.SRCALPHA)
        lapisan.fill((0, 0, 0, 175))
        self.layar.blit(lapisan, (0, 0))

        judul = self.font_besar.render("GAME OVER", True, MERAH)
        teks_skor = self.font_biasa.render(f"Pisang: {self.skor}", True, PUTIH)
        teks_rekor = self.font_biasa.render(f"Tertinggi: {self.skor_tertinggi}", True, KUNING)
        teks_info = self.font_biasa.render("Tekan R untuk main lagi, ESC untuk keluar", True, PUTIH)

        self.layar.blit(judul, (LEBAR // 2 - judul.get_width() // 2, TINGGI // 2 - 110))
        self.layar.blit(teks_skor, (LEBAR // 2 - teks_skor.get_width() // 2, TINGGI // 2 - 35))
        self.layar.blit(teks_rekor, (LEBAR // 2 - teks_rekor.get_width() // 2, TINGGI // 2 - 2))

        if self.rekor_baru:
            teks_rekor_baru = self.font_biasa.render("REKOR BARU!", True, ORANYE)
            self.layar.blit(teks_rekor_baru, (LEBAR // 2 - teks_rekor_baru.get_width() // 2, TINGGI // 2 + 32))

        self.layar.blit(teks_info, (LEBAR // 2 - teks_info.get_width() // 2, TINGGI // 2 + 85))

    def gambar(self):
        self.layar.blit(self.latar, (0, 0))

        for b in self.benda:
            b.gambar(self.layar)

        self.keranjang.gambar(self.layar)
        self.gambar_hud()

        if self.status == "paused":
            self.gambar_pause()
        elif self.status == "kalah":
            self.gambar_game_over()

        pygame.display.flip()

    def run(self):
        self.reset()
        while self.jalan:
            self.handle_input()
            self.update()
            self.gambar()
            self.jam.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
