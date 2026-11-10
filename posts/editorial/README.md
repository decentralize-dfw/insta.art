# Editoryel carousel'ler

Farklı resimlerden alınmış, aynı temayı (konu, renk ya da biçim) taşıyan yakın detaylar.
Her sayfa 1080×1350, yazısız. Obje tek başına, ortalı, kesilmeden, %5 beyaz payla (`tools/boxcrop.py`); obje detay fotoğrafında bütün varsa ondan, yoksa ana resimden kırpılır. Caption: tek
kelimelik tema ve sayfa sırasıyla eser adları. Üretim: `python3 tools/render.py <klasör>/spec.json`.

| klasör | tema | sayfa |
| --- | --- | --- |
| `crossed-eyes/` | çarpı gözler | 6 (guarding, good people, 7 fam, wings of abyss, victim, baby rights) |
| `chairs/` | sandalyeler | 6: guarding (ters sandalye), mandarin (ters sandalye), victim (beyaz sandalye), Virgil, sept neuf (koltuk), guarding (ayaklık) |
| `tables/` | masa, küçük masa, yatak | 4: walls (masa), sept neuf (sehpa), crow (divan), caprocorn (sandık) |
| `shoes/` | ayakkabılar | 10, her ayakkabı bütün: sept neuf (2 topuklu), cellular (kırmızı topuklu), s(t)lop (2 spor ayakkabı), duality (beyaz çizgi 2 topuklu), viperella (2 sivri), cute but unemployed (stiletto) |
| `birds/` | kuşlar | 13, her kuş bütün: sept neuf, cute but unemployed, crow, family dinner (ortadaki baş), lucid drowning (pembe ve koyu kuş), wings of abyss, duality (soluk tüylü kuş), s(t)lop, mandarin (dört kuş) |

Önerilen sonraki temalar: gözler, dişler ve ağızlar, eller, ayaklar ve pençeler, beden
baloncukları, asılı ve ters figürler, nesneler, kanatlar, saçlar, resimdeki yazılar, imzalar,
halkalar ve spiraller, çerçeve içinde çerçeve, başlangıçlar (ilk eskizler), yüzeyler, renkler.
