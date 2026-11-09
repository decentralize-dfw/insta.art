# Instagram algoritması — güncel kanıtlarla birleşik model

Son kontrol: 16 Ekim 2026. Güncel mekanizma için 2026 kaynakları önce gelir; 2025 kaynakları yalnız açık tarihleri ve destekledikleri sınırlı konularla kullanılır. 2020–2023 belgeleri güncel teknik ayrıntıların dayanağı olmaktan çıkarıldı. Eski kaynakların sicilde kalması bugünkü sistemi doğruladıkları anlamına gelmez.

## Doğrudan belgelenen model

Instagram, kullanıcı için aday içerikler seçer ve olası davranışları tahmin ederek sıralar. Haziran 2026 Feed kartının görülen parçaları içerik türünü girdi, diğer yayınlara göre geçme olasılığını tahmin olarak gösteriyor. Feed Recommendations kartı takip/etkileşim geçmişini, bilgilendiricilik değerlendirmesini ve üreticinin profilini açma olasılığını örnekliyor. Kartların tam metni bu araçta 429 verdi; buradaki kapsam yalnız resmî indekste görülen bilgilerdir. [F31, F27](system-evidence-20261014.md).

Mayıs 2026 SilverTorch açıklaması Meta'nın içerik öneri altyapısında ilgi benzerliğiyle aday arama, uygunluk filtreleri ve birden fazla eyleme ilişkin tahminlerin aday bulma içinde birlikte çalışabildiğini belgeliyor. Bu, genel Meta altyapısıdır; her Instagram yüzeyinin bütün kodunun tek model olduğu iddia edilmiyor. [F30](system-evidence-20261014.md).

## Karar katmanları

| Katman | Kaynakla söylenebilen bilgi | Dayanak |
| --- | --- | --- |
| Aday havuzu | Feed önerileri için kamusal Instagram içeriğinin bir bölümü toplanır | F27, Haziran 2026 indeks |
| Eşleştirme | İçerik adayları kullanıcının ilgisine yakınlık üzerinden aranabilir | F30, Mayıs 2026 tam metin |
| Uygunluk | Adaylar içerik politikası, dil/ülke gibi koşullarla filtrelenebilir | F30; genel altyapı, her yüzey için aynı kural listesi değil |
| Davranış tahmini | Farklı eylemler için ayrı tahminler kullanılır | F27/F31; ayrıca F30 genel altyapı |
| Sıralama | Aday bulmadan sonra sıralama katmanları vardır | F30; Instagram'a özel F02, Mayıs 2025 |
| Çeşitlilik | Bildirimlerde yakın geçmişe benzerliğe göre ek düzenleme bulunur | F06, Eylül 2025; doğrudan bütün Feed'e genellenmez |
| Açık tercih | Kullanıcı Feed/Reels/Explore konu tercihlerini değiştirebilir | F29, Haziran 2026 güncellemesinin resmî indeksi |

Tablo ortak bir araştırma şemasıdır. Kaynaklarda bütün bu kutuların her yüzeyde aynı sırayla ve aynı yazılımla çalıştığı açıklanmıyor. Bu ayrım teknik modeli kurmaya engel değildir: **aday seçimi → davranış tahmini → sıralama**, güncel kaynakların desteklediği çekirdektir. Uygunluk ve kullanıcı tercihleri bu seçimin koşullarına katılır. [F30, F31, F27, F29](system-evidence-20261014.md).

## Araştırmanın çıkarımları

Aşağıdaki sonuçlar doğrudan Meta kuralı değil, yukarıdaki mekanizmadan üretilen açık çıkarımlardır:

- Aday olmak ve adaylar arasında öne çıkmak farklı işlerdir. Yalnız toplam beğeniyle her kişiye dağıtım açıklanamaz.
- İçeriğin kişiye uygunluğu, üreticinin genel popülerliğiyle aynı kavram değildir. Aynı yayın farklı kişilerde farklı karşılık bulabilir.
- Profil açma, videoyu tüketme ve takip etme farklı sonuçlardır. İçerik tasarımı ve değerlendirme bu sonuçları ayrı tutmalıdır.
- Bir paylaşım doğrudan başka kişiye ulaşma yolu da olabilir. Bütün erişim yalnız öneri sıralamasından gelmez; native repost bunun belgelenmiş bir örneğidir. [F21](system-evidence-20261014.md).
- Gözlenen erişim bu seçimlerden doğar; tek bir toplamdan özel yayının bütün nedenleri teşhis edilemez.

## Kullanılabilir açıklama çerçevesi

**İçerik bilgisi ve adaylık:** Kişiye sunulabilecek yayınlar nasıl bulunuyor?

**Karşılaşma ve davranış:** O kişi yayınla ne yapabilir; hangi davranış inceleniyor?

**Yüzey ve dağıtım yolu:** Feed, Reels, arama, Story, arkadaş aktarımı veya reklam mı?

**Uygunluk ve tercih:** Hangi içerik/izleyici koşulları ve açık seçimler etkili?

**Sonuç:** Görme, tüketme, üreticiyi inceleme ve bağlantı kurma ayrı mı ölçülüyor?

Bu beş soru araştırmanın analiz düzenidir; evrensel etkileşim puanı değildir. Kaynakla doğrulanmış mekanizma ile yazarın içerik önerisi birbirinin yerine kullanılmaz.

## Okuma sırası

- [Yüzeyler ve görünür tahminler](system-surfaces-20261014.md)
- [İçerik bilgisi ve aday bulma](system-content-retrieval-20261014.md)
- [Dağıtım ve ölçüm](system-distribution-20261014.md)
- [Tarihli güncel değişiklikler](system-changes-20261014.md)
- [Reklam mimarisi](system-ads-20261014.md)
- [Kaynak ve kullanım sicili](system-evidence-20261014.md)
- [16 Ekim yeniden kontrolü](recheck-20261016.md)
