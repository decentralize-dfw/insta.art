# Editoryel carousel'ler

Farklı resimlerden alınmış, aynı temayı (konu, renk ya da biçim) taşıyan yakın detaylar.
Her sayfa 1080×1350, yazısız. Obje tam ve ortada, 4:5 karede etrafı resmin kendisi; beyaz yok (`tools/boxcrop.py`, `"fit": "fill"`). Resim kenarda bitiyorsa kare de orada biter. Obje detay fotoğrafında bütün varsa ondan, yoksa ana resimden kırpılır. Kuşun resmin tamamı olduğu iki sayfada (cute but unemployed, wings of abyss) resim 4:5'ten dar olduğu için yanlarda ince beyaz kalır. Her carousel'in ilk sayfası (`00.jpg`) kapak: bütün sayfalar ekranı dolduran bir grid, ortada beyaz etiket içinde tema adı (Hanken Grotesk, siyah). Üretim: `python3 tools/gridcover.py <klasör>`. Caption: tek
kelimelik tema ve sayfa sırasıyla eser adları. Üretim: `python3 tools/render.py <klasör>/spec.json`.

| klasör | tema | sayfa |
| --- | --- | --- |
| `crossed-eyes/` | çarpı gözler | 6 (guarding, good people, 7 fam, wings of abyss, victim, baby rights) |
| `chairs/` | sandalyeler | 6: guarding (ters sandalye), mandarin (ters sandalye), victim (beyaz sandalye), Virgil, sept neuf (koltuk), guarding (ayaklık) |
| `platforms/` | platforms: masa, sehpa, divan, sandık | 4: walls (masa), sept neuf (sehpa), crow (divan), caprocorn (sandık) |
| `shoes/` | ayakkabılar | 11, her ayakkabı tam ve ortada, etrafı resmin kendisi (beyaz yok, `"fit": "fill"`): sept neuf (2), cellular, s(t)lop (2), duality (2), viperella (2), cute but unemployed (2) |
| `birds/` | kuşlar | 13, her kuş bütün: sept neuf, cute but unemployed, crow, family dinner (ortadaki baş), lucid drowning (pembe ve koyu kuş), wings of abyss, duality (soluk tüylü kuş), s(t)lop, mandarin (dört kuş) |

Önerilen sonraki temalar: gözler, dişler ve ağızlar, eller, ayaklar ve pençeler, beden
baloncukları, asılı ve ters figürler, nesneler, kanatlar, saçlar, resimdeki yazılar, imzalar,
halkalar ve spiraller, çerçeve içinde çerçeve, başlangıçlar (ilk eskizler), yüzeyler, renkler.
