import json,re,collections
from pathlib import Path
from urllib.parse import unquote,urlparse
ROOT=Path(__file__).resolve().parent.parent
p=ROOT/'instagram-review/publication-plan-180'
plan=json.loads((p/'plan-180.json').read_text(encoding='utf8'));posts=plan['posts'];errors=[]
inventory={a['id']:a for a in json.loads((ROOT/'archive-audit/audit-files.json').read_text(encoding='utf8'))}
assert len(plan['days'])==180 and len(posts)==78
first=[x for x in posts if x['day']<=14]
assert [x['day'] for x in first]==[1,3,5,8,10,12]
assert len({x['work_key'] for x in first})==6
assert [x['day'] for x in first if x['work_key']=='painstaking']==[3]
seen={};min_gap=999
for r in posts:
 k=r['work_key']
 if k in seen:
  gap=r['day']-seen[k];min_gap=min(min_gap,gap)
  if gap<14:errors.append(('repeat gap',k,seen[k],r['day']))
 seen[k]=r['day']
 for a in r['assets']:
  if not Path(a['path']).exists():errors.append(('missing source',a['id']))
 assert len(r['caption_en'])<=2200
 if r.get('shots'):
  assert r['shots'][0]['out_start']==0 and r['shots'][-1]['out_end']==r['duration_seconds']
  for a,b in zip(r['shots'],r['shots'][1:]):assert a['out_end']==b['out_start']
  for s in r['shots']:
   if s['source_in'] is not None:
    assert s['source_out']<=inventory[s['asset_id']]['duration']
    assert abs((s['source_out']-s['source_in'])/s['speed']-(s['out_end']-s['out_start']))<.01
for w in plan['weeks']:
 assert len(set(w['work_keys']))==3
 assert w['archive_feed_count'] in [1,2]
for f in ['PLAN-180.html','ILK-14-GUN.html']:
 txt=(p/f).read_text(encoding='utf8')
 for ref in set(re.findall(r'(?:href|src)="([^"]+)"',txt)):
  if ref.startswith(('https:','http:','#')):continue
  q=Path(unquote(urlparse(ref).path).lstrip('/')) if ref.startswith('file:') else p/unquote(ref.split('#')[0])
  if not q.exists():errors.append(('missing target',f,ref))
 assert '<b>129</b>' not in txt and 'Three faces. One arrangement.' not in txt
counts=collections.Counter(x['caption_en'] for x in posts)
assert not [n for n,c in counts.items() if c>1]
assert not errors,errors
validation={'valid':True,'version':2,'days':180,'posts':78,'formats':dict(collections.Counter(p['format'] for p in posts)),'first_two_week_days':[x['day'] for x in first],'first_two_week_unique_works':6,'painstaking_first_two_week_days':[3],'all_weeks_three_distinct_works':True,'weekly_archive_posts_min':min(w['archive_feed_count'] for w in plan['weeks']),'weekly_archive_posts_max':max(w['archive_feed_count'] for w in plan['weeks']),'minimum_same_work_gap_days':min_gap,'no_missing_source_or_html_target':True,'unique_caption_count':len(counts),'contiguous_detailed_timelines':True,'source_cut_times_within_file_duration':True,'media_rendered':False,'new_english_narration_required_days':[8,10],'browser_preview':'not_attempted_due_to_prior_file_protocol_policy_block'}
(p/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(validation,ensure_ascii=False))
