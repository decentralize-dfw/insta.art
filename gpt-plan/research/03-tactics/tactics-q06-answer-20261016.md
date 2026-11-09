# Soru 06 — Carousel: ilk kaydırmanın ve devamın gerekçesini kurmak
16 Ekim 2026. Üçüncü ayak / Oda 1. Kaynaklı araştırma cevabı; önerilen uygulama denenmedi. [Dizin](tactics-rooms-index-20261016.md) · [Genişletilmiş kaynak sicili](tactics-evidence-06-60-20261016.md).

**Okuma anahtarı:** Kaynakta anlatılan olay veya ürün işlevi bağlantıyla gösterilir. “Çıkarım”, “öneri” ve deney kararları bu çalışmanın akıl yürütmesidir; platformun açıkladığı kural veya elde edilmiş sonuç değildir.

## 1. Taktik ve somut uygulama

**Önerilen uygulama:** Carousel'i slayt sayısından başlayarak değil, çözülmesi gereken sorudan geriye kur. İlk slayt ne öğrenileceğini, ikinci slayt bu vaadin ilk somut karşılığını, devamı farklı adımları veya karşılaştırmaları, son slayt kullanılabilir sonucu versin. Örneğin bir ayar rehberinde önce “bu sorun nasıl düzelir”, sonra hata görüntüsü, doğru ayar ve kontrol sonucu gösterilebilir. Bu örnek özgün tasarımdır, ölçülmüş kazanan değildir.

İkinci giriş yalnız ilk başlığın tekrarı olmasın: ilk slaytı atlayarak başlayan birinin de bağlamı anlayabilmesini sağlamak ayrı bir tasarım hedefidir. Instagram'ın her carousel'i ikinci slayttan tekrar göstereceğine dair burada kural konmuyor. İşlevsiz slaydı sırf sayıyı tamamlamak için ekleme; her sayfaya yeni bir bilgi görevi yaz.

## 2. Mekanizma ve çıkarım

**Hipotez:** İlk slayt seçim, sonraki slaytlar devam etme kararı için farklı işler yapar. İlkini iyileştirmek bütünü daha çok kişiye açabilir; içeriği gerçekten kullandırmak ayrıca gövdeye bağlıdır. Bu ayrım kullanıcı anlatısından çıkarılmış deney mantığıdır; algoritmanın ayrı ayrı verdiği puanlar olarak sunulmuyor. [R10](https://www.reddit.com/r/InstagramMarketing/comments/1wjntza/spent_a_month_redesigning_only_the_first_carousel/)

## 3. Resmî açıklama ve kapsamı

Instagram'ın teknik açıklaması yüzeyleri ve sıralama katmanlarını ayırıyor. Belirli slayt sayısı veya “son slayta gelene bonus” yayımlamıyor. Carousel tasarım kararını bu kaynakla doğrulanmış eşik gibi yazamayız. [N01](https://engineering.fb.com/2025/05/21/production-engineering/journey-to-1000-models-scaling-instagrams-recommendation-system/)

## 4. Uygulayıcı deneyimi

İlk slaytını yeniden tasarladığını anlatan silinmiş Reddit yazarı daha kısa vaat, daha sade yerleşim ve yüksek kontrast kullandığını söylüyor. Kaydetme ve profil ziyaretinin arttığını bildiriyor; ham sayılar yok. Birlikte değişen kapak unsurlarının hangisinin katkı verdiği ayrışmıyor. [R10](https://www.reddit.com/r/InstagramMarketing/comments/1wjntza/spent_a_month_redesigning_only_the_first_carousel/)

## 5. Forum karşılaştırması ve karşı örnek

Mindless_Baseball308, Reels ile carousel dönüşümlü yayınında erişim ve takip/kaydetmenin aynı formatta kazanmadığını anlatıyor. Bu beyan carousel'in her hesapta üstün olduğunu göstermiyor. Kapak vakası tasarımı, bu vaka formatı karşılaştırıyor; ikisini tek başarı deneyi gibi birleştirmiyoruz. [R11](https://www.reddit.com/r/InstagramMarketing/comments/1wxiz97/i_ran_carousels_vs_reels_for_a_month_on_a_tiny/)

**İşlenen karar:** Önce aynı formatın girişini iyileştir; format değiştirme kararını daha sonra, hedef davranış ve üretim maliyetiyle al.

## 6. Kaynak kontrolü

R10/R11 ana metinleri ve ilgili yorumları okundu; tasarım dosyaları, hesap Insights'ları ve rastgele dağıtım kaydı yok. R10 yazarı silinmiş, R11 yayın günü belirsiz. N01 resmî teknik metin; tasarım reçetesi değil. Erişim ve tarih notları sicilde.

## 7. Sınırlar, emek ve başarısızlık

Slayt bazlı devam verisi görünmüyorsa son slayta kaç kişinin ulaştığını toplam erişimden hesaplama. Daha fazla kaydetme, son sayfanın okunduğunu tek başına göstermez. Görseli sadeleştirirken önemli ayrıntıyı kaybetmek de olası maliyettir.

Kapak yeniden yazımı, gövde yeniden düzenlemesi ve toplam slayt sayısını üç ayrı müdahale olarak tut. Aynı anda değiştirirsen öğrenme bir tasarım paketine aittir; tek unsura atfedilemez.

## 8. Deneme, ölçüt ve karar

İlk tur: aynı türde ve aynı gövde uzunluğunda içeriklerde yalnız kapak vaadi değişsin. İkinci tur: kapak ilkesini sabit tutup ikinci slaytın açıklık düzeyini değiştir. Yayın sırasını benzer konu çiftlerinde tersle; organik kitlelerin aynı olmadığını kaydet.

Aynı yayın yaşında erişim, kaydetme, paylaşım, atfedilen takip ve tasarım dakikasını tut. Varsa slayt verisini kendi tanımıyla ekle; yoksa N/A. Sonucu tek büyük posttan çıkarma. **Karar:** Kapak değişimi hedef sonucu tekrar artırıyorsa kullan; yalnız erişim yükselip kaydetme/eylem aynı kalıyorsa gövdeyi incele. Gövde sadeleşince emek azalıyor ve hedef sonuç korunuyorsa bu da kullanılabilir verim kazancıdır.

## Kaynak bağlantıları

- [N01 — Meta Engineering — Instagram model altyapısı](https://engineering.fb.com/2025/05/21/production-engineering/journey-to-1000-models-scaling-instagrams-recommendation-system/). Tam teknik metin. Yayın/güncelleme gözlemi: 21 Mayıs 2025.
- [R10 — Reddit — İlk carousel slaydını yeniden tasarlama](https://www.reddit.com/r/InstagramMarketing/comments/1wjntza/spent_a_month_redesigning_only_the_first_carousel/). Ana metin ve görünen yorum. Yayın/güncelleme gözlemi: Kesin gün teyitsiz; sayfa 17d ago.
- [R11 — Reddit — Mindless_Baseball308 / carousel vs Reels](https://www.reddit.com/r/InstagramMarketing/comments/1wxiz97/i_ran_carousels_vs_reels_for_a_month_on_a_tiny/). Ana metin ve ilgili yorum. Yayın/güncelleme gözlemi: Kesin gün teyitsiz; sayfa 15h ago; indeks göreli yaşından farklı.
