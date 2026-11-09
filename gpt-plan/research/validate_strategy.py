#!/usr/bin/env python3
"""Validate the authored phase-4 plan against its source snapshot. No network."""
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
OUT = ROOT / '04-strategy'
plan = json.loads((OUT / 'strategy-plan-data-20261016.json').read_text())
coverage = json.loads((OUT / 'strategy-evidence-transfer-20261016.json').read_text())
checks = []

def check(condition, message):
    if not condition:
        raise SystemExit('FAIL: ' + message)
    checks.append(message)

start = date.fromisoformat(plan['start'])
end = date.fromisoformat(plan['end_inclusive'])
days = plan['days']
check(len(days) == (end-start).days+1 == 90, '90 consecutive inclusive calendar days')
check([d['date'] for d in days] == [(start+timedelta(days=i)).isoformat() for i in range(90)], 'Every date appears once, in order')
check([d['day'] for d in days] == list(range(1,91)), 'All day IDs 1 through 90')
check(all(d['week'] == (d['day']-1)//7+1 for d in days), 'All week assignments match the dates')
check(start.weekday() == 0 and end.weekday() == 5, 'Start Monday / final Saturday')
weekday_names = ['Pazartesi','Salı','Çarşamba','Perşembe','Cuma','Cumartesi','Pazar']
check(all(d['weekday']==weekday_names[date.fromisoformat(d['date']).weekday()] for d in days), 'All Turkish weekday names match actual dates')
formats = Counter(d['format'] for d in days)
check(formats == {'Reel R1':13, 'Reel R2':13, 'Reel R3':13, 'Carousel C1':13, 'Tek görsel P1':13, 'Üretim / veri':13, 'Değerlendirme':12}, '39 Reels + 13 carousels + 13 photos, production and review days')
check(sum(d['is_feed_post'] for d in days)==plan['total_feed_posts']==65, '65 planned feed posts')
zone = ZoneInfo(plan['timezone'])
flights = plan['flights']
check(len(flights)==26, '26 planned flights')
ad_dates=[]
for f in flights:
    a=datetime.fromisoformat(f['start_local']).replace(tzinfo=zone)
    b=datetime.fromisoformat(f['end_exclusive_local']).replace(tzinfo=zone)
    check((b.timestamp()-a.timestamp())==72*3600, f"{f['id']} lasts exactly 72 hours with DST accounted for")
    check(f['planned_lifetime_limit_eur']==15 and f['planned_daily_average_eur']==5, f"{f['id']} 15 EUR total / 5 EUR planned daily average")
    expected=[(a.date()+timedelta(days=i)).isoformat() for i in range(3)]
    check(f['calendar_ad_days']==expected, f"{f['id']} actual calendar dates match flight boundaries")
    ad_dates.extend(expected)
check(len(ad_dates)==len(set(ad_dates))==78, '78 nonoverlapping advertising days')
check(all(start<=date.fromisoformat(d)<=end for d in ad_dates), 'All advertising days fall inside the 90-day horizon')
check(sum(f['planned_lifetime_limit_eur'] for f in flights)==plan['planned_media_budget_eur']==390, '390 EUR planned total')
check(sum(d['planned_media_average_eur'] for d in days)==390, 'Daily allocation agrees with flight budget')
check(all(d['ad_flight']==next((f['id'] for f in flights if d['date'] in f['calendar_ad_days']),None) for d in days), 'Each day points to the correct advertising flight')
check(all(d['status']=='planned_not_published' and d['actual_published_at'] is None for d in days), 'No planned publication is labeled as completed')
check(all(f['actual_spend_eur'] is None and f['status']=='planned_not_launched' for f in flights), 'No ad spend or launch is fabricated')
check(plan['current_followers'] is None and plan['organic_niche_baseline'] is None and plan['actual_spend_eur'] is None, 'Unknown baseline and actual spend remain null')
check(len(plan['weeks'])==13, '13 authored weekly themes and decision questions')
for d in days:
    expected=[]
    for p in days[:d['day']-1]:
        if p['is_feed_post']:
            for h in (24,72,168):
                if date.fromisoformat(p['date'])+timedelta(hours=h)==date.fromisoformat(d['date']):
                    expected.append(f"D{p['day']:02d}/{h}sa")
    check(d['observation_ids']==expected, f"D{d['day']:02d} measurement-age schedule")
    check(all((ROOT/p).is_file() for p in d['sources']), f"D{d['day']:02d} source paths exist")
expected_sources={str(p.relative_to(ROOT)) for folder in ['01-algorithm','02-market','03-tactics'] for p in (ROOT/folder).glob('*.md')}
check(len(expected_sources)==175 and expected_sources=={m['path'] for m in coverage['documents']}, 'All 175 phase-1–3 Markdown files covered')
for m in coverage['documents']+coverage['json_registers']:
    check(hashlib.sha256((ROOT/m['path']).read_bytes()).hexdigest()==m['sha256'], 'Source snapshot hash '+m['path'])
check(len(coverage['atomic_claim_transfers'])==266, 'All 266 existing claim records transferred with original scope')
for source in {c['source_file'] for c in coverage['atomic_claim_transfers']}:
    original=json.loads((ROOT/source).read_text())['claims']
    transferred=[c['original_record'] for c in coverage['atomic_claim_transfers'] if c['source_file']==source]
    check(original==transferred, 'Original claim records preserved '+source)
check({c['question'] for c in coverage['atomic_claim_transfers'] if c['source_file'].startswith('03-')}==set(range(1,61)), '60 tactics questions represented in atomic transfer')
check(coverage['question_counts']=={'algorithm':18,'market':28,'tactics':60}, '18 + 28 + 60 numbered-question coverage')
for p in OUT.glob('*.md'):
    body=p.read_text()
    check(body.splitlines()[1].startswith('16 Ekim 2026.'), 'Written date metadata '+p.name)
    for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)',body):
        if not re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:',target) and not target.startswith('#'):
            check((p.parent/target.split('#')[0]).resolve().is_file(), 'Internal link '+target)
    for table in re.findall(r'(?m)^\|.*(?:\n\|.*)*',body):
        widths=[len(line.split('|')) for line in table.splitlines()]
        check(len(set(widths))==1, 'Table column consistency '+p.name)
check(len(list(OUT.glob('*.md')))==11, '11 strategy reader documents')
print(f'PASS: {len(checks)} calendar, budget, evidence, date, status and internal-link checks.')
