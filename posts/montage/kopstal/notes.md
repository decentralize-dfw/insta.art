# Müzikli montaj (REELS_FORMULU.md)

- **Formül:** 50 hızlı plan, her biri 1/16 vuruş (117 ms), sert kesme: resmin tamamı, detay, detay... Sonra 4 yavaşlayan plan (117, 156, 195, 234 ms). Sonra 3×3 düzen beyaz zeminde her vuruşta bir parça dolar (orta, orta sağ, orta sol, üst orta, alt orta, alt sağ, üst sol, üst sağ, alt sol), 2 vuruş tam düzen. Video 10. vuruşta biter.
- **Tempo:** 128 BPM, 60 fps, 11,25 sn. Her kesim mutlak vuruş zamanından hesaplandı, kayma yok (`timeline.json`).
- **Müzik (Yiğit uygulamada ekler):** ~128 BPM bir parça seç. **İlk düzen parçası 6,56. saniyede** gelir: müziği güçlü bir vuruş (kick, drop, cümle başı) tam oraya düşecek şekilde başlat. Referans reel'in şarkısı Instagram'da var: Axwell, *Barricade (Radio Edit)*, 128 BPM.
- **Ses yok, bitiş ekranı yok:** video döngüye girer.
- **Kalite:** detaylar 2.500–5.184 px fotoğraflardan; büyütülünce yumuşayan detaylar (7 fam, articulo, s(t)lop) kullanılmadı. Yatay triptik (Painstaking) dikey karede küçük kaldığı için yalnız detaylarıyla var. Beyaz kenarla fotoğraflanmış resimler kırpıldı.
- **Üretim:** `python3 tools/montage.py build <tarif> <klasör>` (tarifler: sept-neuf, kopstal, genel). Spec: `spec.json`.
