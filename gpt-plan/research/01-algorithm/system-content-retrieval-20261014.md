# İçerik bilgisi ve aday bulma — güncel açıklama

Son kontrol: 16 Ekim 2026. 2023 belgesindeki eski üretim teknikleri güncel Instagram mimarisi olarak kullanılmıyor. Bu bölümün güncel teknik dayanağı Mayıs 2026 SilverTorch açıklaması ve aynı çalışmanın Mayıs 2026 sürümüdür. [F30, F34](system-evidence-20261014.md).

## Aday bulmanın işi

Aday bulma, büyük içerik havuzunu sonraki sıralamanın değerlendirebileceği bir kümeye indirir. SilverTorch makalesi indeks ve filtrelerin ayrı hizmetler yerine model katmanları olarak birleştirildiğini; yaklaşık benzerlik araması ile uygunluk filtrelemesinin birlikte tasarlandığını açıklıyor. Bu Meta'nın farklı uygulamalarına hizmet eden altyapıdır. [F34](system-evidence-20261014.md).

**Araştırma çıkarımı:** İlgili aday olmak ile son sırada öne çıkmak farklı sorulardır. “Çok like aldı, dolayısıyla her ilgili kişiye gösterilir” sonucu bu çok aşamalı yapıyı atlar.

## Güncel modelden hangi özellikler doğrulanıyor?

| Açıklanan öğe | Doğrulanan işlev | Kaynak kapsamı |
| --- | --- | --- |
| Kullanıcı ilgi temsili | İlgilere yakın içerik arama | F30; genel Meta içerik altyapısı |
| İçerik indeksi | Adayların model içinde temsil edilmesi | F34; makale özeti/yöntem özeti |
| Uygunluk filtresi | Adayların koşullara göre elenmesi | F30/F34 |
| Birden fazla eylem tahmini | Adayların farklı beklenen tepkilerle değerlendirilmesi | F30 |
| İçerik türü | Feed'de fotoğraf/video/carousel bilgisinin girdi olması | F31, Haziran 2026 resmî indeks |
| Geçmiş etkileşim | Önerilerde yakın dönem takip ve etkileşimin kullanılması | F27, Haziran 2026 resmî indeks |

Bu tablo “her videonun her pikselinden şu ağırlık çıkıyor” gibi açıklanmamış bir ayrıntı eklemez. Eski kaynakta geçen bütün görsel/ses tanıma yöntemleri bugünkü Instagram kodu diye aktarılmadı.

## Yeni içerik nasıl havuza girer?

SilverTorch açıklaması indeks güncellemelerinin yeni içerik, değişen etkileşim özellikleri ve uygunluk bilgileri için akış halinde uygulanabildiğini anlatıyor. Dolayısıyla yeni yayınları aday havuzuna alma, her seferinde bütün modelin yeniden yayımlanmasını gerektiren bir işlem olarak tarif edilmiyor. [F30](system-evidence-20261014.md).

**Araştırma çıkarımı:** Yeni içeriğin başlangıçta az davranış verisi olması ile teknik olarak bulunamaz olması aynı şey değildir. Ancak bu mekanizma belirli bir yayına başlangıç gösterim kotası veya bütün hesaplara eşit erişim vaadi vermez.

## Konu ve izleyici eşleşmesi nasıl düşünülmeli?

Your Algorithm'ın Haziran 2026 güncellemesinin resmî indeksinde Feed, Reels ve Explore için konu tercihleri görülebiliyor. Feed Recommendations'ın güncel parçası da takip ve etkileşim geçmişini anıyor. [F29, F27](system-evidence-20261014.md).

**Araştırma çıkarımı:** “Sanat izleyicisi” tek bir davranış değildir. Bir resmin bütünü, üretim süreci veya anlatılan sahne farklı inceleme nedenleri sunabilir. Bu, üretim seçeneklerini karşılaştırmak için yazarın analitik örneğidir; platformun ilan ettiği kesin sanatçı/izleyici etiketleri değildir.

## Metin, hashtag, ses ve konum hakkında sınır

2021 arama rehberinin eski SEO ayrıntıları güncel sıralama kuralı olarak bu bölümden çıkarıldı. Güncel Search kartının görülen parçası, yazmaya başladıktan sonra çıkan bir hesabı açma ve ek eylem tahminini destekliyor. Anahtar kelime ağırlığı veya ideal hashtag sayısını açıklamıyor. [F11](system-evidence-20261014.md).

Trial Reels ürün belgesi ses/konum sayfası ve DM gibi başka karşılaşma yollarını gösteriyor; bu yolların varlığı tek başına algoritmik ağırlık değildir. [F13](system-evidence-20261014.md), 2025 güncellemeli ürün açıklaması.

**Tasarım önerisi, algoritma kuralı değil:** İçeriğin gerçek konusu, açıklaması ve profildeki devamı anlaşılır olmalıdır. Bu öneri iletişim tutarlılığına dayanır; belirli kelime veya etiket için doğrulanmış erişim artışı iddiası içermez.
