# Soru 7 — Performans teşhisi ve yeterli veri kararı

Denetim: 14 Ekim 2026 · Düzeltilmiş sürüm. Hesaba ait yeni Insights veya reklam deneyi yapılmadı.

## Önce ölçümün doğru olup olmadığını kontrol et

Hesapta yeni yayın ölçümü yok; aşağıdaki yöntem önerisidir. S048'in güncel tam Insights açıklaması giriş duvarında kaldı. Metrik adı, paydası, platform kapsamı ve atıf penceresi gerçek ekrandan kaydedilmelidir. S050'nin skip rate açıklaması güncel her hesapta retention grafiği bulunduğu anlamına gelmez.

Eksik metrik N/A'dır; sıfır değildir. Views tekrarları içerebilir; reach tekil hesap ölçümüdür ve platformun tahmin/metrik açıklaması korunur. Takipçi dışı yüzdesi views bazlıysa reach'e uygulanmaz. Organik/ücretli, Trial/normal/Collab ve birleşik Facebook–Instagram sonuçları ayrı tutulur. Aynı yayın yaşı ve benzer format/uzunluk karşılaştırılır.

## Gözlem, alternatif açıklama ve sonraki kontrol

| Gözlem | En az iki olası açıklama | Sonraki kontrol |
| --- | --- | --- |
| Düşük dış erişim | Uygunluk kısıtı; ilgi uyumu; küçük örneklem | Account Status, yayın yaşı ve benzer gönderiler |
| Erken izleme kaybı | Okunmayan açılış; uyumsuz izleyici; ses bağımlılığı | Varsa erken retention, ilk kareyi sesli/sessiz inceleme |
| Belirli yerde düşüş | Gereksiz bölüm; izleyicinin cevabı alması | Düşüş anını içerikteki olayla eşleştirme |
| İzleme iyi, paylaşım az | İçerik özel tüketiliyor; aktarma gerekçesi yok | Postun önceden belirlenmiş hedefi |
| Erişim var, profil ilgisi az | İçerik kendi içinde yeterli; hesap devamı belirsiz | Atıf alanı, profil vaadi, takipçi karışımı |
| Profil ziyareti var, takip az | Tekrar ziyaret; mevcut takipçi; profil uyumu | Aynı kullanıcı hunisi varsaymadan metrik açıklaması |
| Like çok, keşif az | Mevcut ilişkiler; küçük sevilen izleyici | Mutlak takipçi dışı erişim |
| Erişim artarken oran düşüyor | Kitle genişlemesi; ilgisiz yeni dağıtım | Mutlak ilgili eylem ve maliyet/üretim yükü |
| Tek yayın kötü | Konu/sunum veya rastlantı | Bütün hesap için hüküm kurma |
| Birçok yayın birlikte düşüyor | Ortak hesap/ölçüm koşulu; dönem etkisi | Değişiklik günlüğü ve uygunluk; platform arızasını ayrıca doğrula |

Düşük ortalama izleme tek başına ilk saniyelerde kayıp demek değildir. “İçerik kötü” veya “shadowban” bu tablodan otomatik çıkmaz. Veri ancak gözlenen sorunu daraltır; alternatiflerin etkisini ayıran karşılaştırma gerekir.

## Eksik bırakılmış konu: ne kadar veri yeterli?

Evrensel dört post, yedi gün veya 1.000 izlenme eşiği yok. Yeterlilik karar sorusuna bağlıdır: çok büyük bir farkı ayırmak daha az, küçük bir farkı ayırmak daha çok bilgi ister. Önceden birincil sonuç, pratik olarak anlamlı en küçük fark, karşılaştırma zamanı ve toplam araştırma maliyeti yazılır. Bu maliyete üretim zamanı da dahildir.

Varsayımsal örnek: 300 erişimde 3 kaydetme %1; 400 erişimde 8 kaydetme %2. Ham fark 5 olaydır. Bağımsız Bernoulli denemeleri varsayımı altında Wilson %95 aralıkları yaklaşık %0,34–2,90 ve %1,02–3,90'dır. Bu aralıkların örtüşmesi tek başına standart fark testi değildir; örnek küçük olduğunda belirsizliği gösterir. Gerçek Instagram erişimleri otomatik bağımsız deneme sayılmaz; aynı kullanıcı örtüşmesi, seçilmiş dağıtım ve eylem tanımı bu varsayımı bozabilir.

Planlama örneği: bağımsız, eşit büyüklüklü iki grupta gerçek olay oranı %1 ile %2 ise, iki yönlü %5 hata ve %80 güç için normal yaklaşım yaklaşık 2.320 kişi/grup ister. Bu bir Meta eşiği veya bu hesaba bütçe tavsiyesi değildir. Görüntülenme sayısını bağımsız kişi sayısı diye kullanmak geçersizdir. Organik post karşılaştırmasında atama birimi post olduğundan milyonlarca görüntülenme, iki postu milyonlarca bağımsız deney yapmaz.

Sıfır olayda da “oran sıfırdır” denemez. Yalnız bağımsız ve eşit olasılıklı n fırsat varsayımında tek yönlü %95 üst sınır 1 − 0,05^(1/n), yaklaşık 3/n'dir. Gerçek uygun fırsat sayısı bilinmiyorsa bu hesap kullanılmaz.

## Karşılaştırma ve tekrarlama

Yeni resim dönemi kendi başlangıç serisini oluşturur; eski web3 gönderileri doğrudan performans tabanı olmaz. Benzer yayınlarda medyan ve aralık başlangıç betimlemesidir, tahmin doğruluğu garantisi değildir. Medyan sıfırsa performans çarpanı hesaplanmaz. Çok küçük alt gruplarla sahte hassaslık yaratılmaz.

Eser, hook, saat ve format birlikte değiştiyse hangi unsurun etkili olduğu bilinmez. Bazı değişkenleri ortak tutup tek hipotez sınanır; farklı günlerdeki organik karşılaştırma yine keşif niteliğindedir. Birçok metrik/saat arasından yalnız iyi sonuçları seçmek yanlış pozitifleri artırır. Önceden seçilen ölçü ve süre korunur; erken teknik veya harcama hatası için müdahale bunun dışındadır.

## Karar kuralları

- Amaçla uyumlu sonuç farklı benzer içeriklerde tekrar ediyorsa yaklaşımı sürdür; otomatik olarak bütün ayrıntılarını kopyalama.
- Gözlenen belirli sorun ve sınanabilir alternatif varsa tek değişkeni revize et.
- Ölçüm yok veya belirsizlik karar verecek kadar dar değilse “yetersiz veri” yaz. Süre uzaması tek başına güven sağlamaz.
- Önceden kabul edilen maliyet sınırı dolduysa, istatistiksel kanıt beklemeden ekonomik nedenle durdurulabilir. “İşe yaramadığı kanıtlandı” yerine kararın gerekçesi yazılır.
- Gerçek uygunluk bildirimi varsa kapsamını incele; düşük sayı nedeniyle topluca silme veya eser değerini yargılama.

## Kayıt şablonu

Post ID; eser ID; sunum ID; yayın zamanı ve zaman dilimi; format/süre; hook; CTA; tek ana hedef; Trial/normal/Collab; boost zamanı; ölçüm yaşı; metriklerin ekrandaki adları ve paydaları; organik erişim; views; mevcut nonfollower sayısı; izleme/retention varsa; beğeni/kaydetme/paylaşma; özgün anlamlı yorum; atfedilmiş profil/takip varsa; dış paylaşım; en az iki alternatif açıklama; sonraki tek değişiklik; kararı değiştirecek gözlem.

24 saat ilk kayıt, 72 saat geçici teşhis, 7 gün kıyas, 14 gün geç dağıtım gözlemi operasyon seçimidir. Günlük net takip artışı tek gönderi etkisi değildir. [Kaynak sicili](audit-sources-20261014.md); sayısal örnekler gerçek hesap verisi değildir.
