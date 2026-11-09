import json,html,re,collections,sys
from pathlib import Path
from urllib.parse import quote,unquote,urlparse
from first14 import DETAILS,DAY_TASKS
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
OUT=ROOT/'instagram-review/publication-plan-180-posts'
OUT.mkdir(exist_ok=True)
(OUT/'texts').mkdir(exist_ok=True)
load=lambda p:json.loads(p.read_text(encoding='utf8'))
save=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
brief=load(HERE/'brief.json');catalog=load(HERE/'source-catalog.json');works=catalog['works']
assets={x['id']:x for x in load(ROOT/'archive-audit/audit-files.json')}
cover_manifest=ROOT/'instagram-review/grid-cover-design/covers.json'
covers={c['n']:c for c in load(cover_manifest)['covers']} if cover_manifest.exists() else {}
parts=[load(HERE/f'posts-{a:03}-{b:03}.json') for a,b in [(1,60),(61,120),(121,180)]]
posts=sorted(sum(parts,[]),key=lambda p:p['n'])
filming=load(HERE/'new-filming-decisions.json')
for change in filming:
 p=next(x for x in posts if x['n']==change['n'])
 p['fallback']={'format':p['format'],'title_en':p['title_en'],'caption_en':p['caption_en'],'idea_tr':p['idea_tr'],'production_tr':p['production_tr'],'reason':'Yeni kayıt üretilemezse aynı soru ve kaynaklarla mevcut sabit görsel taslağı.'}
 p.update({k:v for k,v in change.items() if k not in ['n','benefit_tr']})
 p['format']='Reel';p['sound']='english_voice';p['requires_new_capture']=True
 if p['n']==134:
  p['fallback']['format']='Carousel';p['fallback']['idea_tr']='Tam eser ile aynı masterdan kol/beden birleşmesini gösteren tek detay; iki sayfa, doğru konum işareti.'
 p['new_value_tr']+=' '+change['benefit_tr']
 p['tactics']=list(dict.fromkeys(p['tactics']+['T03','T46']))
 if p['goal']=='G1':p['check_tr']='Takipçi dışı erişim ve varsa gönderiye atfedilen takip; açıklanan kenar/alan/beden ilişkisine ilişkin gerçek devam soruları. Yalnız görüntülenme kazanımı yeterli değil.'
for p in posts:
 if 'baby' in p['works']:
  p['production_tr']+=' Baby Rights: kaynak fotoğrafın oranı katalogdaki80×100cm oranıyla birebir eşleşmiyor; resmi ölçüye uydurmak için esnetme. Künye katalog beyanı; fiziksel teyit ayrı.'
cover_corrections_path=ROOT/'instagram-review/grid-cover-design/content-corrections.json'
cover_corrections=load(cover_corrections_path) if cover_corrections_path.exists() else []
for change in cover_corrections:
 p=next(x for x in posts if x['n']==change['n'])
 p.update(change['replacements'])
 p['cover_source_review']=change['source_evidence']
 for f in filming:
  if f['n']==change['n']:
   f.update({k:v for k,v in change['replacements'].items() if k in f or k in ['assets','fallback']})
E=lambda x:html.escape(str(x))
REF='https://github.com/decentralize-dfw/u320x/blob/23e3dd0cb7effcaec2904d5ddeb49e9888abb0a5/instagram/'
studies={'A0001','A0004','A1696','A1718','A2763','A2795'}
def url(p):return Path(p).as_uri()
def thumb(i):return '../../archive-audit/'+('video-sheets/' if assets[i]['kind']=='video' else 'thumbs/')+i+'.jpg.webp'
def credit(k):
 w=works[k]
 if k=='society':return 'Study from the society screwing balance archive.\nStudy image undated.'
 if w.get('panel_count'):return f"{w['title']}\n{w['year']} · {w['medium']}\nTriptych · 3 panels, each 40 × 30 cm (h × w)."
 return f"{w['title']}\n{w['year']} · {w['medium']}\n{w['height_cm']} × {w['width_cm']} cm (h × w)."
def fullcaption(p):
 if p['n']==6:return DETAILS[6]['caption_en']
 s=p['caption_en']
 if all(i in studies for i in p['assets']):
  if 'undated' not in s.lower():s+='\n\nStudy image undated.'
  return s
 return s+'\n\n'+'\n\n'.join(credit(k) for k in p['works'])
def refs(p):
 rs=[('Ayak4: içerik kararı',REF+'04-strategy/strategy-content-playbook-20261016.md'),('Yerel eser audit',url(ROOT/'archive-audit/ARSIV-AUDIT.html'))]
 for t in p['tactics']:
  m=re.fullmatch(r'T(\d+)',t)
  if m:
   n=int(m[1]);name={3:'tactics-q03-hooks-20261016.md',4:'tactics-q04-retention-20261016.md'}.get(n,f'tactics-q{n:02}-answer-20261016.md')
   rs.append((t,REF+'03-tactics/'+name))
 return rs
for p in posts:
 n=p['n'];p['id']=f'P{n:03}';p['week']=(n-1)//3+1;p['day']=(p['week']-1)*7+[1,3,5][(n-1)%3]
 p['time']='19:00';p['timezone']='Europe/Paris';p['detailed']=n<=6
 p['status']='editorial_draft_not_rendered_or_published'
 p['actual_published_at']=None
 p['source_files']=[{'id':i,'path':assets[i]['path'],'kind':assets[i]['kind']} for i in p['assets']]
 p['requires_new_capture']=p['format']=='Reel' and not any(assets[i]['kind']=='video' for i in p['assets'])
 p['research_links']=refs(p)
 if n in DETAILS:
  p['details']=DETAILS[n];p['caption_en']=DETAILS[n]['caption_en']
 if n in covers:
  p['cover']=covers[n]
  p['cover_status']='local_cover_rendered_platform_preview_pending'
  if 'details' in p:p['details']['cover_en']=covers[n]['headline_en']
 p['caption_with_credit_en']=fullcaption(p)
 p['music']={'track':None,'decision':'No music in this draft; English narration where assigned, otherwise visual reading. This is an editorial decision, not a claimed ranking advantage.'}
 (OUT/'texts'/f'{p["id"]}-EN-CAPTION.txt').write_text(p['caption_with_credit_en']+'\n',encoding='utf8')

def srt_time(s):return f'{int(s)//3600:02}:{int(s)%3600//60:02}:{int(s)%60:02},000'
for n,d in DETAILS.items():
 prefix=f'P{n:03}'
 if d.get('voice_en'):(OUT/'texts'/f'{prefix}-EN-VOICE.txt').write_text(d['voice_en']+'\n',encoding='utf8')
 if d.get('subtitles'):
  txt='\n\n'.join(f'{j}\n{srt_time(a)} --> {srt_time(b)}\n{s}' for j,(a,b,s) in enumerate(d['subtitles'],1))+'\n'
  (OUT/'texts'/f'{prefix}-EN-DRAFT.srt').write_text(txt,encoding='utf8')
 if d.get('slides'):
  (OUT/'texts'/f'{prefix}-EN-SLIDES.txt').write_text('\n\n'.join(f"Slide {s['n']} · {s['asset']}\n{s['text']}" for s in d['slides'])+'\n',encoding='utf8')

phase_titles=['Hesabın vaadini görünür kıl','Bir esere neden yeniden bakılır?','Farklı girişler, aynı pratik','Eserler birlikte ne söylüyor?','Zamandaki süreklilik ve fark','İncelenebilir üç seçki ve devam']
phase_outputs=[
 'Tek bir popüler figür hesabı değil, beden/sahne/mekân soruları olan ressam profili. P030 üç alanı doğru künyelerle aynı girişte toplar.',
 'İzleyici yalnız tanımakla kalmaz: kontur, hacim, nesne ve çevre hakkında somut fark görebilir. P060 beden seçkisi bu bakışı kullanılabilir hale getirir.',
 'Kültürel kaynak ve kişisel bağlam, daha geniş girişler sunar; her giriş kendi resmindeki dönüşüme geri döner. Referans ilgisi ile esere devam ayrılır.',
 'Tek resimden ilişkili iş gövdesine geçiş: aynı sorunun iki farklı eserdeki karşılıkları, gerçek nesne/ölçü bilgileriyle incelenebilir olur.',
 '2019/2020/2023/2026 işleri kronolojik başarı merdiveni yapılmaz. Nelerin sürdüğü ve hangi çözümün farklılaştığı görsel kanıtla gösterilir.',
 'Beden, sahne ve mekân için kısa, künyeli seçkiler oluşur. Son yayınlar geçmişi kapatan bir final değil, bu seçkilere yeni inceleme girişleridir.'
]
metrics={
 'G1':{'name':'İlgili keşif','primary':'Varsa gönderiye atfedilen takip; takipçi dışı erişim ile birlikte.','secondary':'Paylaşım/erişim; izleme alanları yalnız platformda görülen tanımlarıyla.','decision':'Erişim var, devam yoksa vaat–eser–profil bağını düzelt. Salt görüntülenmeye göre aynı karakteri çoğaltma.'},
 'G2':{'name':'Pratiğin tanınması','primary':'Birden fazla esere ilişkin somut gözlem, benzerlik/fark sorusu.','secondary':'Profil ziyareti ve ilgili takip, kapsamı biliniyorsa.','decision':'Yalnız referans karakter konuşuluyorsa sıradaki içerikte biçimsel kanıtı görünür kıl. Sessiz izleyiciyi ilgisiz sayma.'},
 'G3':{'name':'Tekrar inceleme ve devam','primary':'Kaydetme/erişim, esere özgü farklı kişi soruları; gerçek devam talebi.','secondary':'İlgili paylaşımlar ve post düzeyinde mevcut takip alanı.','decision':'Aynı iddia yeni crop ile dönüyorsa çıkar. Yeni resim/karar/karşılaştırma yoksa slotu ertele.'},
 'G4':{'name':'Portföy ve eser incelemesi','primary':'İzlenebilen seçki erişimi, gerçek ölçü/malzeme/ziyaret/proje/edinme talebi.','secondary':'Talebin ilerleyişi; inceleme, rezervasyon ve satış ayrı.','decision':'Ulaşılan seçki ile gönderi vaadi eşleşmiyorsa yolu düzelt. Meslek unvanını talep veya satın alma niyeti sayma.'}
}
principles=[
 ('Vizyon eserden önce gelir','Önce hesabın hangi pratiği görünür kılacağı ve hangi karşılığı aradığı belirlenir; eser bu işi yapabildiği için seçilir. En iyi video dosyasına sahip olmak tek başına açılış hakkı vermez.'),
 ('Bir bağ kur; sonraki eserde genişlet veya sınırını göster','Gary → Cellular kütle ilişkisi; Board → Virgil → Capricorn sahne/çevre ilişkisi. Sıra için yalnız renk çeşitliliği veya format dönüşümü yeterli değil.'),
 ('Her yayın tek başına tamamlanır','Takipçi akışı bu sırayla görmeyebilir. Önceki postu izleme zorunluluğu, saklanan cevap veya yapay part2 yok. Sıra, birlikte bakıldığında ek ilişki kurar.'),
 ('Arşiv ana anlatının parçası','Her üç yayınlık haftada bir veya iki eski eser/çalışma var. Arşivin işi tarih göstermek, karşılaştırmak veya farklı çözüm sunmak; yeni işin arasında boşluk doldurmak değil.'),
 ('Aynı esere dönmenin bedeli yeni bilgidir','Yeni kaynak, somut farklı karar, fiziksel nesne bilgisi veya gerekçeli yeni karşılaştırma gerekir. Sadece crop, efekt, dosya adı, video hızı ya da başlık değişikliği yeterli değil.'),
 ('Format soruyu taşır','Gerçek hareket/anlatı/konuşma varsa Reel; karşılaştırma ve gerçek aşamalar için carousel; kendi başına incelenen güçlü eser veya eskiz için tek görsel. Fotoğraf slaytı Reel kotasına yazılmaz.'),
 ('Düzen sabit; eser ataması revize edilebilir','Bu180 satırın tamamı seçilmiş ve gerekçelendirilmiş taslak. Gerçek sonuç veya yeni eser gelince hedef, kaynak ve sıra gerekçesi korunarak kayıtlı değişiklik yapılır; rastgele boşluk doldurulmaz.')
]
plan={'version':4,'scope':'180 separate posts','language':'English public text; Turkish planning rationale','created':'2026-11-04','start_date':None,'post_count':180,'baseline_posts_per_week':3,'weeks':60,'last_post_day':418,'first14_post_days':[1,3,5,8,10,12],'vision':brief['vision_tr'],'promise_en':brief['promise_en'],'goals':metrics,'principles':principles,'phase_titles':phase_titles,'phase_outputs':phase_outputs,'phase_allocation_basis':'30-post blocks are editorial management checkpoints; not algorithm evidence or isolated topic months. Every block retains all three pillars.','growth_goal':{'target':5000,'type':'organic and relevant followers','original_deadline_day':90,'baseline':None,'achievability_verified':False,'extended_by_180_post_scope':False},'advertising':{'activated':False,'activation_day':None,'committed_spend_eur':0,'previous_total_ceiling_eur':390,'readiness':'Organic publication baseline and working profile/portfolio first. No invented day when the algorithm settles. Campaign decision separate.'},'music_policy':'Explicit none for now; English narration or reading. No trending-sound or silence-performance claim.','measurement_ages_hours':[24,72,168],'first14_daily_work':[{'day':d,'task':t} for d,t in DAY_TASKS.items()],'posts':posts,'rendered_media':False,'published_media':False,'new_english_recording_required_first14_posts':['P001','P004']}
plan['rendered_covers']=len(covers)
plan['cover_review']='../grid-cover-design/GRID-VE-KAPAKLAR.html' if covers else None
plan['finished_post_media_complete']=False
plan['cover_source_corrections']=[x['n'] for x in cover_corrections]
save(OUT/'PLAN-180-POST.json',plan)
save(OUT/'YENI-CEKIMLER.json',filming)
save(OUT/'KAYNAK-DUZELTMELERI.json',load(HERE/'source-corrections.json'))
save(OUT/'ILK-14-GUN.json',{'scope':'6 posts in14days','days':plan['first14_daily_work'],'posts':posts[:6]})
if not (OUT/'OLCUM.json').exists():
 save(OUT/'OLCUM.json',{'baseline_followers':None,'baseline_date':None,'current_account_insights_read':False,'entries':[{'post_id':p['id'],'planned_day':p['day'],'published_at':None,'observations':[{'planned_age_hours':h,'actual_observed_at':None,'reach':None,'nonfollower_reach':None,'shares':None,'saves':None,'attributed_follows':None,'work_specific_questions':None,'production_minutes':None} for h in [24,72,168]]} for p in posts]})
save(OUT/'KAYNAK-KULLANIMI.json',[{'asset_id':i,'path':assets[i]['path'],'posts':[p['id'] for p in posts if i in p['assets']]} for i in dict.fromkeys(i for p in posts for i in p['assets'])])

STYLE='''
@font-face{font-family:'Hanken Grotesk';font-style:normal;font-weight:100 900;font-display:swap;src:url('../grid-cover-design/fonts/hanken-normal-latin-ext.woff2') format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:'Hanken Grotesk';font-style:normal;font-weight:100 900;font-display:swap;src:url('../grid-cover-design/fonts/hanken-normal-latin.woff2') format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
:root{--paper:#fff;--ink:#000;--muted:#000;--line:#000;--accent:#000;--white:#fff}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.65 'Hanken Grotesk',Arial,sans-serif}main{max-width:1320px;margin:auto;padding:38px 32px 100px}a{color:#000;text-underline-offset:3px}h1{font:500 clamp(28px,3.6vw,48px)/1.16 'Hanken Grotesk',Arial,sans-serif;max-width:1050px;margin:22px 0}h2{font:500 28px/1.2 'Hanken Grotesk',Arial,sans-serif;margin:0 0 20px}h3{font-size:21px;line-height:1.35;margin:20px 0 9px}.eyebrow,.tag{font-size:12px;letter-spacing:.07em;text-transform:uppercase;color:var(--muted)}.lead{font-size:22px;max-width:1020px;line-height:1.5}.note{border-left:3px solid var(--accent);padding:12px 20px;background:#fff}.muted,small{color:var(--muted)}nav{display:flex;gap:12px;flex-wrap:wrap;margin:28px 0}nav a,.pill{border:1px solid var(--line);padding:8px 14px;border-radius:0;text-decoration:none;background:var(--white)}section,.post{margin:30px 0;padding:28px;background:var(--white);border:1px solid var(--line);border-radius:0}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}.goals{grid-template-columns:repeat(4,minmax(0,1fr))}.box{padding:20px;border:1px solid var(--line);background:var(--white)}.box h3{margin-top:0}.stats{display:flex;gap:22px;flex-wrap:wrap;margin:30px 0}.stats strong{font:36px 'Hanken Grotesk',Arial,sans-serif;display:block}.stats div{border-right:1px solid var(--line);padding-right:25px}.post header{display:grid;grid-template-columns:150px 1fr;gap:24px}.post header img{width:150px;height:160px;object-fit:contain;background:#fff}.post h3{margin:4px 0 9px;font-size:25px}.reason{display:grid;grid-template-columns:1fr 1fr;gap:24px}.reason p{margin:10px 0}.badge{display:inline-block;padding:2px 8px;background:#fff;font-size:12px;margin:0 6px 8px 0}.post details{border-top:1px solid var(--line);margin-top:18px;padding-top:14px}summary{cursor:pointer;font-weight:500}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:16px/1.6 'Hanken Grotesk',Arial,sans-serif;padding:22px;background:#fff;border:1px solid var(--line)}.sources{display:flex;gap:12px;flex-wrap:wrap}.assets{display:flex;gap:15px;flex-wrap:wrap}.assets img{width:180px;height:170px;object-fit:contain}.assets a{max-width:200px;overflow-wrap:anywhere;font-size:12px}.assets span{display:block}.table-wrap{overflow-x:auto}table{width:100%;border-collapse:collapse}td,th{border-bottom:1px solid var(--line);padding:12px;text-align:left;vertical-align:top}th{font-size:13px;color:var(--muted)}.filters{display:flex;gap:12px;flex-wrap:wrap;padding:18px;background:#fff}input,select{font:inherit;padding:9px;border:1px solid #000;max-width:100%}input{flex:1;min-width:230px}.hidden{display:none!important}.slides{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}.slide{background:#fff;border:1px solid var(--line);padding:16px;aspect-ratio:4/5;display:flex;flex-direction:column;justify-content:center;gap:14px}.slide img{width:100%;height:78%;object-fit:contain}.slide p{font-size:15px;line-height:1.35;margin:0}.back{font-size:13px}footer{padding-top:30px;color:var(--muted);font-size:13px}.caption{max-width:850px}.toc a{display:block;padding:9px 0}.evidence{font-size:14px}.titleblock{max-width:960px}.work img{height:270px;max-width:100%;object-fit:contain}.work{text-align:center}.work h3{font-size:19px}.work pre{text-align:left;font-size:14px}.positive{color:#000}@media(max-width:900px){.grid,.goals{grid-template-columns:1fr 1fr}.slides{grid-template-columns:1fr 1fr}.reason{grid-template-columns:1fr}}@media(max-width:600px){main{padding:20px 15px 60px}section,.post{padding:18px}.grid,.goals{grid-template-columns:1fr}.post header{grid-template-columns:85px 1fr;gap:14px}.post header img{width:85px;height:105px}.post h3{font-size:21px}.lead{font-size:19px}.slides{grid-template-columns:1fr 1fr}.slide{padding:8px}.slide p{font-size:12px}h2{font-size:28px}}@media print{nav,.filters,details:not([open]){display:none}body{background:white}section,.post{break-inside:avoid}main{max-width:none;padding:10px}.post{margin:12px 0}.grid{display:block}}
strong,b{font-weight:500}.steps button[aria-current=true]{border-width:2px}.tile.unknown{background:#fff;border:1px dashed #000}.covervisual img{box-shadow:none}.profilegrid{background:#fff}

'''
def head(title):return f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><style>{STYLE}</style></head><body><main id="top">'
NAV='<nav><a href="VIZYON-VE-180-POST.html">1 · Vizyon →180gönderi</a><a href="ILK-14-GUN.html">2 · İlk14gün</a><a href="PROFILE-ENTRY.html">3 · Profil ve seçki girişi</a><a href="../grid-cover-design/GRID-VE-KAPAKLAR.html">4 · 180 kapak ve grid</a><a href="PLAN-180-POST.json">Tüm karar verisi</a></nav>'
FOOT='<footer>Yerel planlama belgesi ·4Kasım2026 · Araştırma snapshot:23e3dd0c. Kaynak sanat görselleri RESSAMS arşivinden. Bu çalışma yeni yayın, ses kaydı, reklam veya büyüme sonucu değildir. HTML kaynak ve bağlantıları kontrol edildi; tarayıcı görsel önizlemesi bu oturumda doğrulanmadı.</footer></main></body></html>'
def assetlinks(p):return '<div class="sources">'+''.join(f'<a href="{E(url(assets[i]["path"]))}">{i} · {E(Path(assets[i]["path"]).name)}</a>' for i in p['assets'])+'</div>'
def gallery(p):return '<div class="assets">'+''.join(f'<a href="{E(url(assets[i]["path"]))}"><img loading="lazy" src="{E(thumb(i))}" alt="{E(i)}"><span>{E(i)} · {E(Path(assets[i]["path"]).name)}</span></a>' for i in p['assets'])+'</div>'
def postcard(p):
 k=p['works'][0];im=works[k]['master'];goal=metrics[p['goal']]['name'];pill={'body':'Beden/yüz','scene':'Sahne','space':'Mekân/bellek'}[p['pillar']]
 # For a study-only post show its actual study, not the final painting.
 if p['assets'][0] in studies:im=p['assets'][0]
 textsearch=' '.join([p['id'],p['title_en'],p['why_tr'],p['order_tr']]+[works[w]['title'] for w in p['works']]).lower()
 cover_src=f'../grid-cover-design/tiles/{p["id"]}.png' if p['n'] in covers else thumb(im)
 h=f'<article class="post" id="{p["id"]}" data-phase="{p["phase"]}" data-goal="{p["goal"]}" data-search="{E(textsearch)}"><header><img loading="lazy" src="{E(cover_src)}" alt="{E(works[k]["title"])}"><div><p class="eyebrow">{p["id"]} · Hafta{p["week"]} · Gün{p["day"]} ·19.00 Europe/Paris</p><h3 lang="en">{E(p["title_en"])}</h3><span class="badge">{E(p["format"])}</span><span class="badge">{E(pill)}</span><span class="badge">{p["goal"]} ·{E(goal)}</span>'+('<span class="badge">Tarihli arşiv / çalışma</span>' if p['archive'] else '')+f'<p>{E(" · ".join(works[w]["title"] for w in p["works"]))}</p></div></header>'
 if p['n'] in covers:h+=f'<p><a href="../grid-cover-design/GRID-VE-KAPAKLAR.html#P{p["n"]:03}">Tasarlanmış kapak, kaynak seçimi ve grid görünümü →</a></p>'
 h+=f'<div class="reason"><p><b>Neden bu eser?</b><br>{E(p["why_tr"])}</p><p><b>Neden burada?</b><br>{E(p["order_tr"])}</p></div>'
 h+='<details><summary>Fikir, yeni değer, kaynak, caption ve ölçüm</summary>'
 for lab,key in [('Nasıl yapılacak','idea_tr'),('Öncekinden farklı bilgi','new_value_tr'),('Üretim ihtiyacı','production_tr'),('Kanıt','evidence'),('Neye bakılacak','check_tr')]:h+=f'<p><b>{lab}:</b> {E(p[key])}</p>'
 h+=f'<p><b>Ses/müzik:</b> {E({"none":"Müzik yok; görsel inceleme veya İngilizce ekran metni.","english_voice":"Yeni İngilizce anlatım; müzik yok. Kayıt/render yapılmadı.","original_studio":"Gerçek stüdyo sesi; anlaşılır İngilizce metin gerekli. Arka plan medyası varsa temizlenmeden kullanılmaz."}.get(p["sound"],p["sound"]))}</p>'
 if p.get('requires_new_capture'):h+='<p class="note"><b>Yeni çekim gerekli.</b> Bu kartın hareketli görüntüsü mevcut arşivde hazır değil; üretim tarifi yukarıda. Fiziksel eser gereken çekimler erişime bağlı.</p>'
 if p.get('fallback'):h+=f'<p><b>Çekim yapılamazsa tanımlı yedek:</b> {E(p["fallback"]["format"])} · {E(p["fallback"]["idea_tr"])}</p>'
 h+=assetlinks(p)+f'<pre lang="en" class="caption">{E(p["caption_with_credit_en"])}</pre><p><a href="texts/{p["id"]}-EN-CAPTION.txt">English caption dosyası</a></p><p class="evidence">'+ ' · '.join(f'<a href="{E(u)}">{E(l)}</a>' for l,u in p['research_links'])+'</p></details>'
 if p['n']<=6:h+=f'<p><a href="ILK-14-GUN.html#{p["id"]}">Bu yayının ayrıntılı üretim kartı →</a></p>'
 return h+'</article>'

doc=head('Vizyon →180gönderi →ilk14gün')+'<p class="eyebrow">yigitozen.art · Ayak4 ·180ayrıgönderi</p><h1>Önce ressamın vaadi.<br>Sonra her gönderinin görevi.</h1>'
doc+=f'<p class="lead">{E(brief["vision_tr"])}</p><p lang="en" class="lead"><i>{E(brief["promise_en"])}</i></p>'+NAV
doc+='<div class="stats"><div><strong>180</strong>gerekçeli gönderi</div><div><strong>60</strong>haftalık başlangıç düzeni</div><div><strong>418</strong>son gönderinin göreli günü</div><div><strong>6</strong>ilk14günde ayrıntılı yayın</div></div>'
doc+='<p class="note">Bu plan180gün değil,180ayrıgönderidir. Başlangıç düzeni haftada3: Gün1/3/5, sonra8/10/12… Tarih atanmadı. Saat19.00 Europe/Paris bir çalışma tercihi; ideal saat veya günlük yayın zorunluluğu iddiası yok. Tüm180seçim yazılıdır; ileri tarihlerdeki sonuçlar bilinmediği için plan gözden geçirilebilir. Yayına hazır video/görsel renderleri bu teslimin parçası değildir.</p>'
doc+='<section id="vision"><h2>1. Hesabın ana işi</h2><p>Bir kişi tanıdığı bir karakter, çarpıcı bir yüz ya da gerçek boyama hareketi nedeniyle gelebilir. Burada kalma nedeni, farklı işlerde ayırt edebildiği bir resim pratiği olmalı. Hesap, bitmiş eserleri, üretimdeki gerçek kararları ve tarihli arşivi birbirine bağlayan bir inceleme alanı olarak çalışacak.</p><p>İzleyici ressamlarla sınırlanmayacak: işin kendisine bakan sanat izleyicisi, meslektaş, küratör/galeri çalışanı veya eserle ilgilenen kişi aynı içeriğe farklı ihtiyaçlarla yaklaşabilir. Belirli yaş, servet veya satın alma niyeti veri olmadan hedef kitle diye üretilmeyecek.</p><p><b>Öncelik:</b> yeni ilgili karşılaşma → pratiğin ayırt edilmesi → başka esere devam → künyeli eser/portföy incelemesi. Bu, izleyicinin zorunlu sırayla geçeceği bir tünel değil; hesabın desteklemesi gereken dört ayrı iştir.</p><div class="grid goals">'
for g,m in metrics.items():doc+=f'<div class="box"><p class="eyebrow">{g}</p><h3>{E(m["name"])}</h3><p>{E(m["primary"])}</p><small>{E(m["decision"])}</small></div>'
doc+='</div><p><b>Büyüme hedefi:</b> araştırmadaki90.günde5.000organik ve ilgili takipçi hedefi korunuyor.180gönderinin60haftaya uzaması bu hedef tarihini kendiliğinden uzatmıyor. Güncel başlangıç ve dönüşüm oranları olmadığı için hedefin ulaşılabilirliği doğrulanmış değil. Gün14/30/60/90’dayetişme hızı ve kaynak/ilgi belirsizliği açık raporlanacak.</p></section>'
doc+='<section><h2>2. Hesabın tanınmasını sağlayacak üç alan</h2><div class="grid"><div class="box"><h3>Beden ve yüz</h3><p>Painstaking, Gary, s(t)lop, Walls. Kütle, kontur, yüz parçaları ve nesne ilişkisi. Cellular, Ciao ve diğer eski işler aynı sorunun farklı çözümlerini getirir.</p></div><div class="box"><h3>Sahnenin dönüşümü</h3><p>Gxd, Board, Mandarin, Virgil, Sept. Kaynağı tanımak giriş olabilir; sahnenin beden, bakış, taşıma ve karşılaşma düzeninin nasıl değiştiği asıl içeriktir.</p></div><div class="box"><h3>Mekân ve bellek</h3><p>Angora, Virgil, Sept; Capricorn ve diğer arşiv karşılıkları. Ev, oda, sandalye, boşluk ve geometri figürü nasıl değiştiriyor? Kişisel hikâye yalnız kayıtlı olduğu kadar.</p></div></div><p>Süreç, Reel, eskiz ve carousel bu alanların sunum biçimleridir. Ana vizyonun yerine bir format takvimi konmaz. Eski eser her hafta anlamlı bir karşılıkla yer alır; bütün arşiv tüketilmek zorunda değil.</p></section>'
doc+='<section id="rules"><h2>3. Seçim ve sıra kuralları</h2>'
for title,body in principles:doc+=f'<h3>{E(title)}</h3><p>{E(body)}</p>'
doc+='<p class="evidence"><a href="'+REF+'04-strategy/strategy-index-20261016.md">Ayak4 ana fikir</a> · <a href="'+REF+'02-market/market-yigit-work-map-20261016.md">13eser haritası</a> · <a href="'+REF+'03-tactics/tactics-q17-answer-20261016.md">T17 sıklık</a> · <a href="'+REF+'03-tactics/tactics-q23-answer-20261016.md">T23 formatın işi</a> · <a href="'+REF+'03-tactics/tactics-q55-answer-20261016.md">T55 yeni değer</a> · <a href="'+REF+'03-tactics/tactics-q56-answer-20261016.md">T56 bağımsız bölüm</a></p></section>'
doc+='<section id="arc"><h2>4.180gönderinin bütün içindeki hareketi</h2><p>Altı30gönderilik blok üretimi ve değerlendirmeyi yönetir;30sayısı araştırmadan çıkmış doğal eşik değildir. Her blokta üç alan da var. Baskın inceleme işi değişir: tanışma, somut karar, farklı giriş, iş gövdesi, zaman karşılaştırması, kullanılabilir seçki.</p><div class="grid">'
for j,(title,output) in enumerate(zip(phase_titles,phase_outputs),1):doc+=f'<div class="box"><p class="eyebrow">P{(j-1)*30+1:03}–P{j*30:03} ·Hafta{(j-1)*10+1}–{j*10}</p><h3>{E(title)}</h3><p>{E(output)}</p><a href="#phase{j}">Gönderileri sırayla incele →</a></div>'
doc+='</div></section><section><h2>5. İlk14gün bu bütünü nasıl açıyor?</h2><p>Angora kişisel mekânı açar. Gary beden dilini gösterir. Cellular bu dilin eski ve farklı bir karşılığını getirir. Sept gerçek bir renk kararını hareket halinde gösterir. Painstaking üç yüzü tek yayında karşılaştırır. Ciao çizim aşaması aynı incelemeyi kontura taşır. Painstaking ilk14günde bir kez kullanılır.</p><p>Gün2,4,6,7,9,11,13,14’te akış yayını yok. Bu günler kurgu, ses, ölçüm ve gerçek yanıtlar içindir. Story de sırf günlük görünürlük kotası için zorunlu tutulmaz.</p><p><a href="ILK-14-GUN.html">Altı yayının görüntü sırası, İngilizce metni, caption’ı ve günlük işleri →</a></p></section>'
doc+='<section id="decisions"><h2>6. Sonuçlar hangi kararı değiştirecek?</h2><p><b>Gün14:</b> anlaşılma, üretim süresi ve ilk olgunlaşan gönderiler. <b>Gün30:</b> keşif, profil devamı veya eser incelemesi arasındaki darboğaz. <b>Gün60:</b> iyi görünen anlatımın farklı eserde karşılığı. <b>Gün90:</b>5.000hedefine göre gerçek ilerleme ve kaynak belirsizliği. Sonrasında her15gönderide sıradaki15yeniden incelenir.</p><p>Ölçümler24/72/168saatlik yaşlarda kaydedilir. İlk altı farklı içerik bir A/B testi sayılmaz. Aynı anda konu, format, saat ve ses değişirse sonuç tek bir “trick”e bağlanmaz. Gerçek bir darboğaz görüldüğünde bir sonraki uygun gönderide tek müdahale seçilir; kazanan aktarımı ikinci bir eserde gözlenmeden kalıcı kural yapılmaz.</p><p><b>Reklam:</b> başlangıçta kapalı. Önce organik yayınlar, anlaşılır profil ve erişilebilir seçki. Başlatma günü yok; “algoritma oturdu” diye varsayımsal tarih konmuyor. Önceki390€tavanı otomatik harcama veya60haftalık artırılmış bütçe değil.</p><p><b>Uzun vade:</b> yeni işler geldiğinde sıradaki kartın hedefi ve ilişkisi daha iyi karşılanıyorsa eser değişebilir. Değişiklik eski kart, yeni kaynak ve gerekçeyle kaydedilir. İzleyici sonuçları bu taslakta uydurulmadı.</p></section>'
doc+='<section id="all"><h2>7. Tek tek180gönderi</h2><p>Her kartta eser, amaç, sıra, yeni bilgi, kaynak dosya, İngilizce caption taslağı ve ölçüm işi var. İlk altı kartın ayrıca ayrıntılı üretim sayfası bulunuyor.</p><div class="filters"><input id="search" type="search" aria-label="Gönderilerde ara" placeholder="Eser, Pnumarası veya gerekçe ara"><select id="phasefilter" aria-label="Bölüm"><option value="">Tüm bölümler</option value="1">1–30</option><option value="2">31–60</option><option value="3">61–90</option><option value="4">91–120</option><option value="5">121–150</option><option value="6">151–180</option></select><select id="goalfilter" aria-label="Hedef"><option value="">Tüm hedefler</option value="G1">G1 Keşif</option><option value="G2">G2 Tanınma</option><option value="G3">G3 Devam</option><option value="G4">G4 İnceleme</option></select><span id="count">180gönderi</span></div></section>'
for phase in range(1,7):
 doc+=f'<section id="phase{phase}"><p class="eyebrow">Bölüm{phase}</p><h2>{E(phase_titles[phase-1])}</h2><p>{E(phase_outputs[phase-1])}</p><a class="back" href="#top">Başa dön ↑</a></section>'
 doc+=''.join(postcard(p) for p in posts if p['phase']==phase)
doc+='''<script>
const q=document.getElementById('search'),ph=document.getElementById('phasefilter'),g=document.getElementById('goalfilter'),cards=[...document.querySelectorAll('.post')];
function filter(){let n=0;for(const c of cards){const ok=(!ph.value||c.dataset.phase===ph.value)&&(!g.value||c.dataset.goal===g.value)&&(!q.value||c.dataset.search.includes(q.value.toLowerCase()));c.classList.toggle('hidden',!ok);if(ok)n++;}document.getElementById('count').textContent=n+' gönderi';}
for(const el of [q,ph,g])el.addEventListener('input',filter);
</script>'''+FOOT
research_table='<section><h2>Araştırma hangi somut kararı değiştirdi?</h2><div class="table-wrap"><table><tr><th>Dayanak</th><th>Bu plandaki karşılığı</th><th>Nasıl okunacak?</th></tr>'
for tactic,action,measure in [
 ('T03 / T42 · Özgül kanca','P001: çocukluk evi + tanıdık ziyaretçi. Kanca sanatçının kaydındaki bilgiyle karşılanır.','Karaktere tepki ile ev/resim hakkında devam sorusunu ayır.'),
 ('T04 / T46 · İzlemeyi taşıyan bilgi','P004: erken sıcak beden → gerçek boya müdahalesi → morlaşan beden. Her bölüm yeni durum gösterir.','İzleme alanları varsa kaydet; süreyi kısaltmayı otomatik başarı sayma.'),
 ('T43 · Kapak/ilk kare ayrımı','P001 kapağı ev konusunu tanıtır; oynayan ilk kare ev ve figürü birlikte gösterir.','Kapağın iyi olması boş açılışı çözmez; iki işi ayrı kontrol et.'),
 ('T54 · Carousel bilgi ilerlemesi','P005 her sayfada başka panel ve başka yüz dengesi. Genel save/follow son sayfası yok.','Kaydetme ve panel farkına ilişkin somut gözlem; görünmeyen swipe yüzdesi yok.'),
 ('T55 · Tekrarda yeni değer','Gary P002 bütün; P020 gündelik nesneler; P048 hacmi kuran gerçek fırça izleri.','Sadece yeni crop veya hız varsa yeni içerik sayma; farklı iddia kanıt gerektirir.'),
 ('T57 · Paylaşılma nedeni','P022 müzikten kendi resmine kaynak yolu; P001 çocukluk mekânının değişmesi.','Birinin arkadaşına göndermesi için içerikte neden var mı? Bu neden gözlenmiş DM davranışı değil.'),
 ('T14 / T56 · Profil ve bağımsız devam','P030 künyeli üç alan girişi; her önceki yayın kendi cevabını tamamlar.','Erişim ile profil/ilgili takip ayrılır; önceki bölümü görmeyen de içeriği anlayabilir.'),
 ('T17 / T60 · Sıklık ve ölçüm','Haftada 3 başlangıç; 19.00 çalışma saati; 24/72/168 saat karşılaştırma.','Bunlar araştırmanın optimum rakamları değil. Üretim süresi ve ilgili sonuçlar birlikte okunur.')]:research_table+=f'<tr><td>{E(tactic)}</td><td>{E(action)}</td><td>{E(measure)}</td></tr>'
research_table+='</table></div><p>Kancalar ve paylaşılma nedenleri tasarım hipotezidir. Yapılmamış hesap deneyi varmış gibi sonuç yazılmaz.</p></section>'
mix=collections.Counter(p['format'] for p in posts)
format_note=f'<section><h2>Format dağılımının bilinçli sınırı</h2><p>Bu taslakta {mix["Reel"]} Reel, {mix["Carousel"]} carousel, {mix["Single"]} tek görsel var. Arşivin güçlü yanı bitmiş eser, detay ve eşlenmiş gerçek aşamalar. Keşif işi hem gerçek hareket/anlatı Reels’ine hem belirli bir karşılaştırmayı paylaşılabilir yapan carousel fikrine verildi.</p><p>Bu dağılım eski araştırmadaki haftada 3 Reel üretim varsayımından farklıdır; 5.000/90 gün hedefini taşıdığı henüz kanıtlanmış değildir. Gün 30’da yeni ve ilgili karşılaşma yetersizse sıradaki uygun G1 kartları için yeni gerçek stüdyo/ressam çekimleri planlanır. Aynı fotoğrafları daha hızlı slayta çevirmek bu açığı kapatmış sayılmaz; değişen kartın kaynak ve üretim ihtiyacı da güncellenir.</p></section>'
newcaptures=[p['id'] for p in posts if p.get('requires_new_capture')]
format_note=format_note.replace('</section>',f'<p><b>Yeni hareketli çekim isteyen {len(newcaptures)} kart:</b> {E(", ".join(newcaptures))}. Bunlar hazır arşiv videosu diye sunulmadı. İlk14gündeki iki Reel için yeni görüntü çekimi değil, yeni İngilizce ses kaydı gerekli. <a href="YENI-CEKIMLER.json">Dokuz ek hareket/çekim fikri ve yedekleri</a>.</p></section>')
doc=doc.replace('<section id="arc">',research_table+'<section id="arc">').replace('<section id="all">',format_note+'<section id="all">')
def tidy_visible(markup):
 # Only prose nodes: keep attributes, script, CSS and source hashes intact.
 bits=re.split(r'(<style\b.*?</style>|<script\b.*?</script>|<[^>]+>)',markup,flags=re.S)
 for i,s in enumerate(bits):
  if s.startswith('<'):continue
  saved={}
  def protect(m):
   key='HASHPLACEHOLDER'+chr(65+len(saved));saved[key]=m[0];return key
  s=re.sub(r'&#?[A-Za-z0-9]+;|\b[0-9a-f]{8,40}\b|[^\s<>]+\.(?:txt|srt|json|html|png|jpg|mp4)\b|\b[APGTY]\d{1,4}\b',protect,s)
  s=re.sub(r'(Gün|Hafta|Bölüm|ilk|İlk|son|Son|Ayak)(?=\d)',r'\1 ',s)
  s=re.sub(r'(?<=\d)(?=[A-Za-zÇĞİÖŞÜçğıöşü])',' ',s)
  s=re.sub(r'(?<=[a-zçğıöşü])(?=\d)',' ',s)
  s=re.sub(r'(?<=[a-zçğıöşü])(?=P\d{3}|A\d{4})',' ',s)
  s=re.sub(r',(?=\S)',', ',s)
  s=re.sub(r'^([1-7])\.(?=\d)',r'\1. ',s)
  s=s.replace('180 ayrıgönderi','180 ayrı gönderi').replace('Pnumarası','P numarası').replace('gönderi180','gönderi 180')
  for k,v in saved.items():s=s.replace(k,v)
  bits[i]=s
 return ''.join(bits)
if covers:
 doc=doc.replace('Yayına hazır video/görsel renderleri bu teslimin parçası değildir.','180 kapak PNG/SVG olarak üretildi; grid önizlemeleri ayrı sayfada. Bitmiş videolar, ses kayıtları ve carousel iç sayfaları henüz tamamlanmış değil. Kapak çıktısı, Instagram yükleme önizlemesinin kontrol edildiği anlamına gelmez.')
(OUT/'VIZYON-VE-180-POST.html').write_text(tidy_visible(doc),encoding='utf8')

first=head('İlk14gün ·180gönderilik vizyonun açılışı')+'<p class="eyebrow">yigitozen.art ·İngilizce yayın paketi taslağı</p><h1>İlk14gün.<br>Altı ayrı görev, altı eser.</h1>'+NAV+'<p class="lead">Bu altı yayın180gönderilik plandaki P001–P006’dır. Sıra ana vizyondan geliyor: kişisel mekân, beden dili, tarihli karşılık, gerçek karar, yüz karşılaştırması, çizim.</p><p class="note">Gün1/3/5/8/10/12 ·19.00 Europe/Paris. İkiReel için yeni İngilizce ses kaydı gerekli. Caption, söz metni, taslakSRT ve sayfa metinleri yazıldı; final medya ve sesler henüz üretilmedi. Müzik seçimi: ilk altı yayında yok; bu bir performans iddiası değil.</p>'
first+='<section><h2>14günün işi</h2><div class="table-wrap"><table><thead><tr><th>Gün</th><th>Yayın / üretim / ölçüm</th></tr></thead><tbody>'
for d,t in DAY_TASKS.items():first+=f'<tr><td>Gün{d}</td><td>{E(t)}</td></tr>'
first+='</tbody></table></div></section>'
for p in posts[:6]:
 d=p['details'];first+=f'<article class="post" id="{p["id"]}"><p class="eyebrow">{p["id"]} ·Gün{p["day"]} ·19.00 ·{E(p["format"])}</p><h2 lang="en">{E(p["title_en"])}</h2><p><b>Hedef:</b> {p["goal"]} ·{E(metrics[p["goal"]]["name"])}</p><div class="reason"><p><b>Neden bu eser?</b><br>{E(p["why_tr"])}</p><p><b>Neden bu sıra?</b><br>{E(p["order_tr"])}</p></div>'+gallery(p)
 first+=f'<h3>Görsel düzen</h3><p>{E(d["layout_tr"])}</p>'
 if d['cover_en']:first+=f'<p lang="en"><b>Cover:</b> {E(d["cover_en"])}</p>'
 if p['n'] in covers:
  first+=f'<div class="assets"><a href="../grid-cover-design/exports/{p["id"]}.webp"><img style="width:270px;height:360px" src="../grid-cover-design/tiles/{p["id"]}.webp" alt="{p["id"]} designed cover"><span>Tam boy kapak PNG</span></a></div><p><a href="../grid-cover-design/GRID-VE-KAPAKLAR.html#{p["id"]}">Kapak kararı ve yayın sonrası grid →</a></p>'
 if d.get('shots'):
  first+='<div class="table-wrap"><table><thead><tr><th>Çıktı</th><th>Kaynak</th><th>English on-screen text</th><th>Görüntünün işi</th></tr></thead><tbody>'
  for s in d['shots']:
   source='Sabit bütün' if s['source'] is None else f'{s["source"][0]}–{s["source"][1]}sn'
   first+=f'<tr><td>{s["out"][0]}–{s["out"][1]}sn</td><td>{E(s["asset"])}<br>{source}'+(f'<br>+{s["overlay"]} eser' if s.get('overlay') else '')+f'</td><td lang="en">{E(s["text"])}</td><td>{E(s["action"])}</td></tr>'
  first+='</tbody></table></div>'
 if d.get('slides'):
  first+='<div class="slides">'
  for s in d['slides']:first+=f'<div class="slide"><img loading="lazy" src="{E(thumb(s["asset"]))}" alt="{E(s["asset"])}"><p lang="en">{E(s["text"])}</p></div>'
  first+='</div>'
  for s in d['slides']:first+=f'<p><b>Sayfa{s["n"]} ·{s["asset"]}:</b> {E(s["action"])}</p>'
 if d.get('voice_en'):first+='<h3>English voice · yeni kayıt metni</h3><pre lang="en">'+E(d['voice_en'])+'</pre>'
 first+='<h3>Caption · English</h3><pre lang="en">'+E(p['caption_with_credit_en'])+'</pre><h3>Alternative text · English</h3><pre lang="en">'+E(d['alt_en'])+'</pre>'
 first+=f'<p><b>Ses / müzik:</b> {E(d["sound_tr"])}</p><p><b>İsteğe bağlı Story:</b> {E(d["story_tr"])}</p><pre lang="en">{E(d["story_en"])}</pre><p><b>Yayın öncesi kontrol:</b> {E(d["check_tr"])}</p><p><b>Sonrasında ölçüm:</b> {E(p["check_tr"])}</p><div class="sources">'
 for fn in d['deliverables']:first+=f'<a href="texts/{E(fn)}">{E(fn)}</a>'
 first+=f'</div><p><a href="VIZYON-VE-180-POST.html#{p["id"]}">180gönderilik plandaki yeri →</a></p></article>'
if covers:
 first=first.replace('final medya ve sesler henüz üretilmedi.','altı kapak PNG/SVG olarak üretildi. Bitmiş Reel kurguları, sesler ve carousel iç sayfa çıktıları henüz tamamlanmadı.')
first+=FOOT;(OUT/'ILK-14-GUN.html').write_text(tidy_visible(first),encoding='utf8')

profile=head('Profil ve künyeli seçki girişi')+'<p class="eyebrow">Yerel metin/seçki taslağı ·Instagram değiştirilmedi</p><h1>Profilin verdiği sözü<br>eserler tamamlasın.</h1>'+NAV
profile+='<section><h2>Bio ·English</h2><pre lang="en">Paintings of unstable bodies and familiar spaces.\nWorks, studio decisions and the archive.\nSelected works ↓</pre><p>Bağlantı, yayın sırasında gerçekten açılan güncel seçkiye gitmeli. Aşağıdaki yerel seçki bir gözden geçirme materyali; internet üzerinde yayımlanmış yeni sayfa değil.</p><h3>Sabit içeriklerin görevi</h3><p>P001 kişisel mekân/anlatı girişi. P003 geldiğinde tarihli arşiv karşılığı. P005 geldiğinde beden/yüz incelemesi. P030 yayımlandıktan sonra genel künyeli seçki, P003’ün sabit yerini alabilir. Böylece yapılmamış bir gönderi ilk günden mevcutmuş gibi planlanmaz.</p><p>Üç sabitin görevi: pratiğe giriş, somut karar/inceleme ve iş gövdesine erişim. Mevcut profil/sabitler bu oturumda okunmadı veya değiştirilmedi; yayın sırasında var olan güçlü içerikler varsa bu işlevlerle karşılaştırılır.</p></section>'
profile+='<section><h2 lang="en">Selected paintings</h2><p lang="en">Bodies, scenes and spaces across the current work and the archive. Titles, materials and dimensions identify each painting; availability is not stated.</p><div class="grid">'
for k in ['angora','gary','board','painstaking','stlop','wall','gxd','virgil','sept','mandarin','cellular','ciao','capricorn']:
 w=works[k];profile+=f'<div class="box work"><a href="{E(url(assets[w["master"]]["path"]))}"><img loading="lazy" src="{thumb(w["master"])}" alt="{E(w["title"])}"></a><h3 lang="en">{E(w["title"])}</h3><pre lang="en">{E(credit(k))}</pre></div>'
profile=profile.replace('Mevcut profil/sabitler bu oturumda okunmadı veya değiştirilmedi; yayın sırasında var olan güçlü içerikler varsa bu işlevlerle karşılaştırılır.','4 Kasım 2026 tarihinde herkese açık profil okundu; üç görünür gönderi grid önizlemesine eklendi. Hesabın mevcut sabitleri ve arşivin tamamı bu görünümden kesinleşmiyor. Önerilen sabit sırası hesapta uygulanmadı; gerçek yayın önizlemesinde kontrol edilmeli.')
profile+='</div></section>'+FOOT;(OUT/'PROFILE-ENTRY.html').write_text(tidy_visible(profile),encoding='utf8')

errors=[]
required=['n','phase','works','assets','format','pillar','goal','title_en','caption_en','idea_tr','why_tr','order_tr','new_value_tr','archive','tactics','production_tr','sound','evidence','check_tr']
if [p['n'] for p in posts]!=list(range(1,181)):errors.append('180 unique consecutive post numbers missing')
weekly=[]
for week in range(1,61):
 ps=[p for p in posts if p['week']==week];count=sum(p['archive'] for p in ps);weekly.append({'week':week,'archive_posts':count})
 if count not in [1,2]:errors.append(f'week{week}:archive{count}')
for p in posts:
 for k in required:
  if k not in p or p[k] is None or (isinstance(p[k],(str,list)) and not p[k]):errors.append(f'{p["id"]}:{k}empty')
 if len(p['caption_with_credit_en'])>=2200:errors.append(p['id']+'caption too long')
 for i in p['assets']:
  if i not in assets or not Path(assets[i]['path']).exists():errors.append(p['id']+'missingasset'+i)
 if p['format']=='Reel' and not any(assets[i]['kind']=='video' for i in p['assets']):
  if not any(x in p['production_tr'].lower() for x in ['yeni','çekim','kaydet']):errors.append(p['id']+'Reelwithoutmotionornewrecording')
for a,b in zip(posts,posts[1:]):
 if a['works'][0]==b['works'][0]:errors.append(f'consecutive primary work:{a["id"]},{b["id"]}')
for p in posts[:6]:
 d=p['details']
 if d.get('shots'):
  ss=d['shots']
  if ss[0]['out'][0]!=0 or ss[-1]['out'][1]!=d['duration']:errors.append(p['id']+'timeline endpoints')
  for a,b in zip(ss,ss[1:]):
   if a['out'][1]!=b['out'][0]:errors.append(p['id']+'timeline gap')
  for s in ss:
   if s['source']:
    if s['source'][1]>assets[s['asset']]['duration']:errors.append(p['id']+'source beyond duration')
    if s['source'][1]-s['source'][0]!=s['out'][1]-s['out'][0]:errors.append(p['id']+'speed not accounted')
for f in OUT.glob('*.html'):
 txt=f.read_text(encoding='utf8')
 for ref in set(re.findall(r'(?:href|src)="([^"]+)"',txt)):
  ref=html.unescape(ref)
  if ref.startswith(('http:','https:','#')):continue
  ref=ref.split('#')[0]
  dest=Path(unquote(urlparse(ref).path).lstrip('/')) if ref.startswith('file:') else OUT/unquote(ref)
  if not dest.exists():errors.append(f.name+'brokenlocal:'+ref)
report={'valid':not errors,'errors':errors,'posts':len(posts),'first14_days':[p['day'] for p in posts[:6]],'last_post_day':posts[-1]['day'],'unique_work_keys':len(set(k for p in posts for k in p['works'])),'format_counts':dict(collections.Counter(p['format'] for p in posts)),'goal_counts':dict(collections.Counter(p['goal'] for p in posts)),'weekly_archive_counts':weekly,'all_source_paths_checked':True,'source_link_validation':'local file existence only; external historical research URLs not refreshed','first14_timeline_checks':True,'browser_visual_qa':False,'new_voice_recordings_first14':['P001','P004'],'rendered_media':False,'published':False,'semantic_review':'independent editorial review plus source checks; not evidence of audience success'}
report['rendered_covers']=len(covers)
report['cover_platform_preview_checked']=False
save(OUT/'VALIDATION.json',report)
print(json.dumps({k:v for k,v in report.items() if k!='weekly_archive_counts'},ensure_ascii=False,indent=2))
if errors:sys.exit(1)
