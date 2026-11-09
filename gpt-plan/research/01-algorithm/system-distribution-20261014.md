# Dağıtım ve ölçüm — kaynakla doğrulanan yollar

Son kontrol: 16 Ekim 2026. 2024'te açıklanan küçük grup → büyük grup şeması, bütün güncel dağıtımın doğrulanmış işleyişi olarak bu metinden çıkarıldı. Güncel açıklama, ayrı erişim yolları ve gözlenebilir davranışlar üzerinden kuruluyor.

## Üç dağıtım yolu

| Yol | Doğrulanmış bilgi | Kaynak |
| --- | --- | --- |
| Öneri seçimi | Kamusal adaylardan kullanıcıya ilişkin tahminlerle seçim | F27/F31, Haziran 2026 indeks; F30, Mayıs 2026 altyapı |
| Sosyal aktarım | Native repost ile paylaşanın takipçilerine öneri; DM ile doğrudan karşılaşma | F21/F13, 2025 ürün açıklamaları |
| Ücretli dağıtım | Reklam amacı ve adayına ilişkin ayrı tahmin modelleri | F19/F20, Ağustos/Ekim 2026 teknik açıklamalar |

Bu yolların toplamı bir yayının erişimine katkı sağlayabilir. **Araştırma çıkarımı:** Yalnız yüksek görüntülenmeye bakıp tamamını organik öneri başarısı diye adlandırmak, sosyal aktarım veya ücretli dağıtım etkisini atlayabilir.

## Takipçi olmayanlara erişim

Haziran 2025 güncellemeli Trial Reels belgesi önce takipçi olmayanlara sunum yolunu açıklar. Aynı belge, takipçilerin DM veya ses/konum sayfası gibi başka yollarla içeriği görebileceğini belirtir. [F13](system-evidence-20261014.md).

**Araştırma çıkarımı:** Mevcut takipçilerden zorunlu bir onay alınmasını bütün keşfin tek giriş koşulu sayamayız. Buna karşılık bu üründen bütün organik yayınlar için sabit başlangıç kitlesi, basamak boyutu veya saatlik genişleme programı türetilmez.

## Tepki bilgisi nasıl okunmalı?

Güncel Feed Recommendations kartında yakın dönem takip ve etkileşim geçmişi; Feed kartında geçme tahmini bulunur. SilverTorch açıklaması etkileşim özellikleri ve uygunluk değişikliklerinin güncel indeks bilgisine aktarılabildiğini anlatır. Bunlar bir yayına her eylem için sabit erişim puanı verildiğini açıklamaz. [F27, F31, F30](system-evidence-20261014.md).

**Araştırma çıkarımı:** Beğeni, paylaşma, izleme ve profil açmayı ayrı okumak gerekir. Gönderme bir kişiye doğrudan ulaşma eylemi de olabilir; öneri sistemindeki ek etkiyle aynı sayı değildir. Yüksek bir eylem oranının her sonraki izleyici grubunda korunacağı varsayılmaz.

## Ortalama izleme ile tamamlanma farklıdır

Bu ayrım ölçüm aritmetiğidir; Instagram'ın açıklanmamış formülü değildir. Ortalama izleme süresi / video uzunluğu, **normalize ortalama izlemeyi** verir. Videonun sonuna ulaşanların oranını vermez. Platformun tekrar ve payda tanımı ayrıca korunmalıdır.

Varsayımsal 10 saniyelik bir videoda, tekrar olmayan 100 izleme düşünelim:

| Dağılım | Toplam izleme süresi | Ortalama | Sonuna ulaşan |
| --- | --- | --- | --- |
| 100 kişi 5'er saniye izler | 500 saniye | 5 saniye | 0 kişi: %0 |
| 50 kişi 10'ar saniye, 50 kişi 0 saniye izler | 500 saniye | 5 saniye | 50 kişi: %50 |

Örnek, 0 saniyelik gözlemlerin aynı varsayımsal paydada sayıldığı matematik modelidir; Instagram'ın görüntüleme sayma kuralı değildir. Aynı ortalama iki farklı tamamlanma oranıyla uyumludur. Bu yüzden ortalamadan gerçek tamamlanma türetilmez. [Soru 6'nın ölçüm düzeltmesi](alg-q6-viral.md) ile tutarlıdır.

## Metrikleri karşılaştırmanın koşulları

| Soru | Kullanılacak ayrım |
| --- | --- |
| Kaç kişi karşılaştı? | Tekil erişim ile görüntüleme/gösterim ayrılır |
| Ne kadar tüketildi? | Toplam süre, ortalama, normalize ortalama ve tamamlanma ayrılır |
| Ne yaptı? | Beğeni, kaydetme, gönderme, profil açma ve takip ayrı olaylardır |
| Hangi yoldan geldi? | Öneri yüzeyi, doğrudan aktarım ve ücretli dağıtım ayrılır |
| Hangi dönemde ölçüldü? | Aynı yayın yaşı ve veri penceresi karşılaştırılır |

Tablo araştırmanın ölçüm yöntemidir; bütün alanların her hesapta görünür olduğu iddiası değildir. Verilmeyen alan N/A bırakılır. Eylem/erişim oranı eylem sayısını tekil kişi sayısıyla karşılaştırır; olaylar tekrarlanabiliyorsa benzersiz eylem yapan kişi oranı olarak adlandırılmaz.

## Saatler ve karşılaştırma

Trial Reels'teki yaklaşık 24 saat sonuç gösterimi ve isteğe bağlı ilk 72 saat otomatik açılma koşulu ürün özelliğidir. Genel viral ömür veya bütün içerikler için dağıtım son tarihi değildir. [F13](system-evidence-20261014.md).

**Araştırma yöntemi:** Farklı saatte, konuda, formatta ve ücretli destekle yayımlanan içerikler arasında görülen fark tek bir değişkene yüklenmez. Gözlemsel benchmark yayımlandığı yılın tüm Instagram'ı üzerinde random deney sayılmaz. Bu yöntem hesabına erişim istemek değildir; kaynakların neyi kanıtladığını sınamanın ölçütüdür.

## Çıkarılan açıklama

Güncel belgeler aday bulma ve davranış tahminini; ürün belgeleri de öneri dışında sosyal ve ücretli yolları gösteriyor. **Araştırma sentezi:** Dağıtımı anlamak için adaylık, tüketim, aktarım ve sonuç birlikte fakat ayrı ölçülerle incelenmelidir. Sabit parti büyüklüğü veya gizli eylem katsayısı eklemek gerekmiyor.
