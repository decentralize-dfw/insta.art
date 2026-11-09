# Editoryel carousel'ler

Farklı resimlerden alınmış, aynı temayı (konu, renk ya da biçim) taşıyan yakın detaylar.
Her sayfa 1080×1350, yazısız. Obje tek başına, ortalı, kesilmeden, %5 beyaz payla (`tools/boxcrop.py`); obje detay fotoğrafında bütün varsa ondan, yoksa ana resimden kırpılır. Caption: tek
kelimelik tema ve sayfa sırasıyla eser adları. Üretim: `python3 tools/render.py <klasör>/spec.json`.

| klasör | tema | sayfa |
| --- | --- | --- |
| `crossed-eyes/` | çarpı gözler | 6 (guarding, good people, 7 fam, wings of abyss, victim, baby rights) |
| `chairs/` | sandalyeler | 6: guarding (ters sandalye), mandarin (ters sandalye), victim (beyaz sandalye), Virgil, sept neuf (koltuk), guarding (ayaklık) |
| `tables/` | masa, küçük masa, yatak | 4: walls (masa), sept neuf (sehpa), crow (divan), caprocorn (sandık) |
| `birds/` | kuşlar | 9 (sept neuf, wings of abyss: üç gaga, crow: iki detay, mandarin: üç kuş) |

Önerilen sonraki temalar: gözler, dişler ve ağızlar, eller, ayaklar ve pençeler, beden
baloncukları, asılı ve ters figürler, nesneler, kanatlar, saçlar, resimdeki yazılar, imzalar,
halkalar ve spiraller, çerçeve içinde çerçeve, başlangıçlar (ilk eskizler), yüzeyler, renkler.
