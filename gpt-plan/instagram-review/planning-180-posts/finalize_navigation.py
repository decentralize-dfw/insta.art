from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parent.parent
old=ROOT/'publication-plan-180';backup=ROOT/'publication-plan-180-v3-superseded'
if not backup.exists():shutil.copytree(old,backup)
destinations={'PLAN-180.html':'VIZYON-VE-180-POST.html','KURASYON-GEREKCESI.html':'VIZYON-VE-180-POST.html#rules','ILK-14-GUN.html':'ILK-14-GUN.html'}
for filename,dest in destinations.items():
 (old/filename).write_text(f'''<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Güncel plan:180 ayrı gönderi</title><style>body{{font:18px/1.7 system-ui;max-width:850px;margin:70px auto;padding:24px;background:#f4f1e9;color:#252723}}h1{{font:44px Georgia}}a{{color:#4b5b36}}.box{{padding:24px;background:#fffdf7;border:1px solid #d8d7ca}}</style></head><body><p>yigitozen.art ·4Kasım2026</p><h1>Güncel çalışma:<br>180 ayrı gönderi.</h1><div class="box"><p>Önceki180günlük bölüm havuzu yerini ana vizyona, tek tek gerekçelendirilmiş180gönderiye ve ilk14günün ayrıntılı paketine bıraktı.</p><p><a href="../publication-plan-180-posts/{dest}">Güncel belgeyi aç →</a></p><p>Başlangıç düzeni haftada3yayın, yaklaşık60hafta. Eski sürüm tarihsel kayıt olarak korunuyor; bu klasördeki eski JSON/CSV dosyaları güncel uygulama planı değil.</p></div><p><a href="../publication-plan-180-v3-superseded/{filename}">Önceki v3 belgeyi incele</a></p></body></html>''',encoding='utf8')
summary=ROOT/'INCELEME.md'
text=summary.read_text(encoding='utf8')
marker='**Sonraki kullanıcı düzeltmesi:**'
tail=text[text.index(marker):] if marker in text else text
intro='''# yigitozen.art — güncel çalışma

**4 Kasım 2026 · Güncel kapsam: 180 ayrı gönderi.** Kullanıcı180gün yerine180ayrıgönderiyi doğruladı. Okuma sırası: [Ana vizyon ve180gönderinin tek tek gerekçesi](publication-plan-180-posts/VIZYON-VE-180-POST.html) → [İlk14günün ayrıntılı üretim kartları](publication-plan-180-posts/ILK-14-GUN.html) → [Profil ve künyeli seçki girişi](publication-plan-180-posts/PROFILE-ENTRY.html).

Başlangıç düzeni haftada3yayın;60hafta,sonyayınGün418. Her gönderide amaç,eser,kaynak,sıra,yeni inceleme değeri,İngilizce caption ve ölçüm işi var. İlk14gündeGün1/3/5/8/10/12:Angora,Gary,Cellular,Sept,Painstaking,Ciao çalışma aşaması. İki Reel için yeni İngilizce ses kaydı gerekiyor; medya renderlenmedi ve yayın yapılmadı. Reklam başlangıcı atanmadı.

[Yapılandırılmış180gönderi](publication-plan-180-posts/PLAN-180-POST.json) · [Doğrulama](publication-plan-180-posts/VALIDATION.json) · [Kaynak düzeltmeleri](publication-plan-180-posts/KAYNAK-DUZELTMELERI.json). İlk üç strateji sürümü ve aşağıdaki90günlük metinler tarihsel kayıttır; güncel180gönderi planının yerine kullanılmamalı. Yeni kaynak/sonuçlar geldiğinde ileri kartlar gerekçeleriyle revize edilir.

---

'''
summary.write_text(intro+tail,encoding='utf8')
(ROOT/'publication-plan-180-posts/OKUMA-SIRASI.txt').write_text('1. VIZYON-VE-180-POST.html\n2. ILK-14-GUN.html\n3. PROFILE-ENTRY.html\n\n180 posts, not180days. Public text English; planning rationale Turkish. All media remains unrendered/unpublished.\nGenerator: ../planning-180-posts/build.py\nDo not run the old build_180.py/build_180_v2.py/build_180_v3.py to replace the current plan.\n',encoding='utf8')
print('Current entry links updated; old v3 preserved.')
