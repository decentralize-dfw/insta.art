import json,csv,html,re,collections
from pathlib import Path
from urllib.parse import unquote,urlparse
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'instagram-review/publication-plan-180'
OLD=ROOT/'instagram-review/publication-plan-180-v1-superseded'
OUT.mkdir(exist_ok=True);(OUT/'captions-v2').mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
assets={r['id']:r for r in read(ROOT/'archive-audit/audit-files.json')}
works=read(OLD/'works.json');music=read(OLD/'music.json');catalog={w['id']:w for w in read(ROOT/'yigit-site-repo/v3/content/works.json')}
for key,slug,master in [('lucid','remixed-execution-of-lucid-drowning','A1695'),('society','society-screwing-balance','A2763')]:
 c=catalog[slug];works[key]={'key':key,'title':c['title'],'year':c['year'],'medium':c['medium'],'height_cm':c['height_cm'],'width_cm':c['width_cm'],'master':master,'details':[],'metadata_source':'yigit-site-repo/v3/content/works.json'}

# Haftanın üç işi birbirinden farklı eserler; arşiv her hafta 1–2 yayın.
# Sıralama, mevcut videodaki farklı olaylara dayanır; yeni bir film çekilmiş sayılmaz.
rows=[
 ('capricorn','painstaking','baby','A0001','Study','The lower figure changes.','A2802','actual_painting','Alt figürün koyu alanla değişmesi; son eser ile çekim aşamasını ayır.'),
 ('board','angora','ciao','A1903','Single','What would you leave alone?','A0620','studio_conversation','Piyonlar ve arka plan üzerine gerçek atölye konuşması.'),
 ('sept','wall','wings','A2795','Study','The figure is the part left unpainted.','A1159','actual_painting','Yeşil zemin boyanırken açık figür alanının bırakılması.'),
 ('gxd','stlop','duality','A1945','Single','How did an album cover enter this painting?','A1340','artist_story','Sanatçının kendi resmine giden referans yolunu kısa anlatıya çevir.'),
 ('capricorn','virgil','good','A0004','Study','This yellow stage came before the dark painting.','A2800','actual_painting','Sarı zeminli kaydı tarihli ara aşama olarak göster; son kararmayı filme alınmış gibi sunma.'),
 ('board','gary','cellular','A1862','Single','A red shape becomes part of the figure.','A0630','actual_painting','Kırmızı gövde alanındaki gerçek çalışma hareketini tek ilerleme olarak kur.'),
 ('angora','mandarin','rompi','A1750','Single','A visitor, or a threat?','A1632','artist_story','Çocukluk evi ve kahramanı arasındaki ikiliği anlatan kaynak bölüm: yaklaşık 616–672 sn.'),
 ('sept','painstaking','lucid','A1696','Study','The paper guide enters the painting session.','A1161','studio_method','Kâğıt kılavuzun gerçekten kullanıldığı bölümü seç; sahneleme yok.'),
 ('gxd','wall','unemployed','A2388','Single','Why put AFK in a painting title?','A1340','artist_story','Başlığın sanatçı anlatısındaki anlamını aç; kaynaktaki sözleri doğrulamadan alıntı kurma.'),
 ('capricorn','angora','peachy','A2156','Single','One passage at the speed it was painted.','A2801','actual_painting','Bir fırça hareketini gerçek hızda tut; ardından aynı kaynak aralığının hızlandırılmış kısa karşılığını göster.'),
 ('board','gxd','greatfire','A2423','Single','The reference stays beside the canvas.','A0631','studio_method','Resim ve kâğıt referansın aynı çekimde görünmesini kullan; yaklaşık 49–57 dk boş kısmı çıkar.'),
 ('sept','virgil','materialize','A2063','Single','The figure changes colour during the session.','A1167','actual_painting','Sarıdan koyu/mor figüre ilerleyen gerçek kayıttan iki anlamlı an; süreç fotoğraflarıyla taklit etme.'),
 ('angora','stlop','society','A2763','Study','A blue world with an orange visitor.','A1632','artist_story','Renk ve çocukluk referansını bağla; kaynak yaklaşık 672–756 sn. Karakteri tek başına popüler kültür yemi yapma.'),
 ('gxd','gary','viperella','A1772','Single','The weight of the group.','A1340','artist_story','Taşıma/grup ilişkisini sanatçının anlatımı ve kendi eseriyle aç; üçüncü taraf eser görüntüsü gerekmiyor.'),
 ('capricorn','mandarin','baby','A1809','Single','The brush returns to the same figure.','A2801','actual_painting','Alt figüre geri dönülen ayrı kaydı seç. Önceki Reel ile aynı saniyeleri yeniden kullanma.'),
 ('board','painstaking','guard','A2050','Single','A small correction inside a large painting.','A0632','actual_painting','Kişiler gelmeden önce gerçek ince çalışma; son sohbet bölümünü D08 gibi tekrar kullanma.'),
 ('sept','wall','transhumanism','A2213','Single','The smaller figure gets its own attention.','A1169','actual_painting','Kuş/yan alan üzerindeki gerçek çalışma anını seç; arka plandaki medya sesini temizle.'),
 ('angora','gary','morbid','A2182','Single','When the house becomes the main character.','A1632','artist_story','Mekânın ağırlığını anlatan yaklaşık 196–224 ve 504–560 sn kaynaklarını tek düşüncede birleştir.'),
 ('gxd','virgil','ciao','A1716','Process carousel','A familiar arrangement with a different context.','A1340','artist_story','Referansın yeniden yorumunu açıkla; önceki AFK/başlık bölümünden farklı kaynak cümleleri.'),
 ('capricorn','stlop','wings','A2451','Single','A filmed session from the 2020 archive.','A2800','archive_session','Boyama hızından önce stüdyodaki gerçek çalışma hâli; arşivi yeni çekim gibi göstermeden.'),
 ('board','gary','duality','A1930','Detail pair','The palette and the painting share a frame.','A0627','studio_method','Palet, el ve tuvali aynı çekimde tutan erken dönem parçayı seç.'),
 ('sept','mandarin','good','A2014','Single','The outline changes what the green surrounds.','A1165','actual_painting','Beyaz/mavi kontur işçiliğinin gerçek hareketi; ilk yeşil zemin videosundan farklı olay.'),
 ('angora','painstaking','cellular','A1844','Detail pair','The character belongs to a personal place.','A1632','artist_story','Çocukluk hafızası ve mekânı bağlayan başka anlatım parçası; D10 metnini yeniden okumak değil.'),
 ('gxd','wall','lucid','A1695','Single','One reference led to another.','A1340','artist_story','Caravaggio → albüm kapağı → kendi resmine geçişi kaynağa bağlı kısa sözlü hikâye olarak kur.'),
 ('capricorn','angora','rompi','A2452','Single detail','A figure can be lost inside its own repainting.','A2799','actual_painting','Önceki alt figür siyahlaştırma kurgusundan farklı fırça aralığı; aynı anın hızlı kopyası olmaz.'),
 ('board','virgil','penguin','A2743','Single','A session ends before the painting is a finished post.','A0631','studio_method','Boyama anından gerçek mola/masadan ayrılmaya geç; kaydı bitmiş eserin tamamlanma anı diye etiketleme.')]

reel_captions={
 1:'From the 2020 studio archive. Watch the dark paint take over the lower figure. The filmed passage is an intermediate stage; the last image shows the later finished painting.',
 2:'The studio conversation came down to two things: darken the pieces, and leave the background alone. A small moment from working on 7 fam board game.',
 3:'The green goes down around the figure. This part of the painting is built by leaving an area open while working on what surrounds it.',
 4:'An album cover became part of the route into Gxd is AFK, We banned it. This short account follows the reference back into the painting.',
 5:'A yellow stage from the studio archive, followed by the finished dark-field painting. The archive preserves how far apart two states of one work can be.',
 6:'The brush keeps returning to the red figure. This excerpt stays with one area rather than trying to compress the whole painting into a few seconds.',
 7:'A childhood character above a childhood home. The figure in Angora Mergvs can read as a visitor, but it can also feel like a threat.',
 8:'A paper guide, paint on the table, the figure taking shape. A working moment from the sept neuf recordings.',
 9:'The title of Gxd is AFK, We banned it brings another language into a painted group. A short excerpt from the account behind the work.',
 10:'The same passage at two speeds. The real-time section stays long enough to see the hand working before the edit changes pace.',
 11:'The reference remains beside the canvas during this session. The painting is still being decided, one small passage at a time.',
 12:'The figure is changing while the session continues. These are moments from the recorded painting process, with the original sequence preserved.',
 13:'The blue setting and orange figure carry different associations into Angora Mergvs. The colour story is part of the account behind the painting.',
 14:'The grouping gives the scene its weight. This excerpt follows the account behind the bodies and the spaces between them.',
 15:'Another return to the lower figure in the studio archive. A painting can change through several visits to the same small area.',
 16:'One correction inside a larger composition. The wide studio view stays in the edit so the gesture has somewhere to belong.',
 17:'A smaller figure receives the same slow attention as the larger one. A working excerpt from the sept neuf archive.',
 18:'The house began to take over the painting. A short account of how architecture became central to Angora Mergvs.',
 19:'A familiar grouping entered a different context. This excerpt stays with the route into the painting rather than treating the reference as the whole explanation.',
 20:'A filmed painting session from 2020. The movements belong to the original archive; this is a new edit of that record.',
 21:'The palette, the hand and the canvas share the same frame. A working passage from 7 fam board game.',
 22:'A small outline changes the relation between the figure and the green field. A later passage from the sept neuf recordings.',
 23:'The place in Angora Mergvs is personal. This excerpt returns to the memories behind the architecture, through a different part of the recorded account.',
 24:'One reference led to another, and then into a painting. The short account keeps that route visible without replacing the work with its references.',
 25:'Repainting can make a figure less certain. This excerpt follows another passage from the 2020 studio record.',
 26:'A pause in a painting session. The archive keeps the working time around the image, including the moment when the hand stops.'}

archive_notes={
 1:'An undated study from the baby rights 101 files. The drawing keeps the overlapping bodies and red passage visible at an early stage. The painting is dated 2020; a date for this study has not been established.',
 2:'From the Milan archive, 2020. Two elongated figures share the red-and-black field.',
 3:'An undated drawing from the archive. The working lines and notes remain visible. Filed as wingsofabbyss-v1; the drawing is presented on its own.',
 4:'From the 2019 archive. A divided figure in purple, blue and green.',
 5:'An undated drawing from the good people files. The loose pencil lines are part of what is being shown here.',
 6:'From the 2020 archive. A pale field filled with eyes and organic forms.',
 7:'From the 2019 archive. A face broken into coloured passages.',
 8:'An undated study from the lucid drowning files. Colour notes and drawn furniture remain in the image.',
 9:'From the 2020 archive. A rounded figure held against red.',
 10:'From the 2019 archive. An elongated body and a drawn chair occupy the same field.',
 11:'From the 2020 archive. The complete work, with the surrounding dark field preserved.',
 12:'From the 2019 archive. A route across a crowded surface, from one head to another.',
 13:'An undated drawing from the society screwing balance files. Working lines, boxes and small forms remain visible.',
 14:'From the 2020 archive. The complete figure in viperella.',
 15:'baby rights 101, 2020. The finished painting returns after the earlier study shown at the start of this selection.',
 16:'From the 2019 archive. Bodies suspended against a room divided into blocks of colour.',
 17:'From the 2019 archive. A dark mechanical centre, coloured bodies and painted signs.',
 18:'From the 2019 archive. This work is distinct from the square penguin painting dated 2023.',
 19:'Three recorded states of ciao capo, sono squalo. The final painting is dated 2020; the individual photographs are not independently dated.',
 20:'wings of abyss, 2019. The complete painting follows the undated archive drawing shown earlier in the selection.',
 21:'Two details from duality of the angelic summarization, 2019. The full painting remains in the last frame for orientation.',
 22:'good people helping bad ones (that’s why they’re bad too), 2019. The finished work follows the earlier archive drawing.',
 23:'Two details from cellular spleens, 2020. The full painting locates them without turning the details into separate works.',
 24:'remixed execution of lucid drowning, 2019. The complete painting returns after its undated study.',
 25:'A close view from il sbagliato di rompipalle, 2019. A new viewing distance for a work shown earlier in this selection.',
 26:'From the 2023 archive. The complete square painting, with all four edges preserved.'}

def credit(w):
 if w.get('panel_count'):return f"{w['title']}\n{w['year']} · {w['medium']}\nTriptych · 3 panels, each 40 × 30 cm (h × w)."
 return f"{w['title']}\n{w['year']} · {w['medium']}\n{w['height_cm']} × {w['width_cm']} cm (h × w)."
def music_credit(mid):
 if mid=='M0':return ''
 m=music[mid];return f"Music: {m['title']} — Scott Buckley. CC BY 4.0. Excerpt; volume adjusted.\n{m['url']}\nhttps://creativecommons.org/licenses/by/4.0/"
posts=[];weeks=[]
def add(day,wk,key,fmt,hook,asset_ids,caption,why,kind,mid='M0',duration=0):
 w=works[key];p={'id':f'V2-P{len(posts)+1:03}','day':day,'week':wk,'time':'19:00','timezone':'Europe/Paris','format':fmt,'work_key':key,'title_en':hook,'asset_ids':asset_ids,'caption_en':caption,'why_this_post_tr':why,'content_kind':kind,'status':'detailed_plan_not_rendered' if day<=14 else 'draft_revalidate_before_production','music_id':mid,'duration_seconds':duration,'music_window_seconds':([30,30+duration] if mid!='M0' else None),'is_archive':w['year']<2026 or kind=='archive_study','actual_published_at':None,'rendered_media_path':None,'story':'İsteğe bağlı. Bu gönderiyi tekrar anlatmayan tek ayrıntı varsa 19.20; yoksa Story yok.','story_text_en':hook,'measurement_ages_hours':[24,72,168],'editorial_language':'en','source_selection_status':'kesin üretim kartı' if day<=14 else 'eser ve kaynak seçildi; kesim noktası haftalık üretimde kesinleşecek','repeated_work_check':'Aynı esere yeni olay/bilgi olmadan dönüş yok; 14 gün editoryal alt aralık, algoritma eşiği değil.'}
 if mid!='M0':p['caption_en']+='\n\n'+music_credit(mid)
 posts.append(p);return p

for wi,(r,s,a,aid,afmt,hook,vid,kind,brief) in enumerate(rows,1):
 start=(wi-1)*7+1;rw=works[r];sw=works[s];aw=works[a]
 p=add(start,wi,r,'Reel',hook,[vid,rw['master']],reel_captions[wi]+'\n\n'+credit(rw),brief,kind,mid='M1' if kind=='actual_painting' else 'M0',duration=32 if wi==1 else 28)
 p['edit_tr']='Olayın gerçekleştiği hareketli kayıt açılışta. Yalnız yeni bilgi taşıyan kesmeler; en fazla son 3–5 saniye tamamlanmış eser. Fotoğraf yakınlaştırmalarından Reel üretme.'
 p['source_video_id']=vid
 if wi==2:
  p=add(start+2,wi,'angora','Reel','I put a childhood character above my childhood home.',['A1632','A1378'],'I put a childhood character above the house I grew up in. The house began to take over the painting.\n\n'+credit(works['angora']),'Sanatçı anlatısındaki kişisel sebep. Önceki Satranç sohbetinden farklı eser, bilgi ve ritim.','artist_story',duration=38)
  p['edit_tr']='Gerçek konuşma videosu + ev/figürün en fazla iki sabit bindirmesi. Kişisel anlatı taşıyan İngilizce ses metni; slayt sırası yok.';p['source_video_id']='A1632'
 else:
  fmt='Carousel' if wi in [1,5,7,11,13,15,19,23] else 'Single'
  aa=([sw['master'],*sw['panels_left_to_right']] if s=='painstaking' and wi==1 else [sw['master'],*(sw.get('details',[])[:2])] if fmt=='Carousel' else [sw['master']])
  p=add(start+2,wi,s,fmt,sw['title'],aa,credit(sw),'Bağımsız tamamlanmış eser sunumu. Haftanın Reel’inin başka formatta tekrarı değil; farklı eser.','finished_work')
  p['edit_tr']='Tam eser ve gerekliyse gerçekten farklı bilgi taşıyan 2–3 ek görüntü. Tek görsel yetiyorsa carousel yapma; açıklayıcı slogan kotası yok.'
 if afmt=='Study':
  ac=archive_notes[wi]+'\n\nArchive drawing · undated\nYiğit Özen';aa=[aid]
 elif afmt=='Process carousel':ac=archive_notes[wi]+'\n\n'+credit(aw);aa=['A1716','A1718','A1717','A1903']
 elif afmt=='Detail pair':ac=archive_notes[wi]+'\n\n'+credit(aw);aa=[aid,aw['details'][min(3,len(aw['details'])-1)],aw['master']]
 else:ac=archive_notes[wi]+'\n\n'+credit(aw);aa=[aid]
 p=add(start+4,wi,a,'Carousel' if afmt in ['Process carousel','Detail pair'] else 'Single',('Archive drawing' if afmt=='Study' else aw['title']),aa,ac,'Eski iş/eskiz kendi başına bir yayın. Yeni Reel’e köprü veya ders olmak zorunda değil.','archive_study' if afmt=='Study' else 'archive_work')
 p['edit_tr']='Çizim/tarihsel fotoğrafı olduğu gibi sun. Belirsiz çizim tarihini tamamlanmış eserin yılıyla doldurma. Tamamlanmış işte künye; eskizde yalnız doğrulanmış bilgi.'
 weeks.append({'week':wi,'days':[start,min(start+6,180)],'roles':['Gerçek olay/anlatı içeren video','Farklı tamamlanmış eser veya kişisel anlatı','Eski iş/eskiz'],'work_keys':[r,s,a],'archive_feed_count':sum(x['is_archive'] for x in posts if x['week']==wi),'learning_task':'İlk 14 gün sıklık/çeşitlilik düzeltmesini gözle; ayrıca kanca, saat ve müzik A/B testi açma.' if wi<=2 else 'Geçmiş aynı yaştaki sonuç ve üretim süresine göre tek karar. Bu haftanın yeni olayının önceki yayından farkını üretim öncesinde yaz.'})

def P(d):return next(p for p in posts if p['day']==d)
def revisit(day,aa,body,fmt='Single',hook=None):
 p=P(day);p['asset_ids']=aa;p['format']=fmt;p['caption_en']=body+'\n\n'+credit(works[p['work_key']]);p['title_en']=hook or works[p['work_key']]['title'];p['why_this_post_tr']='Önceki bütün sunumundan farklı görüntü/bilgi: '+body
revisit(52,['A0023'],'An earlier recorded state of Painstaking. The finished triptych was shown earlier; this image preserves a different stage.',hook='An earlier state of Painstaking')
revisit(108,['A0017'],'A close view of a painted eye in Painstaking. The surface has its own pace.',hook='A painted eye, close up')
revisit(157,['A0008'],'Two faces meet across the physical gap between the panels of Painstaking.',hook='Across the gap between panels')
revisit(59,['A0224','A0225','A0258'],'Two details from walls of perception: the hat and face, then the plate and fork. The last image locates both within the whole painting.',fmt='Carousel',hook='A hat, a plate, a different viewing distance')
revisit(115,['A0226'],'A flower within walls of perception. A small passage from the complete painting shown earlier.',hook='A small flower in the green field')
revisit(164,['A0227'],'A close view of the yellow passage and the red table in walls of perception.',hook='Where yellow meets red')
revisit(87,['A0096'],'A close view of the face in s(t)lop. The surrounding marks stay visible.',hook='Inside the face of s(t)lop')
revisit(136,['A0098'],'A different passage from s(t)lop: the upright object beside the figure.',hook='Beside the figure')
revisit(94,['A0289'],'The face and cigar in gary grills cooper. A close view from the full painting shown earlier.',hook='The face, close up')
revisit(80,['A0582'],'The complete Virgil on Virtual Cage, with the room kept around the figures.',hook='The complete room and group')
revisit(101,['A0160'],'The complete square of articulo attack on mandarin. A quiet full view after the selected details shown earlier.',hook='The complete square')
revisit(122,['A0296'],'The hands and match in gary grills cooper. Another part of the figure comes forward at this distance.',hook='The hands and the match')
revisit(143,['A0293'],'The grill in gary grills cooper. A surface detail from the painting.',hook='The grill, close up')
revisit(150,['A0139'],'A selected detail from articulo attack on mandarin. The square painting was shown in full earlier in this selection.',hook='A detail from articulo attack on mandarin')
revisit(129,['A0502'],'The hanging chair in Virgil on Virtual Cage. A small object within the room surrounding the group.',hook='The hanging chair')
revisit(178,['A0504','A0582'],'The ceiling and corner in Virgil on Virtual Cage. The second image restores their position within the room.',fmt='Carousel',hook='The room around the group')
revisit(171,['A1560','A1564','A1559','A1378'],'Recorded stages of Angora Mergvs. The buildings remain recognisable while their colour relationships change.',fmt='Carousel',hook='Angora Mergvs: recorded stages')
def shot(o0,o1,aid,ins,outs,text,note,speed=1):return {'out_start':o0,'out_end':o1,'asset_id':aid,'source_in':ins,'source_out':outs,'speed':speed,'on_screen_en':text,'edit_tr':note}
P(1)['shots']=[
 shot(0,2,'A2802',62,64,'This figure changes.','İlk kare gerçek el/fırça hareketi; logo yok.'),
 shot(2,7,'A2802',36,41,'Earlier in the session','Koyu alan genişlemeden önceki hâl. Zamanın geriye alındığını açıkla.'),
 shot(7,15,'A2802',58,74,'','2×; alt figürdeki değişim görünür. Kamera hareketi/renk efekti ekleme.',2),
 shot(15,23,'A2802',83,99,'','2×; bir sonraki gerçek çalışma aralığı.',2),
 shot(23,26,'A2802',110,113,'A recorded painting stage','Son çalışma durumu; final tuvalle aynı aşama gibi eşitleme.'),
 shot(26,32,'A1832',None,None,'The finished painting, later.\n2020','Tek sabit kapanış. Sarıdan koyu final zemine dönüşen tüm sürecin çekildiği iddiası yok.')]
P(1)['cover_en']='A FIGURE IN CHANGE'
P(1)['caption_en']='From the 2020 studio archive. Watch the dark paint take over the lower figure.\n\nThe clip records an intermediate stage of the painting. The final image shows the later finished work.\n\n'+credit(works['capricorn'])+'\n\n'+music_credit('M1')
P(1)['voiceover_en']=None;P(1)['sound_tr']='Kaynak sesi kapat; arka plandaki müziği taşıma. Signal to Noise 00:30–01:02, düşük seviyede; müzik bölümü final kurguda dinlenerek eşlenecek.'
P(1)['story_text_en']='A painting stage from the 2020 studio archive.'
P(3)['slides']=[{'page':1,'asset_id':'A0025','text_en':'Painstaking · 2026','edit_tr':'Tam triptik; yazı resim dışında küçük. Üç yüz bir arada ilk görüntü.'},{'page':2,'asset_id':'A0028','text_en':'Left panel','edit_tr':'Sol panel; yeniden renk işlemi yok.'},{'page':3,'asset_id':'A0029','text_en':'Centre panel','edit_tr':'Orta panel.'},{'page':4,'asset_id':'A0027','text_en':'Right panel','edit_tr':'Sağ panel. Bir ders/ikinci Reel vaat etme.'}]
P(3)['caption_en']=credit(works['painstaking'])
P(3)['cover_en']='Painstaking';P(3)['sound_tr']='Müzik yok. Tamamlanmış eser kendi başına durur.'
P(3)['story']='Otomatik destek Story’si yok. Aynı triptiğin ayrıntılarını başka günlere dağıtma.'
P(5)['caption_en']=archive_notes[1]+'\n\nArchive drawing · undated\nYiğit Özen'
P(5)['alt_text_en']='An archive study with overlapping drawn bodies, long reaching arms and a red passage at the centre.'
P(5)['sound_tr']='Müzik yok.';P(5)['story']='Story gerekmez. Bu çizim bir sonraki postun tanıtımı olarak kullanılmaz.'
P(8)['shots']=[
 shot(0,3,'A0620',56,59,'What would you leave alone?','Tablonun başındaki gerçek konuşmadan aç. Bu İngilizce cümle editoryal soru; birebir alıntı değil.'),
 shot(3,12,'A0620',59,68,'Darken the pieces.','Çekimdeki el ve tablo ilişkisi. Türkçe konuşma yerine aşağıdaki İngilizce anlatım.'),
 shot(12,18,'A0620',71,77,'Leave the background.','Sohbetin gerçek iki kararına dayanan kısa özet; sahte anlaşmazlık ekleme.'),
 shot(18,24,'A0592',None,None,'The painting under discussion','Tamamlanmış esere tek geçiş; konuşma anındaki tuval ile finalin aynı aşama olduğunu iddia etme.'),
 shot(24,28,'A0620',77,81,'A studio conversation.','Tekrar gerçek atölyeye dön. Son cümleyle doğal kapanış.')]
P(8)['voiceover_en']='The suggestion was to darken the pieces, but leave the background alone. This studio conversation is about two decisions: what still needs work, and what already holds together.'
P(8)['caption_en']='The studio conversation came down to two things: darken the pieces, and leave the background alone.\n\nA moment from working on 7 fam board game.\n\n'+credit(works['board'])
P(8)['cover_en']='WHAT WOULD YOU LEAVE ALONE?'
P(8)['sound_tr']='Müzik yok. İngilizce anlatım taslağı sanatçı tarafından kaydedilecek; Türkçe kaynak sesini alıntı/dublaj gibi dudakla eşleme. Anlatım, A0620 28–84 sn dökümündeki konuşmanın editoryal özetidir.'
P(8)['story_text_en']='One thing to change. One thing to leave alone.'
P(10)['shots']=[
 shot(0,4,'A1632',196,200,'This started with my childhood home.','Gerçek sanatçı konuşması ilk karede. İngilizce anlatım birinci tekil taslak; aşağıdaki kaynak kapsamına bağlı.'),
 shot(4,14,'A1632',200,210,'','Video devam ederken A1378 tam eser tek bindirme; sanatçı görüntüsünü tümüyle yok etme.'),
 shot(14,24,'A1632',308,318,'The house began to take over.','Anı anlatımındaki gerçek el hareketleri; ikinci bir fotoğraf dizisi ekleme.'),
 shot(24,34,'A1632',616,626,'A visitor, or a threat?','A1378 içinde figürü işaretleyen tek sabit crop/bindirme; gerçek konuşma arka planda sürer.'),
 shot(34,38,'A1378',None,None,'Angora Mergvs · 2026','Tek bitmiş eser kapanışı.')]
P(10)['voiceover_en']='I put a childhood character above the house I grew up in. I wanted the house to be a main character too. The visitor is familiar, but there is something uncertain about its arrival: is it coming back, or coming to attack?'
P(10)['caption_en']='I put a childhood character above the house I grew up in. The house began to take over the painting.\n\nA familiar visitor can carry a feeling of return, but also a sense of threat.\n\n'+credit(works['angora'])
P(10)['cover_en']='MY CHILDHOOD HOME, REVISITED'
P(10)['sound_tr']='Müzik yok. Yeni İngilizce ses kaydı metni, mevcut Türkçe anlatının 196–224 / 308–364 / 616–644 sn bölümlerinden yaratıcı uyarlama. Henüz kayıt alınmadı; onaylanmış birebir çeviri veya eski videoda söylenmiş İngilizce söz değil.'
P(10)['story_text_en']='The house in this painting is the house I grew up in.'
P(12)['caption_en']='From the Milan archive.\n\n'+credit(works['ciao'])
P(12)['sound_tr']='Müzik yok.';P(12)['story']='Story zorunlu değil; tamamlanmış eski eser için izleyiciye bakma alanı bırak.'
for p in posts:
 if p['day']<=14:
  p['detailed']=True;p['export_tr']='Video 1080 × 1920; kaynak yataysa el, tablo ve kişi ilişkisini koruyan yatay pencereyi dikey alana yerleştir. Ekranı doldurmak uğruna tabloyu kesme. Statik yayın 1080 × 1350 sRGB JPEG; oranı koru.'
  p['caption_status']='İngilizce yayın taslağı. Ses metni olan iki Reel’de İngilizce kayıt gerekli; henüz medya export edilmedi.'
  p['alt_text_en']={1:'A filmed painting session shows dark paint spreading over the lower figure in a yellow-ground stage of caprocorn sister. The finished dark-field work appears at the end.',3:'Painstaking, 2026, a triptych of distorted faces. Four images show the whole arrangement followed by the left, centre and right panels.',5:'An archive drawing with overlapping bodies, long reaching arms and a red passage at the centre.',8:'Two people discuss a painting laid on a studio table. The completed chess-scene painting appears once during the excerpt.',10:'The artist speaks at a desk. The painting Angora Mergvs appears over the footage, showing a blue house with an orange winged figure above it.',12:'ciao capo, sono squalo, 2020: two elongated blue and white figures against a red-and-black field.'}[p['day']]
 else:p['detailed']=False
 p['assets']=[{'id':i,'path':assets[i]['path'],'relative_path':assets[i]['relative_path'],'kind':assets[i]['kind'],'sha256':assets[i].get('sha256')} for i in p['asset_ids']]
 p['caption_file']=f'captions-v2/GUN-{p["day"]:03}.txt'
 (OUT/p['caption_file']).write_text(p['caption_en']+'\n',encoding='utf-8')

days=[]
byday={p['day']:p for p in posts}
for d in range(1,181):
 p=byday.get(d);day={'day':d,'week':(d-1)//7+1,'timezone':'Europe/Paris','actual_published_at':None,'is_feed_post':p is not None}
 if p:day.update(post_id=p['id'],time=p['time'],format=p['format'],task=p['title_en'])
 else:day.update(time='18:00' if (d-1)%7+1 in [2,6,7] else None,format='No feed post',task='Kurgu/yanıt/ölçüm; paylaşım yok. Story yalnız gerçekten yeni bir şey varsa.')
 if (d-1)%7+1==6:day['task']='Sonraki haftanın 3 farklı eserini ve video olayını hazırla; aynı eserin tekrar aralığını kontrol et.'
 if (d-1)%7+1==7:day['task']='Aynı yaştaki sonuç, ilgili sorular ve üretim süresi; tek sonraki karar. Zorunlu paylaşım yok.'
 if d in [14,30,60,90,120,150,180]:day['milestone']='İlgili devam, paylaşım/kayıt, iş yükü ve tekrar yorgunluğu; tek sonuç garantisi yok.'
 days.append(day)

refs=[{'name':'T17 · Saat ve sıklık','url':'https://github.com/decentralize-dfw/u320x/blob/23e3dd0cb7effcaec2904d5ddeb49e9888abb0a5/instagram/03-tactics/tactics-q17-answer-20261016.md','finding':'Günlük kota veya ideal saat yok; sürdürülebilir kapasite ve dönem toplamı/gönderi başına sonuç birlikte.'},{'name':'T23 · Eserin inceleme ihtiyacı','url':'https://github.com/decentralize-dfw/u320x/blob/23e3dd0cb7effcaec2904d5ddeb49e9888abb0a5/instagram/03-tactics/tactics-q23-answer-20261016.md','finding':'Bitmiş eser, süreç ve anlatı farklı soruları karşılar; hepsini her postta zorunlu kılma.'},{'name':'T55 · Yeniden kullanım','url':'https://github.com/decentralize-dfw/u320x/blob/23e3dd0cb7effcaec2904d5ddeb49e9888abb0a5/instagram/03-tactics/tactics-q55-answer-20261016.md','finding':'Aynı görüntünün dosyasını değiştirmek yetmez; yeni bilgi ve inceleme değeri gerekir.'},{'name':'T45 · Kurgu ve süre','url':'https://github.com/decentralize-dfw/u320x/blob/23e3dd0cb7effcaec2904d5ddeb49e9888abb0a5/instagram/03-tactics/tactics-q45-answer-20261016.md','finding':'Her kesmenin bilgi işi olmalı; hızlı kurgu ve kısa süre kendi başına amaç değil.'}]
plan={'schema':'instagram-fourth-leg-180-v2','written_at':'2026-11-04','supersedes':'publication-plan-180-v1-superseded','status':'planned_not_launched','language':'en','timezone':'Europe/Paris','start_date':None,'day_count':180,'feed_count':len(posts),'rhythm':'Haftada 3 akış; döngü gün 1/3/5. Her hafta farklı üç eser. 1–2 eski iş/eskiz; ilk 14 gün 6 yayın.','frequency_basis':'Editoryal başlangıç tercihi; araştırmanın bulduğu optimum sıklık değil.','repeat_gap_days':14,'repeat_gap_is_algorithm_rule':False,'advertising':{'active_budget_eur':0,'activation_day':None,'ceiling_extension_approved':False},'strategy_sources':refs,'first_two_weeks_new_english_voice_recordings_needed':[8,10],'days':days,'weeks':weeks,'posts':posts}
save(OUT/'plan-180.json',plan)
save(OUT/'revision-decisions.json',{'date':'2026-11-04','superseded_feed_count':129,'new_feed_count':78,'superseded_first_14_days':10,'new_first_14_days':6,'painstaking_first_14_days':[3],'reason':'Aynı triptiğin tekrarını kaldırmak; gerçek videoyu olay/anlatı ile kullanmak; arşiv ve eskize yer açmak; yayın dışı günleri korumak.','preserved':['Gün numarası','İngilizce yayın dili','Niş ve ilgili devam hedefi','Europe/Paris 19.00 başlangıç saati','Reklamın organik sonuçtan sonra değerlendirilmesi','24/72/168 saat ölçümü'],'sources':refs})
save(OUT/'works.json',works)
for filename,items in [('YAYIN-TAKVIMI-180.csv',posts),('GUN-GUN-180.csv',days)]:
 fields=list(dict.fromkeys(k for row in items for k in row if k not in ['shots','slides','assets']))
 with (OUT/filename).open('w',encoding='utf-8-sig',newline='') as f:
  writer=csv.DictWriter(f,fields,extrasaction='ignore');writer.writeheader()
  for row in items:writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in row.items() if k in fields})
usage=collections.defaultdict(list)
for p in posts:
 for a in p['asset_ids']:usage[a].append(p['day'])
save(OUT/'asset-usage.json',[{'asset_id':a,'path':assets[a]['path'],'days':v} for a,v in usage.items()])
save(OUT/'measurement-log.json',{'baseline_followers':None,'actual_published_at':None,'entries':[{'id':p['id'],'planned_day':p['day'],'actual_published_at':None,'production_minutes':None,'paid_spend_eur':None,'observations':[{'age_hours':h,'reach':None,'views':None,'shares':None,'saves':None,'attributed_follows':None,'work_specific_questions':None} for h in [24,72,168]]} for p in posts]})

E=lambda s:html.escape(str(s))
def src(i):return f'<a href="{E(Path(assets[i]["path"]).as_uri())}">{E(i)} · {E(Path(assets[i]["path"]).name)}</a>'
def thumb(i):return '../../archive-audit/'+('video-sheets/' if assets[i]['kind']=='video' else 'thumbs/')+i+'.jpg.webp'
def gallery(p):return '<div class="assets">'+''.join(f'<a href="{E(Path(assets[i]["path"]).as_uri())}"><img loading="lazy" src="{thumb(i)}" alt="{E(i)}"><span>{E(i)} · {"VIDEO" if assets[i]["kind"]=="video" else "IMAGE"}</span></a>' for i in p['asset_ids'])+'</div>'
style=re.search(r'<style>(.*?)</style>',(OLD/'PLAN-180.html').read_text(encoding='utf-8'),re.S)[1]
def card(p):
 w=works[p['work_key']];body=f'<article class="post" id="day-{p["day"]}" data-week="{p["week"]}" data-format="{p["format"]}"><div class="eyebrow">Gün {p["day"]} · 19.00 Paris · {E(p["format"])} · {"ARŞİV" if p["is_archive"] else "2026"}</div><h3>{E(p["title_en"])}</h3><p><b>Bu yayının işi:</b> {E(p["why_this_post_tr"])}</p>'+gallery(p)+f'<p><b>Kurgu:</b> {E(p["edit_tr"])}</p>'
 if p.get('shots'):
  body+='<h4>Saniyeli kurgu · ilk iki haftanın kesin kaynak aralıkları</h4><table><tr><th>Çıktı</th><th>Kaynak / zaman</th><th>English screen text</th><th>Uygulama</th></tr>'
  for s in p['shots']:
   tc=f'{s["source_in"]}–{s["source_out"]} sn · {s["speed"]}×' if s['source_in'] is not None else 'Sabit kapanış'
   body+=f'<tr><td>{s["out_start"]}–{s["out_end"]} sn</td><td>{src(s["asset_id"])}<br>{tc}</td><td class="english">{E(s["on_screen_en"])}</td><td>{E(s["edit_tr"])}</td></tr>'
  body+='</table>'
 if p.get('slides'):
  body+='<h4>Sayfalar</h4><table><tr><th>Sayfa</th><th>Kaynak</th><th>Metin</th><th>Uygulama</th></tr>'+''.join(f'<tr><td>{s["page"]}</td><td>{src(s["asset_id"])}</td><td>{E(s["text_en"])}</td><td>{E(s["edit_tr"])}</td></tr>' for s in p['slides'])+'</table>'
 if p.get('voiceover_en'):body+='<h4>English narration · yeni kayıt metni</h4><pre>'+E(p['voiceover_en'])+'</pre>'
 if p.get('sound_tr'):body+='<p><b>Ses:</b> '+E(p['sound_tr'])+'</p>'
 else:body+='<p><b>Ses:</b> '+('Müzik yok; anlatı için İngilizce ses uyarlaması.' if p['format']=='Reel' and p['music_id']=='M0' else 'Signal to Noise · Scott Buckley, 00:30’dan süre kadar; son kurguya göre dinleyerek eşleştir.' if p['music_id']=='M1' else 'Müzik yok.')+'</p>'
 if p.get('export_tr'):body+='<p><b>Export:</b> '+E(p['export_tr'])+'</p>'
 body+=f'<details {"open" if p["detailed"] else ""}><summary>English caption</summary><pre>{E(p["caption_en"])}</pre><a href="{E(p["caption_file"])}">Caption dosyası</a></details><p><b>Story:</b> {E(p["story"])}</p>'
 if p['detailed']:body+=f'<p><b>İsteğe bağlı İngilizce Story metni:</b> {E(p["story_text_en"])}</p>'
 body+='<p class="muted">Yayın ve render yapılmadı. '+E(p['source_selection_status'])+'.</p></article>';return body
def head(title):return '<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+E(title)+'</title><style>'+style+'</style></head><body><main>'
intro='''<p class="eyebrow">yigitozen.art · Ayak 4 · 4 Kasım 2026 revizyonu</p><h1>Farklı işler, gerçek videolar, arşive yer açan düzen</h1><p class="lead">180 günlük taslak haftada üç akış yayınına indirildi. İlk iki haftada altı farklı eser var. Painstaking yalnız Gün 3’te. Aynı eseri Reel, carousel ve tek görsel diye art arda çoğaltmıyoruz.</p><div class="stats"><div class="stat"><b>78</b>180 günde yayın</div><div class="stat"><b>6</b>ilk 14 günde yayın</div><div class="stat"><b>1–2</b>haftalık eski iş/eskiz</div><div class="stat"><b>0</b>ilk 14 günde salt slayt Reel</div></div><p class="notice">Bu bir editoryal başlangıç düzenidir; araştırmanın bulduğu ideal kota değildir. Üç yayın 14 gün denenir, kalite ve ilgili sonuçlarla değerlendirilir. Yayın dili İngilizce; hazırlık notları Türkçe.</p>'''
principles='''<section class="panel"><h2>Araştırma ne diyor, bu revizyon neyi değiştiriyor?</h2><p>Her gün post zorunluluğu yok. Önceki beş yayınlık düzen strateji metnindeki başlangıç tasarımıydı; platform kuralı veya kanıtlanmış en iyi sıklık değildi. Bu revizyonda döngü günleri 1, 3, 5 yayın; aradaki günler üretim, gerçek yanıt ve ölçüm için boş.</p><p>Düzen eser tekrarına değil üç farklı işe dayanıyor: hareket veya hikâye taşıyan video; başka bir tamamlanmış esere bakma alanı; kendi başına değerli eski iş veya eskiz. Her hafta üç farklı eser. Bazı haftalarda arşiv videosuyla birlikte iki eski iş, diğerlerinde bir eski iş var.</p><p>Reel yalnız biçim değil, olay taşır. Fırçanın bir alanı değiştirmesi, stüdyodaki gerçek konuşma veya sanatçının görünmeyen bir kişisel sebebi anlatması. Sabit fotoğraf geçişleri ve “bütüne dön” şablonu ana Reel formatı olmaktan çıkarıldı. Gereken statik görüntü tek açıklama/kapanış olarak kullanılabilir.</p><p>Aynı eserin yeniden kullanımı için en az 14 günlük editoryal aralık ve yeni bilgi gerekir. Bu süre algoritma güvenlik eşiği değildir. Yeni bilgi yoksa aralık dolsa da yayın yapılmaz. İlk iki haftada altı yayın, altı farklı eser; aynı gün/ertesi gün tekrar yok.</p><p>Eski çizimlerin tarihi bilinmiyorsa <em>undated</em> yazılır. Tamamlanmış eserin yılı çizime taşınmaz. İngilizce başlık/voiceover kişisel bir sebep anlatıyorsa mevcut sanatçı kaydına bağlanır; uydurma çocukluk veya üretim anı eklenmez.</p><p>İlgiyi hiç kaybetmeme garantisi veremeyiz. Yayın öncesinde üç kontrol: önceki yayından görsel olarak ayrılıyor mu; yeni bir şey veriyor mu; bu fikrin video olması gerçekten gerekiyor mu? Üçüne de güçlü cevap yoksa slot boş kalır.</p></section>'''
research='<section class="panel"><h2>Kararların araştırma dayanağı</h2><ul>'+''.join(f'<li><a href="{E(r["url"])}">{E(r["name"])}</a> — {E(r["finding"])}</li>' for r in refs)+'</ul><p>Bunlar depodaki 16 Ekim araştırma sürümünün sonuçları. Bu revizyon yeni bir canlı Instagram deneyi veya yeni algoritma kanıtı değildir.</p></section>'
readiness='''<section class="panel"><h2>İlk iki haftanın üretim durumu</h2><p>Gün 1 mevcut gerçek boyama kaydından; Gün 8 mevcut stüdyo konuşmasından; Gün 10 mevcut sanatçı anlatımından kurgulanır. Yeni video çekimi zorunlu değil. Gün 8 ve 10 için İngilizce ses metinleri yazıldı; İngilizce kayıt henüz alınmadı. Bu kayıt olmadan metinler “yayına hazır medya” sayılmaz.</p><p>Gün 3’te Painstaking bir kez ve dört fotoğrafla sunulur. Bu dört sayfa dört ayrı yayın değildir: bütün, sol, orta ve sağ panel. Gün 5 bağımsız bir eski çizim, Gün 12 bağımsız bir Milan eseri.</p><p>19.00 Europe/Paris başlangıç saati korunur; en iyi saat iddiası yok. Müzik her yayına zorla eklenmez. D01 için Signal to Noise önerisi ve kredisi korunur; bölüm final kurguda dinlenerek eşlenecek. Diğer iki Reel anlatımı öne alır.</p><p>Kaynak zamanları görüntü kontrolü ve önceki tam dosya taramasına bağlı kurgu aralıklarıdır; ağızdan çıkan her sözün elle dinlenmiş dökümü değildir. Türkçe dökümler birebir İngilizce altyazı diye sunulmadı; yeni İngilizce anlatım metni açıkça ayrıldı.</p></section>'''
measure='''<section class="panel"><h2>İki hafta sonra hangi kararı vereceğiz?</h2><p>Her yayını kendi 24/72/168 saat yaşında ölç. Erişim, varsa izleme süresi, paylaşma, kaydetme, esere özgü soru, varsa gönderiye atfedilen takip ve üretim dakikasını ayrı yaz. İlk günde az diye silme; görünmeyen veriye sıfır yazma.</p><p>Üç yayında anlamlı iş ve devam üretebiliyorsak düzeni sürdür. Dördüncü yayın yalnız gerçekten ayrı ve hazır bir içerik varsa düşünülür. Frekans değişen hafta aynı anda saat, kanca ve müzik testi açılmaz. İlgi düşüşünü tek başına algoritma cezası sayma.</p><p>Gün 14/30/60/90/120/150/180 kontrolleri korunur. Reklam başlangıcı atanmadı; önce organik içerik ve gerçek sonuç. Son gönderinin yedi günlük ölçümü Gün 187’de tamamlanır.</p></section>'''
nav='<nav><a href="PLAN-180.html">180 gün</a><a href="ILK-14-GUN.html">İlk 14 gün</a><a href="YAYIN-TAKVIMI-180.csv">78 yayın CSV</a><a href="GUN-GUN-180.csv">180 gün görevleri</a><a href="plan-180.json">Plan JSON</a><a href="../../archive-audit/ARSIV-AUDIT.html">Arşiv audit</a></nav>'
def calendar(items):
 body='<table><thead><tr><th>Gün</th><th>Saat</th><th>İş</th><th>İçerik</th></tr></thead><tbody>'
 for d in items:
  body+=f'<tr><td>{"<a href=\"#day-"+str(d["day"])+"\">"+str(d["day"])+"</a>" if d["is_feed_post"] else d["day"]}</td><td>{d.get("time") or "—"}</td><td>{E(d["format"])}</td><td>{E(d["task"])}</td></tr>'
 return body+'</tbody></table>'
first=head('İlk 14 gün · çeşitlilik ve gerçek video revizyonu')+intro+nav+principles+readiness+'<section class="panel"><h2>İlk 14 gün</h2>'+calendar(days[:14])+'</section>'
first+=''.join(card(p) for p in posts if p['day']<=14)+research+measure+'</main></body></html>'
(OUT/'ILK-14-GUN.html').write_text(first,encoding='utf-8')
doc=head('180 gün · haftada üç farklı iş')+intro+nav+principles+research+readiness
doc+='<section class="panel"><h2>26 haftalık omurga</h2><table><tr><th>Hafta</th><th>Video</th><th>Diğer eser</th><th>Eski iş/eskiz</th></tr>'
for w in weeks:
 a,b,c=[works[k]['title'] for k in w['work_keys']];doc+=f'<tr><td><a href="#day-{w["days"][0]}">{w["week"]}</a></td><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td></tr>'
doc+='</table></section><h2>Yayın kartları</h2><div class="tools"><label>Hafta <select id="week"><option value="all">Tümü</option>'+''.join(f'<option value="{i}">{i}</option>' for i in range(1,27))+'</select></label><label>Format <select id="format"><option value="all">Tümü</option><option>Reel</option><option>Carousel</option><option>Single</option></select></label><label>Ara <input id="search"></label><span id="count"></span></div>'
for w in weeks:
 doc+=f'<section class="week" data-week="{w["week"]}"><h2>Hafta {w["week"]} · Gün {w["days"][0]}–{w["days"][1]}</h2><p class="muted">{w["archive_feed_count"]} eski iş/eskiz yayını. Üç farklı eser; aynı işin üç formata bölünmesi yok.</p>'
 doc+=''.join(card(p) for p in posts if p['week']==w['week'])+'</section>'
doc+=measure+'''<script>const W=document.querySelector('#week'),F=document.querySelector('#format'),S=document.querySelector('#search');function filter(){let n=0;document.querySelectorAll('.post').forEach(p=>{const ok=(W.value==='all'||p.dataset.week===W.value)&&(F.value==='all'||p.dataset.format===F.value)&&(!S.value||p.innerText.toLowerCase().includes(S.value.toLowerCase()));p.classList.toggle('hidden',!ok);if(ok)n++});document.querySelectorAll('.week').forEach(w=>w.classList.toggle('hidden',![...w.querySelectorAll('.post')].some(p=>!p.classList.contains('hidden'))));document.querySelector('#count').textContent=n+' yayın'}W.onchange=F.onchange=S.oninput=filter;filter();</script></main></body></html>'''
(OUT/'PLAN-180.html').write_text(doc,encoding='utf-8')
save(OUT/'validation.json',{'status':'pending_external_validation','posts':len(posts),'days':len(days)})
print('Generated',len(posts),'posts;',dict(collections.Counter(p['format'] for p in posts)))
