# Instagram araştırması

Son kontrol: 16 Ekim 2026. Kullanıcının isteğiyle `u320x/main/instagram/` altında şifresiz yürütülür. Parola dosyalara eklenmedi.

## Güncel durum

Birinci ayağın amacı güncel Instagram algoritmasının kapsamlı çözümlemesidir. Önceki 1–12 düzeltmeleri üzerine sistem mimarisi, bütün temel yüzeyler, içerik eşleştirme, dağıtım/geri bildirim, 2025–2026 değişiklikleri ve güncel reklam mimarisi eklendi. Hesap erişimi bu araştırmanın tamamlanma koşulu değildir.

Yeni sistem sicili 34 kaynak kaydı ve 36 URL içerir; bunlar bağımsız yeni araştırmaların toplamı değildir. Tam metin ve sınırlı resmî indeks ayrılır. Önceki 83 iddia, 98 URL ve Stories eki hataların ve devam turlarının ayrı sicilleridir.

Ayak 2’de [28 galeri cevabı, üç kurum dosyası, yeni 5×5 kariyer örneklemi ve seçilmiş görsel karşılaştırma](02-market/market-gap-closure-20261016.md) yazıldı. Doğrudan Instagram incelemesi kullanıcının son talimatıyla kapsam dışında. Ayak 3 kullanıcı isteğiyle üç alt odada toplam 60 soruluk yeni araştırma çerçevesine geçti; eski taktik taslağı tarihsel olarak ayrıdır. Ayak 4 için [haftalık pattern ve tarihli 90 günlük uygulama stratejisi](04-strategy/strategy-index-20261016.md) yazıldı. Planlanan 65 akış yayını ve 26 reklam dönemi vardır; toplam medya bütçesi 390 €. Uygulama henüz başlamadı; hedef 5.000 organik ve nişle ilgili takipçi, garanti veya gerçekleşmiş sonuç değildir.

## Önce okunacaklar

- [16 Ekim kontrolü ve somut düzeltmeler](01-algorithm/recheck-20261016.md)

- [Instagram algoritmasının birleşik modeli](01-algorithm/system-model-20261014.md)
- [Yüzeylerin işleyişi](01-algorithm/system-surfaces-20261014.md)
- [2025–2026 değişiklikleri](01-algorithm/system-changes-20261014.md)
- [Sistem kaynak ve kapsam sicili](01-algorithm/system-evidence-20261014.md)

- [Güncel algoritma araştırması sonucu](01-algorithm/algorithm-research-conclusion-20261014.md)
- [Stories analizi](01-algorithm/alg-q12-stories.md)
- [12 sonrası reklam koşulları](01-algorithm/algorithm-remaining-controls-20261014.md)
- [Stories ve ek koşullar kaynak sicili](01-algorithm/stories-sources-20261014.md)
- [İlk 1–11 denetiminin tarihsel sonucu](01-algorithm/algorithm-close-v1.md)
- [1–18 araştırma dizini](01-algorithm/algorithm-questions-20261014.md)
- [83 maddelik iddia envanteri](01-algorithm/audit-claims-20261014.md)
- [98 URL kaynak ve erişim sicili](01-algorithm/audit-sources-20261014.md)
- [Sanat, öneri, reklam ve müzik ayrımı](01-algorithm/policy-boundaries-20261014.md)
- [Güncel çalışma yetkisi ve durum](01-algorithm/user-review-gate-20261014.md)

Eski metinlerdeki yanlışlar yalnız bu dizinde açıklanmadı: ilgili soru dosyaları doğrudan değiştirildi. Önceki sürümler Git geçmişindedir. 1,29 hook aile değeri, tamamlanma–izleme süresi hesabı, nedensellik sıçramaları, kabul edilmiş gibi yazılan bütçe ve erken kapanışlar düzeltildi.

## Dosyalar ve okuyucu

`01-algorithm/`, `02-market/`, `03-tactics/`, `04-strategy/` altındaki Markdown dosyaları asıl içeriktir. `findings.json`, mevcut Markdown'ın üretilmiş okuyucu verisidir; artık eski aktarım anının değişmez görüntüsü değildir. İddia ve kaynak sicillerinin ayrıca JSON sürümleri vardır. `index.html` bütün mevcut belgeleri şifresiz gösterir; soru ve ayak hiyerarşisi `findings.json` içinden gelir.

Güncellemeden sonra:

```bash
python instagram/sync_findings.py
python instagram/sync_findings.py --check
```

Yerel okuyucu için depo kökünde `python -m http.server 8000` çalıştırıp `http://localhost:8000/instagram/` açılabilir. Dosyanın main'e kaydedilmesi bir GitHub Pages yayını yapıldığı anlamına gelmez.

## Paralel çalışma

Diğer sohbetin alanını yeniden yazma. Push öncesi main'in son halini al, ortak JSON'u o anki tüm Markdown ile üret; mevcut commit üzerine beklenen SHA kontrolüyle ilerle. Kaynak düzeni: iddia → özgün bağlam → veri dönemi/örneklem → sınırlama → hesaba aktarım → düzeltilmiş sonuç. Kaynak bulgusunu, çalışma hipotezini ve hesapta henüz ölçülmemiş sonucu ayır.

## Üçüncü ayak — üç alt oda

[60 sorunun dizini ve ortak araştırma kalıbı](03-tactics/tactics-rooms-index-20261016.md).

- [Oda 1 / 01–20: Genel Instagram taktikleri](03-tactics/room-01-instagram-tricks-questions-20261016.md).
- [Oda 2 / 21–40: Sanat dünyasında Instagram iletişimi](03-tactics/room-02-art-instagram-communication-questions-20261016.md).
- [Oda 3 / 41–60: Algoritmik içerik taktikleri](03-tactics/room-03-algorithmic-content-questions-20261016.md).

Üçüncü ayakta **60/60 kaynaklı cevap, 0 uygulanmış deney**. Cevaplar ilgili odalarda; [genişletilmiş kaynak/karar sicili](03-tactics/tactics-evidence-06-60-20261016.md) ve [ilk beşin sicili](03-tactics/tactics-evidence-01-05-20261016.md) ayrı izlenir. Her cevap sekiz ortak inceleme bölümünü içerir. Araştırma cevabının yazılması uygulanmış doğrulama anlamına gelmez.


[Üçüncü ayağın uygulama ve karar sentezi](03-tactics/tactics-operating-decisions-20261016.md) · [60 cevabın kapsam ve son kontrol kaydı](03-tactics/tactics-completion-audit-20261016.md).

[İlk ayağın açık iş kontrolü](01-algorithm/algorithm-open-work-resolution-20261016.md) · [İkinci ayağın güncel kapanış kaydı](02-market/market-gap-closure-20261016.md).

## Dördüncü ayak — uygulama planı

[Başlangıç ve belge dizini](04-strategy/strategy-index-20261016.md) · [haftalık pattern](04-strategy/strategy-weekly-pattern-20261016.md) · [90 günlük takvim](04-strategy/strategy-calendar-90days-20261016.md) · [reklam politikası](04-strategy/strategy-ad-plan-20261016.md).

19 Ekim 2026–16 Ocak 2027; Europe/Paris. Strateji yalnız depodaki 1–3. ayaktan türetildi. 175 belge, 18 + 28 + 60 soru ve 266 mevcut iddia kaydı aktarım kararlarıyla [kapsam envanterine](04-strategy/strategy-evidence-coverage-20261016.md) bağlandı. Reklam sonuçları organik hedefe sayılmaz. Doğrudan Instagram incelemesi kapsam dışında kalır.

Plan verisi ve boş ölçüm şablonu `04-strategy/` altında. Kontrol: `python instagram/validate_strategy.py` ardından `python instagram/sync_findings.py --check`.
