# Görev: Kopstal eserleri için Instagram Reel'leri

Bu prompt, Yiğit'in bilgisayarında çalışan üretim ajanı içindir. Kopstal'da (Lüksemburg)
yapılmış 2026 eserlerinin her biri için, bilgisayardaki arşivden sessiz Instagram Reel'leri
üreteceksin. Eserlerin dosya envanteri sende var. Her eserin klasöründe detaylar
(`details`), resim yapılırken çekilmiş aşama fotoğrafları (`process`, kadraja alınmış) ve
çoğunun yüksek çözünürlüklü dosyası bulunuyor.

Yiğit sonuçları kontrol edecek. Onaydan sonra Milano eserlerine geçilecek.
**Milano eserlerine dokunma. Hiçbir şeyi Instagram'a gönderme.**

---

## 0. Kesin kurallar (tartışmasız, Yiğit'in açık talimatı)

Bunlar `insta.art/.claude/instagram/voice.md` dosyasındaki kuralların özetidir. Çelişki
olursa `voice.md` geçerlidir.

1. **İki ayrı video türü vardır, asla tek videoda birleştirilmez:**
   - **Süreç videosu:** yalnızca resim yapılırken çekilmiş aşama fotoğrafları.
   - **Detay videosu:** yalnızca bitmiş resmin yakın detayları.
   Aynı eserin süreci ve detayı ayrı klasör, ayrı video olur.
2. **Süreç videosunda kamera HİÇ hareket etmez.** Her aşama fotoğrafı ve bitmiş resim beyaz
   alana **tamamen sığar** (kesilmez, kendi oranında). Her aşama 0,5 saniye. Sonda bitmiş
   resim beyaz alanda 2 saniye.
3. **Detay videosunda kamera HİÇ durmaz.** Her plan kesmeye kadar hareket eder. Sabit kalan
   tek an, sondaki en fazla 2 saniyedir.
4. **Her plan tek eksende hareket eder: ya yatay (x) ya dikey (y).** Çapraz kayma yok. Aynı
   planda kaydırma ve zoom birlikte yok. "Yamuk yumuk" hareket kesinlikle yok.
5. **Detay videosunda ara planların hepsi yakın plan.** Resmin tamamı arada gösterilmez.
6. **Detay videosunun son planı:** resmin ortasında yakından başlar, **merkezi sabit
   zoom-out** ile eser beyaz boş alana tam sığar, 2 saniye sabit kalır. Zoom yalnızca bu
   planda kullanılır.
7. Kesmeler 0,5 saniyelik ızgarada (120 BPM). Planlar genelde 2-2,5 saniye.
8. Instagram Reel formatı: 1080×1920, 30 fps, H.264, **ses kanalı yok** (müziği Yiğit
   uygulamadan ekler). **Ekranda hiçbir yazı yok.** Logo, başlık, altyazı, efekt, geçiş,
   renk düzeltmesi yok.
9. Eser esnetilmez, rengi değiştirilmez, kırpılmış hâli "resmin tamamı" diye gösterilmez.
10. Uydurma bilgi yok. Künye `works.json`'dan gelir.

## 1. Araç ve örnekler

`decentralize-dfw/insta.art` reposunun `claude/friendly-feynman-0pciu5` branch'ini çek. Bu
branch'te şunlar var:

- `tools/render.py`: üretim aracı. `python3 tools/render.py <klasör>/spec.json` videoyu,
  kapağı ve carousel sayfalarını üretir. Kaynak yolu olarak bilgisayardaki dosyanın yolunu
  yaz (mutlak yol ya da `spec.json`'a göre göreli yol).
  - Araç yukarıdaki kuralların çoğunu zorunlu tutar. Çapraz hareket, merkez dışı zoom,
    hareketsiz detay planı, kenara takılan kaydırma, süreç videosunda hareket ya da kırpma
    varsa video üretilmez. **Hata alırsan `spec.json`'ı düzelt, aracın kurallarını
    gevşetme.** Araçta gerçek bir hata bulursan düzelt ve raporda açıkça yaz.
  - Gereken: Python 3, Pillow, ffmpeg.
- `.claude/instagram/voice.md`: hesabın bütün kuralları. Önce bunu oku.
- **Yiğit'in onayladığı örnekler. Yeni videolar bunlarla aynı biçimde olmalı:**
  - Detay videosu: `posts/2026-11-21-gary-grills-cooper-details/` (`spec.json`, `reel.mp4`)
  - Süreç videosu: `posts/2026-11-14-gary-grills-cooper/`
  - Yüksek çözünürlüklü görselin içinde gezinme: `posts/2026-11-10-angora-mergvs/`

Örnek spec'lerdeki `"details:..."` ve `"yigit:..."` önekleri bulut ortamındaki repo
kopyalarını gösterir. Sen bilgisayardaki dosya yollarını kullan.

Künye, `description` ve `note` için: `yigit` reposundaki `v3/content/works.json` (ya da
bilgisayardaki kopyası). Rotayı planlarken `description` ve `note` alanlarını mutlaka oku.
Note, Yiğit'in resimde neyin önemli olduğunu söylediği yerdir.

## 2. Dosyası yoksa yapma

Her eser için önce dosyaları **gözünle** kontrol et (küçültülmüş bir temas sayfası yapıp bak).

- **Süreç videosu** ancak o esere ait, resim yapılırken çekilmiş **en az 4 aşama
  fotoğrafı** varsa yapılır.
  - Aşama olmayan görselleri **çıkar**: resmin dayandığı referans ya da basın fotoğrafı,
    başka bir eser, ekran görüntüsü, renk efekti uygulanmış sürüm. Örnek: gary'nin süreç
    klasöründeki ilk görsel oyuncunun basın fotoğrafıdır ve kullanılmadı.
  - Çıkardıklarını `notes.md` içinde gerekçesiyle yaz.
  - Aşamaları gerçek sıralarına göre diz. Dosya adındaki numara her zaman doğru sıra değildir,
    görüntüye bakarak doğrula.
- **Detay videosu** ancak şu durumda yapılır: genişliği en az 3000 piksel olan yüksek
  çözünürlüklü bir ana görsel **ya da** genişliği en az 2000 piksel olan en az 4 detay
  fotoğrafı varsa. Ayrıca son plan için resmin tamamını gösteren bir görsel olmalı.
- Şart sağlanmıyorsa **o videoyu üretme.** Raporda "atlandı" diye yaz ve neyin eksik olduğunu
  belirt. Eksiği başka bir şeyle doldurma (başka eser, düşük çözünürlüğü büyütme).
- Aynı görselin birden fazla kopyası varsa çözünürlüğü en yüksek olanı kullan.
- Adı ya da görüntüsü değiştirilmiş bir sürüm olduğunu düşündüren dosyaları kullanma (ör.
  renkleri çevrilmiş "inverted" dosya, efekt uygulanmış kopya).

## 3. Detay videosu: yüksek çözünürlüklü görselin içinde anlamlı gezinme

Kamera, yüksek çözünürlüklü dosyanın içinde yakın planda gezer. Ama **rastgele dolaşmaz.**
Her video, resmin kendi kompozisyonundan çıkan bir okuma rotası izler. Şu sırayla çalış:

1. **Resme bak.** Yüksek çözünürlüklü dosyanın küçültülmüş hâline ve detay fotoğraflarına
   bak. `description` ve `note` alanlarını oku.
2. **Rotayı yaz.** 5-9 ilgi noktası seç: yüz, el, ağız, nesne, iki figürün temas ettiği yer,
   bir figürün mekânla buluştuğu yer. Her biri için normalize koordinat (cx, cy) ve seçilme
   gerekçesi yaz. Noktaları bir okuma mantığıyla sırala:
   - Bir hareketin ya da bakışın yönünü izle. Ör. sarkan kol → parmakların değdiği basamak.
   - Ya da bir figürü yukarıdan aşağıya oku: baş → eller → nesne → ayaklar.
   - Ya da iki şey arasındaki ilişkiyi kur: figür → baktığı ya da tuttuğu şey.
   Rotayı `notes.md` içine tablo olarak yaz. Bu tablo Yiğit'in kontrol edeceği ilk şey.
3. **Rotayı planlara çevir.** Her plan, rotadaki bir noktadan aynı yatay ya da dikey hizadaki
   bir sonraki noktaya giden **tek eksenli** bir kaydırmadır.
   - İki nokta aynı hizada değilse araya bir kesme koy. Bir sonraki plan, rotanın devamını
     diğer eksende alır. Böylece rota "L" biçimli parçalarla ilerler.
   - Rota devam ediyorsa yeni plan, önceki planın bittiği yerden başlar.
   - Kaydırmanın bir başlangıç ve bir varış nesnesi olur. Plan süresinin üçte birinden
     fazlası boş zemin (tek renk alan) üzerinden geçmez.
   - Yatay bir görselde dikey kaydırma yapacaksan `cover` değerini yükselt (ör. 1,6). Aksi
     hâlde kamera kenara dayanır ve araç planı reddeder.
4. **Ölçek ve çözünürlük.** Plan içinde yakınlık sabit kalır. Ekrana düşen kaynak pencere
   mümkünse en az 1080×1920 piksel içermeli, yani görüntü büyütülmemeli. En fazla 1,25 kat
   büyütmeye izin var. Bir nokta ana görselde yeterince keskin değilse, aynı nokta için
   çekilmiş detay fotoğrafını kullan. Ana görsel üzerindeki planlar ile detay fotoğrafı
   planları aynı videoda karışabilir, rota sırası korunur.
5. **Bitiş.** Son plan: resmin tamamını gösteren en iyi görsel üzerinde merkezden yakın
   başla (`"cover"` 1,3-2,2), zoom-out ile `"fit": true`, `"hold": 2.0`, `"ease": "out"`,
   `"dur": 6.0`.
6. **Uzunluk.** 15-30 saniye. Rota kısa ise video kısa olur, plan uydurulmaz. Aynı noktaya
   iki kez gidilmez.
7. **Yön çeşitliliği.** Art arda gelen planlar aynı yönde akıp monotonlaşmasın. Rotanın
   izin verdiği ölçüde yatay ve dikey planları karıştır.

## 4. Süreç videosu

- `"camera": "static"`, her planda `{"cx": 0.5, "cy": 0.5, "fit": true}`, her aşama
  `"dur": 0.5`.
- Sonda bitmiş resmin tamamı `fit`, `"dur": 2.0`.
- Örnek: `posts/2026-11-14-gary-grills-cooper/spec.json`.

## 5. Çıktı

Her video için `insta.art` reposunda ayrı bir klasör:

```
posts/kopstal/<slug>-details/
posts/kopstal/<slug>-process/
```

`<slug>` = `works.json`'daki `slug`.

Her klasörde:

| dosya | içerik |
| --- | --- |
| `spec.json` | `tools/render.py` girdisi. Her planda kısa bir `"note"` (ne gösteriyor). |
| `reel.mp4` | `python3 tools/render.py posts/kopstal/<klasör>/spec.json` çıktısı |
| `cover.jpg` | aynı komut üretir (spec'te `"cover": {"src": ..., "fit": true}`) |
| `caption.txt` | aşağıdaki format, birebir |
| `alt.txt` | kuru, betimleyici İngilizce alt text. `description` alanına dayanır. Yorum yok. |
| `notes.md` | tür, süre, kullanılan dosyalar, **rota tablosu** (detay videosu için), çıkarılan görseller ve gerekçeleri, müzik için 2-3 hava önerisi |
| `review.jpg` | videodan eşit aralıklı 15 karelik yatay şerit (Yiğit hızlıca kontrol etsin diye) |

Kaynak görselleri repoya kopyalama. Yalnızca yukarıdaki dosyalar commit'lenir.

Caption formatı (başka hiçbir şey yazma):

```text
<works.json title, birebir>
<year> · <medium küçük harfle> · <height_cm> × <width_cm> cm
```

Painstaking için ikinci satır: `2026 · acrylic on canvas · triptych · 3 panels, each 40 × 30 cm`.
Emoji, hashtag, soru, açıklama, çağrı yok.

Doğrulama (her video için çalıştır, sonucu `notes.md`'ye yaz):

```bash
# detay videosu: donma yalnızca son 2 saniyede olmalı
ffmpeg -i reel.mp4 -vf "freezedetect=n=0.0005:d=0.15" -map 0:v -f null - 2>&1 | grep freeze_start
# süreç videosu: farklı görüntü sayısı = aşama sayısı + 1 olmalı (kamera hiç kıpırdamıyor)
ffmpeg -i reel.mp4 -vf "mpdecimate=hi=64*12:lo=64*5:frac=0.33" -f null - 2>&1 | grep -oE "frame= *[0-9]+" | tail -1
# ses kanalı olmamalı (yalnızca "video" yazmalı)
ffprobe -v error -show_entries stream=codec_type -of csv=p=0 reel.mp4
```

`review.jpg` şeridine kendin de bak. Bir planda boş zemin, kesilmiş bir yüz ya da anlamsız bir
kadraj görürsen spec'i düzelt ve yeniden üret.

## 6. Eserler (Kopstal, 2026)

Dosyaları kendi envanterinden bul. Aşağıdaki rota önerileri `works.json`'daki `description`
ve `note` alanlarından çıkarıldı. Bunlar başlangıç noktası. Resme bakınca daha iyi bir rota
görürsen onu kullan ve nedenini `notes.md`'ye yaz.

### 6.1 Painstaking
- Caption: `Painstaking` / `2026 · acrylic on canvas · triptych · 3 panels, each 40 × 30 cm`
- Rota önerisi: panelleri soldan sağa bir kez kur, sonra her yüzde gözlerden ağza (dikey).
  Ortadaki yüzde dişler. Sağ panelde koyu giysi ve kırmızı kravat. Panel sırasını bozma.
  Son plan: üç panelin birlikte durduğu triptik, beyaz alanda.

### 6.2 Angora Mergvs
- **Detay videosu zaten üretildi:** `posts/2026-11-10-angora-mergvs/`. Yeniden üretme.
- Süreç fotoğrafları varsa yalnızca süreç videosunu yap.

### 6.3 Gxd is AFK, We banned it
- Caption: `Gxd is AFK, We banned it` / `2026 · acrylic on canvas · 80 × 60 cm`
- Rota önerisi: soldaki yaşlı figürün açılmış eli → yukarı kalkan turuncu eller → sağdaki
  ortadan bölünmüş yüz (yatay). Sonra taşınan bedenin sarkan kolu boyunca aşağı, kırmızı uçlu
  parmakların basamağa değdiği yere (dikey). Sonra basamak boyunca taşıyanın okra ayakları →
  mor örtü (yatay). Elini ağzına bastıran türbanlı figür ayrı bir plan olabilir.

### 6.4 sept neuf
- Caption: `sept neuf` / `2026 · acrylic on canvas · 75 × 55 cm`
- Rota önerisi: sigaralı kalkık el → yüz: siyah halka içindeki beyaz disk göz → çizilmiş boş
  göz (yatay). Sonra elbiseyi veren sarı çizgi boyunca göğüsteki koyu kırmızı karelere
  (dikey). Sonra koltuğun koluna sarkan beyaz tırnaklar → bacaklar → beyaz ayakkabılar
  (dikey). Son olarak sehpadaki kuş, başı figüre dönük (yatay).
- Bu eserin gerçek fırça kayıtları (video) varsa onlar bu görevin kapsamı dışında. Süreç
  videosu yalnızca aşama fotoğraflarıyla yapılır.

### 6.5 7 fam board game
- Caption: `7 fam board game` / `2026 · acrylic on canvas · 80 × 100 cm`
- Rota önerisi: gözü ve ağzı olmayan büyük baş → karşısındaki öfkeli küçük baş (yatay, iki
  oyuncu). Küçük başın yakasından sarkan beyaz kordonlar boyunca taşlara (dikey). Sonra
  tahta boyunca: ambalajlı, birbirinden ayrı pembe koniler → iki üç kat üst üste yığılmış
  mavi başlar → sağ kenardaki kulaklı en yoğun yığın (yatay).

### 6.6 Virgil on Virtual Cage (final_final-finalV9)
- Caption: `Virgil on Virtual Cage (final_final-finalV9)` / `2026 · acrylic on canvas · 100 × 80 cm`
- Süreç klasöründeki ilk görsel (`00`) bir referans görsel olabilir. Kontrol et.
- Rota önerisi: beyaz peruğun altında yanağa giden el, perukta yukarıdan aşağı (dikey).
  Çizilmiş kafesin tavan çizgisi boyunca (yatay), bir dikmeden aşağı, dikmenin bittiği yere
  kadar (dikey). Soldaki küçük kıvırcık figür → sağdaki kanatlı sarışın figür (yatay). Sonra
  bacaklarını kaldırmış yatan gri saçlı figür ve mercan renkli fırça yatağı.

### 6.7 gary grills cooper
- **Zaten üretildi:** süreç `posts/2026-11-14-gary-grills-cooper/`, detay
  `posts/2026-11-21-gary-grills-cooper-details/`. Yeniden üretme.

### 6.8 walls of perception
- Caption: `walls of perception` / `2026 · acrylic on canvas · 70 × 50 cm`
- Rota önerisi: şapkanın kenarı → kenarın altından dökülen sarı tane sütunu boyunca aşağı,
  kâseye (dikey, videonun ana hareketi). Sonra kırmızı sekizgen örtü → lavanta çiçeği (yatay)
  → boncuklu gri alet.

### 6.9 articulo attack on mandarin
- Caption: `articulo attack on mandarin` / `2026 · acrylic on canvas · 80 × 80 cm`
- Rota önerisi: sürüdeki kuşlar boyunca (yatay; kuşlar çapraz uçuyor ama kamera yalnızca
  yatay gider) → direği tutan ince figür, direk boyunca aşağı (dikey) → teknenin kenarı
  boyunca X gözlü figürler ve STUGOTZ yazısı (yatay) → sol alttaki çapalar ve zincir.

### 6.10 s(t)lop
- Caption: `s(t)lop` / `2026 · acrylic on canvas · 75 × 55 cm`
- Rota önerisi: sol üstteki yuvarlak baş → gaga boyunca sağa → açık ağzın içindeki kırmızı
  çentikler (yatay). Sonra ince bacaklar boyunca alt kenara (dikey). Son olarak sağdaki
  çerçeveli panel → kutunun içindeki baş (dikey).

Envanterinde burada olmayan başka bir Kopstal (2026) eseri varsa aynı kurallarla onu da
yap ve raporda belirt.

## 7. Bitirince

1. Tüm klasörler `posts/kopstal/` altında olsun.
2. Commit'le ve push'la. Commit mesajında model adı yazma.
3. Şu raporu ver (Türkçe, kısa):

| eser | süreç videosu | detay videosu | süre | atlandıysa neden | açık soru |
| --- | --- | --- | --- | --- | --- |

4. Açık soruları ayrı listele (ör. "virgil süreç klasöründeki 00 referans görsel mi?").
   Emin olmadığın bir görseli kullanmak yerine dışarıda bırak ve sor.

Yapmayacakların: Milano eserleri, Instagram'a paylaşım, takvim ya da tarih atama, caption'a
künye dışında bir şey yazmak, `voice.md`'nin kurallarını değiştirmek, aracın kurallarını
gevşetmek.
