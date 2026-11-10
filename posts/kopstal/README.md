# Kopstal (2026) · Reel'ler

Her eser için iki ayrı video: **süreç** (kamera sabit, aşama fotoğrafları beyaz alana tam
sığıyor) ve **detay** (yakın planlar, her plan tek eksende ve kesintisiz hareketli, sonda
merkezden zoom-out ile eser beyaz alanda 2 sn). Kurallar: `.claude/instagram/voice.md`.
Üretim: `python3 tools/render.py <klasör>/spec.json`, kontrol: `python3 tools/review.py <klasör>`.

| eser | süreç | detay |
| --- | --- | --- |
| Painstaking | yok: repoda aşama fotoğrafı yok | `painstaking-details/` |
| Angora Mergvs | `angora-mergvs-process/`, 3D model: `angora-mergvs-model/` | `angora-mergvs-details/` |
| Gxd is AFK, We banned it | `gxd-is-afk-we-banned-it-process/` | `gxd-is-afk-we-banned-it-details/` |
| sept neuf | `sept-neuf-process/`, boyama kaydı: `sept-neuf-footage/` | `sept-neuf-details/` |
| 7 fam board game | `7-fam-board-game-process/` (14 aşama), boyama kaydı: `7-fam-board-game-footage/` | `7-fam-board-game-details/` |
| Virgil on Virtual Cage (final_final-finalV9) | `virgil-on-virtual-cage-final-final-finalv9-process/` (12 aşama; `00` Leonardo referansı, çıkarıldı) | `virgil-on-virtual-cage-final-final-finalv9-details/` |
| gary grills cooper | `gary-grills-cooper-process/` | `gary-grills-cooper-details/` |
| walls of perception | `walls-of-perception-process/` (5 aşama) | `walls-of-perception-details/` |
| articulo attack on mandarin | `articulo-attack-on-mandarin-process/` (5 aşama) | `articulo-attack-on-mandarin-details/` |
| s(t)lop | yok: repoda aşama fotoğrafı yok | `s-t-lop-details/` |

Süreç fotoğrafları yalnızca Yiğit'in bilgisayarında olan eserler için (Angora, Painstaking,
gxd, sept neuf, s(t)lop) süreç videoları, o dosyalar repoya yüklenince aynı araçla üretilir.

Süreç kapakları (`cover.jpg`): sol yarı ilk eskiz karesi, sağ yarı bitmiş resim. Üretim: `python3 tools/processcover.py <klasör>`.

Boyama kayıtları (`*-footage`) ve 3D model (`angora-mergvs-model`): Yiğit'in yüklediği videolar, `python3 tools/footage.py <kaynak.mp4> <klasör> [--crop x,y,w,h]` ile 1080×1920 beyaz kareye, sessiz, sonda kuş ekranıyla. Kaynaklar arşivde aynı klasörde `source.mp4`.
