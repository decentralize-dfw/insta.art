# Soru 3 — Paylaşım saati: farklı çalışmalar neden farklı sonuç veriyor?

Denetim: 14 Ekim 2026 · Düzeltilmiş sürüm. Hesaba ait yeni Insights veya reklam deneyi yapılmadı.

## Cevap

Bu hesap için doğrulanmış en iyi gün/saat yok. Önceki gün gün öneri takvimi kaldırıldı. Yayıncının veri setinde yüksek görünen saat, Luxembourg veya Milano'daki resim izleyicisinin optimum saati değildir.

## Kaynakların karşılaştırılması

| Kaynak | Veri dönemi ve örneklem | Ölçüm | Yorum sınırı |
| --- | --- | --- | --- |
| Sociality [S033], Ekim 2026 | Ağustos 2025–Temmuz 2026; 476.719 taranan, 335.210 organik gönderi; performans analizinde takipçi geçmişi bulunan 205.217 | Beğeni+yorum / takipçi, hesap ve format medyanına göre normalize; hesaplar eşit ağırlıklı | 20–24 saatleri medyanı %52, 9–17 saatleri %48,7 aşmış: fark 3,3 yüzde puan; erişim artışı değil |
| Buffer [S032], Eylül 2026 güncellemesi | Ocak 2024–Aralık 2025; 9,6 milyon Instagram gönderisi | Takipçiye bölünen etkileşimin medyanı; beğeni, yorum, paylaşım, kaydetme | Perşembe 09, Çarşamba 12 ve 18 gibi zirveler tarihsel örneklem sonucu; 2026 ölçümü değil |
| Sprout [S006], Mart 2026 | 27 Kasım 2025–27 Şubat 2026; 307 bin profil ve 2 milyar etkileşim altı platform toplamı | Etkileşim yoğunluğu; diğer iki çalışmanın hesap-normalize ölçüsüyle aynı değil | Pazartesi 14–16; Salı 13–19; Çarşamba 12–21; Perşembe 12–14 raporlanıyor. Bunlar bize atanmış saatler değil |

Sociality saatleri takip takımının zaman dilimi ayarına bağlı; örneklemin %59'u UTC. Bu ayar izleyicinin yerel saati olmak zorunda değil. İstanbul duyarlılık incelemesi Luxembourg'a doğrulama sağlamaz. Yöntemde 50 gönderi/15 hesap eşiği ile tabloda 500/100 eşiği arasında tutarsızlık var. Çok sayıda saat dilimi arasından en yüksek olanı sonradan seçmek tesadüfi zirveleri büyütebilir; belirsizlik aralığı yok.

Buffer'ın çok platformlu toplamını Instagram örneklemi olarak yazmıyoruz. Sprout'ın genel profil sayısını da Instagram'a mal etmiyoruz. Çalışmaların yayın tarihleri, veri dönemleri ve paydaları farklı; zirveleri ortalayıp tek bir “2026 doğru saat” üretmek geçersiz.

## Bu hesap için ölçüm tasarımı

1. Önce hedefi seç: yeni izleyici erişimi mi, anlamlı eylem mi? Saat etkisini beğeniyle ölçüp satış etkisi ilan etme.
2. Hesabın varsa takipçi aktiflik verisini başlangıç hipotezi olarak oku. Eski kitlenin aktifliği hedeflenen yeni kitlenin aktifliği değildir.
3. Uygulanabilir iki pencere seç; bunları araştırma bulgusu değil operasyon seçimi olarak etiketle. Europe/Luxembourg veya Europe/Rome gibi zaman dilimi ve UTC karşılığını kaydet; yaz saati değişimini hesaba kat.
4. Benzer format/uzunluk/amaçtaki içerikleri pencerelere önceden dengeli dağıt. Güçlü eserleri tek saate yığma; haftanın günüyle saat etkisini karıştırma.
5. Aynı yayın yaşında organik sonuçları karşılaştır. Reklam, Collab veya dış paylaşım varsa ayır. Tek iyi posttan saat kazananı çıkarma.

İçerik birebir aynı olsa bile farklı zaman ve izleyici, sonucu etkiler; bu tasarım keşif sağlar, gerçek rastgele kullanıcı deneyi değildir. Çok sayıda saat/ölçüm arasından yalnız başarılı olanı seçmek yerine ana ölçü ve karşılaştırmayı önceden yaz. Sonuç farkı üretim/iletişim düzenini değiştirmeye değmeyecek kadar küçükse pratik saat seçilebilir; istatistiksel üstünlük iddiası gerekmez.

Yeterli veri kararı ve kayıt alanları [Soru 7](alg-q7-diagnosis.md) içinde. Kaynakların tam adresleri [sicilde](audit-sources-20261014.md).
