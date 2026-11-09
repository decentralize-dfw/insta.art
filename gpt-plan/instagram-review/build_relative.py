import json, re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'source/instagram/04-strategy'
OUT = ROOT / 'working'
OUT.mkdir(exist_ok=True)
plan = json.loads((SRC / 'strategy-plan-data-20261016.json').read_text(encoding='utf-8'))
repo = 'https://github.com/decentralize-dfw/u320x/blob/23e3dd0cb7effcaec2904d5ddeb49e9888abb0a5/instagram/'

def neutral(text):
    text = text.replace('21–27 Aralık tatil bağlamını not et.', 'Gerçek uygulama döneminde tatil/etkinlik varsa bağlamını kaydet.')
    text = text.replace('28 Aralık–3 Ocak bağlamı ayrı;', 'Gerçek uygulama döneminin bağlamı ayrı;')
    text = text.replace('E10: yıl dönümü bağlamında', 'E10: seçili üretim dönemi bağlamında')
    text = text.replace('Bir yıldan seçki:', 'Bir üretim döneminden seçki:')
    text = text.replace('2026 seçkisinden iki uygun iş', 'Doğru yılları belirtilmiş seçkiden iki uygun iş')
    text = text.replace('2026 dışında işi 2026 diye ekleme.', 'Her işin gerçek yılını kullan.')
    text = text.replace('son B 17 Ocak 00.00 kapanır.', 'son B Gün 91 başlangıcında kapanır.')
    text = text.replace('6 günlük kısmi hafta; Pazar incelemesi 90 gün dışında, son değerlendirme Cumartesi 23.59.', '6 günlük kısmi hafta; son değerlendirme Gün 90 saat 23.59; döngünün 7. günü plan dışında.')
    return text

def walk(value):
    if isinstance(value, str): return neutral(value)
    if isinstance(value, list): return [walk(x) for x in value]
    if isinstance(value, dict): return {k: walk(v) for k,v in value.items()}
    return value

plan = walk(plan)
plan['schema'] = 'instagram-relative-plan-v2'
plan['snapshot_commit'] = '23e3dd0cb7effcaec2904d5ddeb49e9888abb0a5'
plan['start'] = None
plan['end_inclusive'] = None
plan['schedule_basis'] = 'relative_local_days_1_to_90_no_weekday_requirement'
plan['activation_rule'] = 'Gün 1 ilk gerçek yayın günüdür. Hazırlık Gün 1 öncesindedir. Gerçek yayın ve ölçüm zamanları ayrıca kaydedilir.'
plan['measurement_rule'] = '24/72/168 saat gerçek yayın zamanından geçen süredir. Yaz/kış saati geçişinde yerel saat otomatik aynı kalmayabilir.'
plan['advertising_duration_rule'] = 'Her dönem üç yerel takvim günüdür; saat değişiminde 71/73 saat olabilir. Toplam dönem bütçesi 15 EUR korunur.'
for i, f in enumerate(plan['flights']):
    start = (f['week']-1)*7 + (1 if f['id'].endswith('-A') else 4)
    for key in ['start_local','end_exclusive_local','calendar_ad_days']: f.pop(key)
    f.update(start_day=start, end_exclusive_day=start+3, calendar_ad_day_numbers=list(range(start,start+3)), local_boundary_time='00:00')
for d in plan['days']:
    d.pop('date'); d.pop('weekday')
    d['cycle_day'] = (d['day']-1)%7+1
    d['label'] = f"Gün {d['day']}"

(OUT / 'plan-gun-1-90.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
template = json.loads((SRC / 'strategy-measurement-template-20261016.json').read_text(encoding='utf-8'))
template['baseline']['plan_day'] = 0
(OUT / 'olcum-sablonu.json').write_text(json.dumps(template,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lines = ['# Gün 1–90 uygulama takvimi', '', 'Durum: planlandı; yayın ve reklam başlamadı. Gün 1 ilk gerçek yayın günüdür; haftanın herhangi bir günü başlayabilir. Hazırlık dönemi 90 güne dahil değildir.', '', '**Korunan hacim:** 39 Reel + 13 carousel + 13 tek görsel = 65 yayın. Reklam: 26 dönem × 15 € = 390 € üst plan bütçesi. Atlanan dönem bütçesi kendiliğinden aktarılmaz.', '', '**Saat:** Europe/Paris yerel saatiyle yayın 19.00; üretim/değerlendirme 18.00. Bunlar başlangıç denemesidir. Ölçüm 24/72/168 saat gerçek yayın zamanından hesaplanır; saat değişimi varsa geçen süre esas alınır.', '', '**Reklam:** Her yedi günlük döngünün 1–3. günleri A, 4–6. günleri B; 7. gün reklam yok. Bitiş sonraki gün 00.00 ve hariçtir. Üç yerel gün saat değişiminde 71/73 saat olabilir. Dönem toplam sınırı 15 €; günlük 5 € ortalama. Gün 1 başında hazır aday yoksa dönem atlanır; eksik içeriğe harcama yapılmaz.', '', '**Hazırlık / Gün 1 öncesi:** başlangıç ölçümü; doğru eser künyeleri; ilk haftanın beş dosyası; bio ve üç sabit içerik taslağı; çalışan portföy bağlantısı; reklamın hak/hedef/bölge/varış kontrolü.', '', '**Kontroller:** Gün 14 sürdürülebilirlik; Gün 30 darboğaz; Gün 60 tekrar edilebilirlik; Gün 90 sonuç. Gün 91–97 yalnız son yayınların olgunlaşan ölçümlerini tamamlar; büyüme hedefini uzatmaz.', '', '**Yedek düzen:** iki hafta üst üste iş yükü eser üretimini aksatırsa döngü gün 1 Reel + gün 2 carousel + gün 5 tek görsel. Aynı hafta başka içerik değişkeni test edilmez.', '', '**Kaynaklar:** Bu yerel sürüm depodaki stratejinin gün numaralı türevidir. Araştırmanın bütün kaynakları yeniden doğrulanmadı. Belge ve künye kaynağı bağlantıları GitHub anlık görüntüsüne gider.', '']
for wi, w in enumerate(plan['weeks'],1):
    a=(wi-1)*7+1; b=min(a+6,90)
    lines += [f"## Hafta {wi} / Gün {a}–{b} — {w['theme']}", '', f"**Sütun / işler:** {w['pillar']} / {w['works']}", '', f"**Soru:** {w['question']}", '', f"**Deney:** {w['test']}", '', f"**Sabitler:** {w['keep']}", '', f"**Çekim:** {w['make']}", '', f"**Sanat çevresi:** {w['gallery']}", '', f"**Reklam kararı:** {w['paid']}", '', '| Gün | Saat / format | İçerik ve uygulama | Story | Reklam / ölçüm |', '|---|---|---|---|---|']
    for d in plan['days'][a-1:b]:
        ad=f"{d['ad_flight']} · ort. 5 €; dönem 15 €" if d['ad_flight'] else 'Reklam yok'
        obs=', '.join(d['observation_ids']) or 'Henüz ölçüm yok'
        cells=[d['label'],f"{d['local_time']} / {d['format']}",d['action'],d['story_task'],f'{ad}; {obs}']
        lines.append('| '+' | '.join(x.replace('|',' / ') for x in cells)+' |')
    refs=sorted(set(p for d in plan['days'][a-1:b] for p in d['sources']))
    lines += ['', '**Dayanak:** '+' · '.join(f'[{Path(p).stem}]({repo}{p})' for p in refs), '']
lines += ['## Reklam dönemleri', '', '| Dönem | Başlangıç | Bitiş, hariç | Toplam sınır |', '|---|---|---|---|']
for f in plan['flights']:
    lines.append(f"| {f['id']} | Gün {f['start_day']} 00.00 | Gün {f['end_exclusive_day']} 00.00 | 15 € |")
(OUT / 'takvim-gun-1-90.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

# Takvim dönüşümünde maddi kayıp veya uydurma gerçekleşme olmadığını kontrol et.
assert [d['day'] for d in plan['days']] == list(range(1,91))
assert Counter(d['format'] for d in plan['days']) == {'Reel R1':13,'Reel R2':13,'Reel R3':13,'Carousel C1':13,'Tek görsel P1':13,'Üretim / veri':13,'Değerlendirme':12}
assert sum(d['is_feed_post'] for d in plan['days']) == 65
assert sum(f['planned_lifetime_limit_eur'] for f in plan['flights']) == 390
assert sum(d['planned_media_average_eur'] for d in plan['days']) == 390
ad_days=[n for f in plan['flights'] for n in f['calendar_ad_day_numbers']]
assert len(ad_days)==len(set(ad_days))==78 and min(ad_days)==1 and max(ad_days)==90
assert all(d['ad_flight']==next((f['id'] for f in plan['flights'] if d['day'] in f['calendar_ad_day_numbers']),None) for d in plan['days'])
original=json.loads((SRC / 'strategy-plan-data-20261016.json').read_text(encoding='utf-8'))
assert all(d['observation_ids']==o['observation_ids'] and d['sources']==o['sources'] for d,o in zip(plan['days'],original['days']))
assert all(d['actual_published_at'] is None and d['status']=='planned_not_published' for d in plan['days'])
assert all(f['actual_spend_eur'] is None and f['status']=='planned_not_launched' for f in plan['flights'])
assert not any('2026-' in json.dumps(d) or '2027-' in json.dumps(d) for d in plan['days'])
assert len(re.findall(r'^\| Gün \d+ \|', '\n'.join(lines),re.M))==90
(OUT / 'dogrulama.txt').write_text('PASS: 90 sıralı gün; 65 yayın; 26 dönem; 78 reklam günü; 390 EUR; ölçüm kimlikleri ve kaynaklar korundu; gerçekleşen yayın/harcama alanları boş. Tam depo kaynak denetimi yeniden çalıştırılmadı.\n',encoding='utf-8')
print('PASS: relative schedule, counts, budgets, measurements and unlaunched status')

# Kullanıcının sonraki talimatı: organik başlangıç; reklam tarihi veri sonrası seçilir.
plan['superseded_ad_schedule'] = {'status':'historical_not_active','planned_media_budget_eur':390,'flight_count':26}
plan['flights'] = []
plan['planned_media_budget_eur'] = 0
plan['media_budget_ceiling_eur'] = 390
plan['advertising_activation'] = {'status':'waiting_for_organic_publications_and_review','start_day':None,'rule':'Önce organik yayınlar ve gerçek performans gözlemi; sonra uygun kreatif/hedef/bölge/varış kararıyla reklam. Algoritmanın oturması için evrensel gün sayısı varsayılmaz.'}
for d in plan['days']:
    d['ad_flight']=None
    d['planned_media_average_eur']=0
for w in plan['weeks']:
    w['paid']='Reklam takvimi atanmadı; organik içerik ve ilk ölçümler sonrası değerlendirme.'
(OUT/'plan-gun-1-90.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
body=(OUT/'takvim-gun-1-90.md').read_text(encoding='utf-8')
body=body.split('## Reklam dönemleri')[0]
body=re.sub(r'Reklam: 26 dönem.*?aktarılmaz\.', 'Reklam ilk günden başlamaz. Önce organik yayınlar ve ilk ölçümler değerlendirilir. Önceki 390 € bütçe üst sınır olarak tutulur; aktif atanmış reklam bütçesi 0 €.',body)
body=re.sub(r'\*\*Reklam:\*\*.*?harcama yapılmaz\.', '**Reklam:** Başlangıç günü atanmadı. Organik içerikler yayımlandıktan ve sonuçlar incelendikten sonra kurulum kararı verilir. 30 €/hafta önceki bütçe çerçevesidir; atlanan haftaların harcaması telafi edilmez.',body)
body=re.sub(r'\*\*Reklam kararı:\*\*[^\n]*','**Reklam kararı:** Organik yayın ve veri değerlendirmesi sonrası; otomatik başlangıç yok.',body)
body=re.sub(r'W\d{2}-[AB] · ort\. 5 €; dönem 15 €', 'Reklam atanmadı',body)
(OUT/'takvim-gun-1-90.md').write_text(body,encoding='utf-8')
assert not plan['flights'] and all(d['ad_flight'] is None and d['planned_media_average_eur']==0 for d in plan['days'])
(OUT/'dogrulama.txt').write_text('PASS: 90 sıralı gün; 65 yayın; ölçüm kimlikleri korundu. Güncel reklam planı: 0 atanmış dönem, 0 EUR atanmış harcama; 390 EUR önceki bütçe üst sınırı. Organik başlangıç sonrası değerlendirme bekleniyor.\n',encoding='utf-8')
print('PASS: organic-first override; no scheduled ad launch or spend')
