# Müzikli montaj · Virgil V4 düzeninde

Onaylı Virgil V4'ün (`posts/montage/virgil-barricade-studio/`) düzeni, kare kare aynı (60 fps):

- **0–5,800 sn:** 46 detay planı, hepsi ekranı kenardan kenara dolduruyor. Küçük resim, beyaz boşluk yok. İlk plan 18 kare (0,3 sn), sonra 7'şer kare (biri 8), sonda yavaşlayan 7, 10, 11, 14 kare.
- **5,800–9,550 sn:** resim 4 × 5 parçadan ortadan dışa, her vuruşta 2–3 parça (V4'ün sırası) birleşir. Resim genişliğe oturur; üstte ve altta V4'teki gibi beyaz şerit.
- **9,550–11,417 sn:** biten resim.
- **11,417–12,417 sn:** V4'ün son vuruşu ve siyah kuş-sandalye logosu (V4'ün kendi son karesi).
- **Ses:** V4'ün Axwell, *Barricade* sesi; 0–11,300 sn ve 14,600 sn'den sona (son vuruş ve yankı). Virgil'deki stüdyo bölümü bu eserlerde stüdyo fotoğrafı olmadığı için yok; vuruşlar yine yerinde. Ses dosyaya gömülü, ikinci müzik eklenmez.
- **Kalite:** detaylar 2.500–5.184 px fotoğraflardan; büyütülünce yumuşayan detaylar (7 fam, articulo, s(t)lop) yok. Neredeyse boş zemin kesitleri ve birbirine benzeyen parçalar elendi. Beyaz kenarla fotoğraflanmış resimler kırpıldı. Karga yok.
- **Üretim:** `python3 tools/montage.py build <tarif> <klasör>` (sept-neuf, kopstal, genel).
