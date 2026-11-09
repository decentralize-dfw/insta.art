# İddia envanteri ve düzeltme sicili

14 Ekim 2026. Önceki 17 algoritma belgesindeki karar değiştiren iddialar, yanlış çıkarımlar ve açık bırakılmış yöntem soruları aşağıda tekilleştirildi. Bazı satırlar eski metnin kesin savı değil, metinde önlenmesi gereken yanlış çıkarımdır; “önceki iddia/risk” sütunu bu yüzden ikisini kapsar. Aynı iddianın farklı dosyalardaki tekrarları ayrı kanıt sayılmadı.

Hata düzeltildi = sayı/mantık hatası; geri çekildi/çıkarıldı = bu denetimde yeterli teyit yok veya kullanım yanlış; doğrulanmadı = yanlış olduğu ispatlandı demek değil; tamamlandı = eksik yöntem yazıldı, hesap sonucu üretilmedi. Kaynak kodlarının adresleri [kaynak sicilinde](audit-sources-20261014.md).

| ID | Konu | Önceki iddia / risk | Denetim kararı | Düzeltilmiş sonuç | Dayanak |
| --- | --- | --- | --- | --- | --- |
| Q1-01 | 1 | Niş içerik beğenmek kendi dağıtımını ressam kitlesine taşır | Doğrulanmadı | İzleyici kişiselleştirmesi ters yönde üretici ödülü kanıtı değil | S001,S059 |
| Q1-02 | 1 | Yayın öncesi/sonrası etkileşim kotası ve warm-up zorunlu | Çıkarıldı | Dakika/gün eşiği ve trust score iddiası yok | S004,S005 |
| Q1-03 | 1 | Takipten çıkma takipçi kitlesini temizler | Düzeltildi | Takip edilenler ile takipçiler farklı kümeler | Mantıksal ayrım |
| Q1-04 | 1 | Haziran 2026 sistem kartı tarihleri kesin doğrulandı | Geri çekildi | 429; güncelleme günleri kullanılmıyor | S002,S003,S011,S012 |
| Q2-01 | 2 | Eski web3 takipçileri ilgisizdir; hesap kalıcı cezalıdır | Doğrulanmadı | Uyumsuzluk hipotezi; hesap verisi yok | Kullanıcı beyanı; S063 |
| Q2-02 | 2 | Keşif için önce takipçi beğeni barajı şart | Doğrulanmadı | Trial dış kitle yolu belgeli; sabit baraj yok | S063 |
| Q2-03 | 2 | Takipçi silerek engagement yükselmesi yeni ilgi kanıtı | Düzeltildi | Payda küçülmesi tek başına yeni izleyici getirmez | Aritmetik |
| Q2-04 | 2 | Dört kötü post/14–30 gün hesap kararını kesinleştirir | Çıkarıldı | Sabit yeterlilik/iyileşme eşiği yok | S047; yöntem |
| Q2-05 | 2 | Trial gizli ve random A/B'dir; 700 takipçiye kesin açık | Düzeltildi | Dolaylı follower maruziyeti; hesap erişimi bilinmiyor | S063 |
| Q2-06 | 2 | Forum ara verme örnekleri kalıcı ceza kanıtı | Çıkarıldı | Özbildirim, konu/ülke/dil ve reklam farkları; güncel kanıt yapılmadı | S070–S072 |
| Q3-01 | 3 | 2026 başlıklı saat raporları tamamen 2026 verisi | Düzeltildi | Yayın tarihi ile veri dönemi ayrı | S006,S032,S033 |
| Q3-02 | 3 | Sprout genel örneklemi Instagram örneklemi | Düzeltildi | Altı platform toplamı; IG alt n yok | S006 |
| Q3-03 | 3 | Sociality saatleri hedef izleyicinin yerel saati | Düzeltildi | Takım ayarı; çoğunluk UTC; Luxembourg aktarımı yok | S033 |
| Q3-04 | 3 | %52–%48,7 farkı %3,3 erişim artışı | Düzeltildi | 3,3 yüzde puan; medyanı aşma oranı | S033 |
| Q3-05 | 3 | Kaynaklar tek saat optimumunda birleşir | Reddedildi | Payda ve ağırlıklar farklı; ortalama zirve üretilemez | S006,S032,S033 |
| Q3-06 | 3 | Gün gün öneri tablosu kanıtlanmış takvim | Kaldırıldı | Operasyon seçimi ayrı; saat testi yeniden yazıldı | Yöntem |
| Q3-07 | 3 | Saat metodolojisi kusursuz | Düzeltildi | Örneklem eşiği tutarsızlığı, çoklu pencere seçimi, CI eksikliği | S033 |
| Q4-01 | 4 | Tanınma hook ailesi 1,29 | Hata düzeltildi | Aile 1,18; 1,29 tek teknik | S009 |
| Q4-02 | 4 | Aynı hesap karşılaştırması yalnız hook'u değiştirir | Hata düzeltildi | Konu/kurgu/kalite/süre sabit değil; nedensellik yok | S009 |
| Q4-03 | 4 | Hook sonucu erken tutma, takip veya satış artışı | Düzeltildi | Ölçülen normalize views | S009 |
| Q4-04 | 4 | %25 yüksek ile %25 düşük aynı karşılaştırma | Düzeltildi | Bölme tabanı farklı; 1,18/0,94 ve tersi ayrıldı | S009; aritmetik |
| Q4-05 | 4 | Sık kullanılan hook etkisini yitirir | Doğrulanmadı | Teknik düzeyindeki ilişki nedensel doygunluk değil | S009 |
| Q4-06 | 4 | Merak boşluğu makalesi IG2026 etkinliğini kanıtlar | Çıkarıldı | Tam metin/abstract bu denetimde doğrulanamadı | S084,S085 |
| Q4-07 | 4 | 14 mekanizma ve örnek cümleler ölçülmüş başarı sıralaması | Düzeltildi | Çalışma sınıflandırması ve özgün örnekler; sıralı başarı iddiası yok | Yazar tasarımı |
| Q4-08 | 4 | İlk üç saniye, yüz, trend ses veya negatiflik zorunlu | Doğrulanmadı | Üretim kontrolü ile platform barajı ayrıldı | S050; sınırlı kaynaklar çıkarıldı |
| Q5-01 | 5 | CTA katsayıları nedensel kazanç | Düzeltildi | Gözlemsel farklı gruplar; alt n/CI eksik | S087,S088 |
| Q5-02 | 5 | Basın raporu yanlış TikTok'a bağlanıyor | Geri çekildi | Güncel sayfada IG raporu mevcut; karşılaştırma linki ayrı | S087 |
| Q5-03 | 5 | Her yorum CTA'sı engagement bait cezası alır | Düzeltildi | Bağlama uygun çağrı ile bait eşit değil; kesin yaptırım listesi yok | S060 |
| Q5-04 | 5 | Yorum/paylaşım/takip aynı başarı | Düzeltildi | Eylem, payda, özgün kişi ve anlamlı görüşme ayrı | Yöntem |
| Q5-05 | 5 | Link-in-bio otomatik erişim cezası | Doğrulanmadı | Forum genellemesi kullanılmıyor | S094 |
| Q6-01 | 6 | Dağıtım sabit kişi basamaklarıyla ilerler | Çıkarıldı | Tarihsel aday/ranking açıklaması sabit eşik vermiyor | S059,S060 |
| Q6-02 | 6 | Viral videoların erken yükselmesi genel viral olasılık | Hata düzeltildi | Başarıya ve trending seçimine koşullu örneklem | S061 |
| Q6-03 | 6 | İlk 72 saat sonrası gönderi biter | Düzeltildi | Yoğunluk bulgusu ve ürün paylaşım akışı son tarih değil | S088,S063 |
| Q6-04 | 6 | Süre × tamamlanma oranı ortalama izleme süresi | Hata düzeltildi | Yalnız ortalama izlenen süre yüzdesiyse çarpılabilir | Metrik tanımı |
| Q6-05 | 6 | Paylaşım/erişim yayılım katsayısıdır | Düzeltildi | Yeni izleyici ve örtüşme bilinmeden hesaplanamaz | Yöntem |
| Q6-06 | 6 | Viral erişim sanat değeri veya doğru kitle garantisi | Reddedildi | İlgili hesap eylemi ve eser değeri ayrı | Yöntem |
| Q7-01 | 7 | Düşük erişim ceza veya kötü eser tanısı | Düzeltildi | En az iki alternatif ve sonraki kontrol tablosu | S060; yöntem |
| Q7-02 | 7 | Eksik metrik sıfır, views reach veya DM share'dir | Düzeltildi | Ekran tanımları ve kapsam korunur; N/A ayrı | S048 erişim kısıtı; yöntem |
| Q7-03 | 7 | Düşük ortalama süre ilk saniye kaybını kanıtlar | Düzeltildi | Retention yoksa kayıp yeri bilinmiyor | Metrik mantığı |
| Q7-04 | 7 | Birkaç post veya büyük views sayısı yeterli veri | Tamamlandı | Bağımsızlık, atama birimi, pratik fark ve güç analizi eklendi | Yöntem; hesap örneği |
| Q7-05 | 7 | 3/300 ile 8/400 kesin iki kat başarı | Düzeltildi | Belirsizlik aralıkları ve seçilmiş organik dağıtım sınırı | Aritmetik; varsayımsal veri |
| Q7-06 | 7 | Sıfır olay gerçek olasılık sıfır demek | Düzeltildi | Koşullu üst sınır ve uygun fırsat varsayımı | İstatistiksel yöntem |
| Q7-07 | 7 | Eski web3 medyanı yeni resim ölçütüdür | Düzeltildi | Yeni dönem ve benzer format ayrı; sıfır medyandan çarpan yok | Yöntem |
| Q8-01 | 8 | Carousel'e dönüştürmek 9 kat kazandırır | Düzeltildi | Gözlemsel grup ortalaması; views tekil erişim değil | S087,S088 |
| Q8-02 | 8 | 35M Socialinsider örneklemi Q2 2026'ya aittir | Düzeltildi | Ana veri 2025; ayrı Q2 n yok | S025 |
| Q8-03 | 8 | %0,50 ve %0,48 farkı %0,02 göreli | Düzeltildi | 0,02 yüzde puan; yaklaşık %4,17 göreli | S025; aritmetik |
| Q8-04 | 8 | Save/follower erişen kişinin save olasılığı | Düzeltildi | Takipçi paydası; farklı oranlar kıyaslanmaz | S089 |
| Q8-05 | 8 | %60–70 Reel optimumdur | Çıkarıldı | Uzman görüşü kontrollü optimum testi değil | S025 |
| Q8-06 | 8 | Organik lider ücretli satış lideridir | Reddedildi | Format, yerleşim, optimizasyon ve sonuç ayrı | Yöntem |
| Q8-07 | 8 | 40×3 hazır ve bağımsız 120 içerik | Düzeltildi | Yaklaşık fırsat; malzeme/ek değer/üretim maliyeti gerekir | Kullanıcı tahmini; yöntem |
| Q9-01 | 9 | Profil ziyareti hedefi takip/satış getirir | Düzeltildi | Ara olay ile gerçek sonuç ayrı; hesap menüsü görülmedi | S034 |
| Q9-02 | 9 | Optimizasyon olayı faturalandırma olayıdır | Düzeltildi | Kurulumda ayrı doğrulanacak alanlar | Yöntem |
| Q9-03 | 9 | Daha çok harcama ROAS düşüşüne neden oldu | Düzeltildi | Bileşim ve dönem farkı; rastgele deney değil | S043 |
| Q9-04 | 9 | ROAS kâr veya ek satıştır | Düzeltildi | Gelir/reklam harcaması; marj ve nedensel etki ayrı | Metrik tanımı |
| Q9-05 | 9 | 5 €/gün kabul edilmiş kullanıcı bütçesi | Geri çekildi | Yalnız aritmetik senaryo; harcama yetkisi değil | Kayıt tutarlılığı |
| Q9-06 | 9 | 50 olay/7 gün, %20 artış ve günlük tavan kesindir | Doğrulanmadı | Tam güncel koşullar erişilemedi; eşik kullanılmıyor | S039–S041 |
| Q9-07 | 9 | Aynı sette iki reklam random A/B'dir | Düzeltildi | Eşit/rasgele dağıtım varsayılmaz | Deney tasarımı |
| Q9-08 | 9 | Öğrenmeden çıkış ticari başarıdır | Reddedildi | Olay kalitesi ve ekonomik sınır ayrı | Yöntem |
| Q9-09 | 9 | Kabul edilebilir CPA ve yeterli bütçe hazırdır | Tamamlandı | Marj/olasılık/maliyet senaryosu ve toplam kayıp sınırı; sayı atanmadı | Yöntem |
| Q10-01 | 10 | Sanat ilgisi eklemek kesin dar hedeftir | Düzeltildi | Kontrol/öneri ve gerçek dağıtım ayrılır | S074 |
| Q10-02 | 10 | Varsayılan genişleme ve tüm kontrol listesi kesin | Geri çekildi | Tam sayfa/hesap ekranı görülmedi; koşullu yazıldı | S073–S076 |
| Q10-03 | 10 | Şehir hedefi yerleşik koleksiyonerleri gösterir | Reddedildi | Konum tanımı ikamet/niyet belgesi değil | S076; yöntem |
| Q10-04 | 10 | 700 takipçi hazır 700 kişilik reklam kitlesi | Düzeltildi | Olay, pencere, eşleşme ve kullanılabilirlik bilinmiyor | S077–S080 |
| Q10-05 | 10 | Eski kitle kesin kötü lookalike kaynağı | Düzeltildi | Uyum belirsizliği; köken değersizlik kanıtı değil | Yöntem |
| Q10-06 | 10 | Ucuz ülkedeki beğeni hedef pazar ilgisini kanıtlar | Reddedildi | Örneklem–amaç uyuşmazlığı; kalıcı zehirlenme iddiası yok | Yöntem |
| Q10-07 | 10 | Kitle testinde eşit bütçe eşit insan/dağıtım | Tamamlandı | Örtüşme, genişleme ve dağıtım bileşimi eklendi | Yöntem |
| Q11-01 | 11 | 18 gün reklamın optimum ömrüdür | Düzeltildi | Gözlenen aktif süre, yönetici kapatma ve seçilim | S056 |
| Q11-02 | 11 | Düşük toplam gösterim yorgunluğu dışlar | Düzeltildi | Reach yok; tekrar ölçülmüyor | S056 |
| Q11-03 | 11 | Frequency 3 veya 7 gün evrensel kapatma eşiği | Doğrulanmadı | Amaç maliyeti, kalite ve dönem birlikte | S051–S055 erişim sınırı |
| Q11-04 | 11 | CPC artışı kesin yorgunluk; CPM içerikten bağımsız | Düzeltildi | Aritmetik bileşenler neden kanıtı değil | Yöntem |
| Q11-05 | 11 | Birbirini izleyen kaydırmalı raporlar bağımsız teyit | Tamamlandı | Örtüşen günler ve atıf olgunluğu açıklandı | Yöntem |
| Q11-06 | 11 | Kopyalama/aç–kapa bütçe reseti garantili fayda | Doğrulanmadı | Evrensel fayda ve güvenli yüzde yok | S039,S041 |
| Q11-07 | 11 | Her yeni post eski reklamı kapatır/eser tüketilir | Reddedildi | Organik takvim, reklam ömrü, eser ve sunum ayrı | Yöntem |
| ALG-01 | Çerçeve | Search/Feed kesin 2026 sinyal listesi okundu | Geri çekildi | Tam kartlar doğrulanmadı; tarihsel Explore modeli sınırlı tutuldu | S002,S003,S011,S012,S059 |
| ALG-02 | Çerçeve | %75 özgünlük ve 2026 fotoğraf değişimi güncel kesin kural | Düzeltildi; kısmen yeniden doğrulandı | S013: %75 ABD Q4 2025 bileşimidir. S015/F16 fotoğraf/carousel özgünlük güncellemesi resmî indeksle sınırlı doğrulandı; sabit katsayı veya tam güncel politika dökümü değildir. | S013/F15; S015/F16; S014,S068 bu turda tam teyit edilmedi |
| ALG-03 | Çerçeve | Sends beğeninin X katı; süre/ses/filigran kesin eşikler | Doğrulanmadı | Sabit ağırlık/teknik baraj kullanılmıyor | S016–S018 |
| ALG-04 | Çerçeve | Eylül 2026 Mosseri dört videosu izlenip doğrulandı | Geri çekildi | Birincil videolar doğrulanmadı; ikincil anlatım teknik kanıt değil | S067; eski kapanış |
| ALG-05 | Çerçeve | Teen içerik ayarı yetişkin nü/sanat kuralıdır | Düzeltildi | Topluluk, öneri, reklam ve yaş katmanları ayrı | S023,S060,S095,S096 |
| ALG-06 | Çerçeve | Sanat istisnası reklam ve müzik kullanımını da kapsar | Tamamlandı | Müzik/organik/reklam ayrı; indeks sınırı ve dosya bazlı kontrol | S095–S098 |
| ALG-07 | Çerçeve | Business hesap, eski eser, sessizlik veya tekrar otomatik ceza | Doğrulanmadı | Evrensel yasak/eşik yok iddiası değil, yeterli kanıt yok | Kanıt sınırı |
| ALG-08 | Çerçeve | Works sayfasındaki 10 eser bağımsız bu turda incelendi | Geri çekildi | Bu denetimde eser/site incelemesi yapılmadı; kullanıcı tahmini ayrı | Önceki ana belge |
| ALG-09 | Durum | Ayak 1 tamamlandı; Ayak 2 durduruldu | Düzeltildi | 1–12 yazılmış olması kapsamlı sistem kapanışı değildi. Devam turunda birleşik model ve eksik sistem yüzeyleri yazıldı. Hesap erişimi araştırma tamamlanma koşulu değil; paralel Ayak 2 yetkili. | Güncel kullanıcı talimatı |
| ALG-10 | Durum | Eski JSON/okuyucu güncel sonuçları gösterir | Düzeltildi | Markdown ile yeniden üretim ve gezinme kontrolü eklendi | Dosya doğrulaması |

## Kapsam ve hesap sınırı

Bu sicil 1–11 ile onları yöneten eski çerçeve/kapanış kayıtlarını denetler. Piyasa ve taktik arşivleri bu sicille doğrulanmış sayılmaz. Sonraki devam çalışmasında Stories 12 ve kalan reklam koşulları yazıldı; güncel kapsam [araştırma sonucunda](algorithm-research-conclusion-20261014.md), ek kaynaklar [Stories sicilinde](stories-sources-20261014.md). Gerçek Account Status, güncel Insights ve Ads Manager ayarları görülmedi. Bu boşluklar yerine sayı veya kesin mekanizma yazılmadı. Her sorunun güncel cevabı ilgili dosyanın içinde doğrudan değiştirildi; sicil eski hatalı metnin üstüne eklenen bir feragat notu değildir.

Güncel araştırma kapsamı [birleşik sistem modeli](system-model-20261014.md) ve [sonuç kaydı](algorithm-research-conclusion-20261014.md) ile genişletildi. Hesap ekranları görülmemiş olması bu sistem araştırmasının açık işi değildir.
