#!/usr/bin/env python3
"""Rebuild the public reader from the current Markdown tree. No network or secrets."""
import argparse
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
QUESTIONS = [
    ('Takip ve etkileşim', ['algorithm-q1-follow-like']),
    ('Eski hesap ve kitle', ['algorithm-q2-old-audience']),
    ('Günler ve saatler', ['algorithm-q3-posting-times']),
    ('Hook', ['algorithm-q4-general-deep', 'alg-q4-hook-completion', 'algorithm-q4-hooks']),
    ('CTA', ['alg-q5-cta']),
    ('Viral dağıtım', ['alg-q6-viral']),
    ('Performans teşhisi', ['alg-q7-diagnosis']),
    ('Formatlar', ['alg-q8-formats']),
    ('Reklam sistemi', ['alg-q9-ads-system']),
    ('Kitle ve coğrafya', ['alg-q10-audience']),
    ('Reklam rotasyonu', ['alg-q11-rotation']),
    ('Stories', ['alg-q12-stories']),
    ('Birleşik sistem modeli', ['system-model-20261014']),
    ('Yüzeyler ve tahminler', ['system-surfaces-20261014']),
    ('İçerik anlama ve aday bulma', ['system-content-retrieval-20261014']),
    ('Dağıtım ve geri bildirim', ['system-distribution-20261014']),
    ('2025–2026 değişiklikleri', ['system-changes-20261014']),
    ('Güncel reklam mimarisi', ['system-ads-20261014']),
]


def document_date(body):
    """Use the document's visible date; never silently redates older evidence."""
    months = {'Ocak': 1, 'Şubat': 2, 'Mart': 3, 'Nisan': 4, 'Mayıs': 5, 'Haziran': 6,
              'Temmuz': 7, 'Ağustos': 8, 'Eylül': 9, 'Ekim': 10, 'Kasım': 11, 'Aralık': 12}
    first_lines = body.splitlines()[:6]
    # Dated metadata wins over future exhibition or planned publication dates.
    metadata = [line for line in first_lines if re.match(r'^(?:Son kontrol:\s*)?\d{1,2} (?:' + '|'.join(months) + r') 20\d{2}\b', line)]
    header = '\n'.join(metadata or first_lines)
    found = []
    for day, month, year in re.findall(r'(\d{1,2}) (' + '|'.join(months) + r') (20\d{2})', header):
        found.append(date(int(year), months[month], int(day)).isoformat())
    for value in re.findall(r'\b20\d{2}-\d{2}-\d{2}\b', header):
        found.append(date.fromisoformat(value).isoformat())
    if not found:
        raise ValueError('Document must have a visible date in its first six lines')
    return max(found)


def build():
    documents = []
    for phase, folder in [(1, '01-algorithm'), (2, '02-market'), (3, '03-tactics'), (4, '04-strategy')]:
        for path in sorted((ROOT / folder).glob('*.md')):
            body = path.read_text(encoding='utf-8')
            title = next((line[2:] for line in body.splitlines() if line.startswith('# ')), path.stem)
            documents.append(dict(id=path.stem, title=title, date=document_date('\n'.join(body.splitlines()[:2]) if phase == 4 else body), phase=phase,
                                  path=path.relative_to(ROOT).as_posix(), body=body))
    ids = [d['id'] for d in documents]
    if len(ids) != len(set(ids)):
        raise ValueError('Document IDs must be unique across phases')
    groups = [dict(id='overview', phase=1, title='Çerçeve ve denetim',
                   desc='Birleşik algoritma modeli, yüzeyler, güncel değişiklikler ve kaynak/iddia sicilleri.',
                   docs=['algorithm-open-work-resolution-20261016', 'recheck-20261016', 'system-model-20261014', 'system-evidence-20261014', 'algorithm-research-conclusion-20261014', 'algorithm-remaining-controls-20261014', 'stories-sources-20261014', 'algorithm-close-v1', 'algorithm-questions-20261014', 'algorithm-2026-v1',
                         'audit-claims-20261014', 'audit-sources-20261014',
                         'policy-boundaries-20261014', 'user-review-gate-20261014'])]
    for n, (title, docs) in enumerate(QUESTIONS, 1):
        groups.append(dict(id=f'q{n}', phase=1, n=n, title=title,
                           desc='Kamuya açık sistem araştırması ve kanıtlardan üretilmiş açıklama çerçevesi.', docs=docs))
    market_order = ['README', 'market-gap-closure-20261016', 'market-breakdown-answers-20261016', 'market-career-sample-5x5-20261016', 'market-gallery-dossiers-20261016', 'market-visual-comparison-20261016', 'market-ten-questions-answers-20261016', 'market-critical-audit-20261016', 'market-gallery-breakdown-questions-20261016', 'market-25-synthesis-20261016', 'market-relations-engine-20261016',
                    'market-forum-mechanisms-20261016', 'market-yigit-work-map-20261016',
                    'market-research-plan-20261016', 'network-25-01-project-careers-20261016',
                    'network-25-02-gallery-circulation-20261016', 'network-25-03-institutional-expansion-20261016',
                    'network-25-04-global-gallery-20261016', 'network-25-05-museum-history-20261016',
                    'market-niche-framework-20261016', 'market-document-review-20261016',
                    'market-full-audit-20261016', 'market-working-model-20261016']
    tactics_rooms = [
        dict(id='tactics-room-1', phase=3, roomNumber=1, title='Oda 1 · Genel Instagram taktikleri · 01–20',
             desc='Hesap, dağıtım, dikkat, etkileşim ve büyüme trickleri. Sanat bağlamı yok. 20/20 kaynaklı cevap yazıldı. Deneyler uygulanmadı.',
             docs=['room-01-instagram-tricks-questions-20261016', 'tactics-q01-initial-distribution-20261016', 'tactics-q02-nonfollowers-20261016', 'tactics-q03-hooks-20261016', 'tactics-q04-retention-20261016', 'tactics-q05-loops-20261016', 'tactics-q06-answer-20261016', 'tactics-q07-answer-20261016', 'tactics-q08-answer-20261016', 'tactics-q09-answer-20261016', 'tactics-q10-answer-20261016', 'tactics-q11-answer-20261016', 'tactics-q12-answer-20261016', 'tactics-q13-answer-20261016', 'tactics-q14-answer-20261016', 'tactics-q15-answer-20261016', 'tactics-q16-answer-20261016', 'tactics-q17-answer-20261016', 'tactics-q18-answer-20261016', 'tactics-q19-answer-20261016', 'tactics-q20-answer-20261016']),
        dict(id='tactics-room-2', phase=3, roomNumber=2, title='Oda 2 · Sanat dünyasında Instagram iletişimi · 21–40',
             desc='Sanatçı, galerist, küratör, dealer, advisor/broker ve koleksiyoner tarafları. 20/20 kaynaklı cevap yazıldı. Deneyler uygulanmadı.',
             docs=['room-02-art-instagram-communication-questions-20261016', 'tactics-q21-answer-20261016', 'tactics-q22-answer-20261016', 'tactics-q23-answer-20261016', 'tactics-q24-answer-20261016', 'tactics-q25-answer-20261016', 'tactics-q26-answer-20261016', 'tactics-q27-answer-20261016', 'tactics-q28-answer-20261016', 'tactics-q29-answer-20261016', 'tactics-q30-answer-20261016', 'tactics-q31-answer-20261016', 'tactics-q32-answer-20261016', 'tactics-q33-answer-20261016', 'tactics-q34-answer-20261016', 'tactics-q35-answer-20261016', 'tactics-q36-answer-20261016', 'tactics-q37-answer-20261016', 'tactics-q38-answer-20261016', 'tactics-q39-answer-20261016', 'tactics-q40-answer-20261016']),
        dict(id='tactics-room-3', phase=3, roomNumber=3, title='Oda 3 · Algoritmik içerik taktikleri · 41–60',
             desc='Konu, görüntü, kurgu, ses ve izleme davranışı. Sanat bağlamı yok. 20/20 kaynaklı cevap yazıldı. Deneyler uygulanmadı.',
             docs=['room-03-algorithmic-content-questions-20261016', 'tactics-q41-answer-20261016', 'tactics-q42-answer-20261016', 'tactics-q43-answer-20261016', 'tactics-q44-answer-20261016', 'tactics-q45-answer-20261016', 'tactics-q46-answer-20261016', 'tactics-q47-answer-20261016', 'tactics-q48-answer-20261016', 'tactics-q49-answer-20261016', 'tactics-q50-answer-20261016', 'tactics-q51-answer-20261016', 'tactics-q52-answer-20261016', 'tactics-q53-answer-20261016', 'tactics-q54-answer-20261016', 'tactics-q55-answer-20261016', 'tactics-q56-answer-20261016', 'tactics-q57-answer-20261016', 'tactics-q58-answer-20261016', 'tactics-q59-answer-20261016', 'tactics-q60-answer-20261016']),
    ]
    tactics_ids = {i for g in tactics_rooms for i in g['docs']}
    tactics_order = ['tactics-rooms-index-20261016', 'tactics-operating-decisions-20261016', 'tactics-completion-audit-20261016', 'tactics-evidence-06-60-20261016', 'tactics-evidence-01-05-20261016', 'tactics-2026-v1']
    for phase, gid, title, desc in [
        (2, 'market', 'Piyasa ve niş araştırması', '28 galeri cevabı, üç kurum dosyası, yeni 5×5 kariyer örneklemi ve görsel karşılaştırma. Instagram erişimi kullanıcı talimatıyla kapsam dışında.'),
        (3, 'tactics', 'Üçüncü ayak · 3 oda / 60 soru', 'Üç ayrı alt odada 20’şer soru. 60/60 kaynaklı araştırma cevabı yazıldı; deneyler uygulanmadı. Ortak kaynak ve iddia sicili. Eski onaysız taslak ayrıca korunur.'),
        (4, 'strategy', 'Dördüncü ayak · Uygulama planı', 'Tekrar edilebilir haftalık pattern, 90 günlük takvim, 26 reklam dönemi ve kaynak aktarımı. Plan yazıldı; uygulama başlamadı.')]:
        groups.append(dict(id=gid, phase=phase, title=title, desc=desc,
                           docs=sorted([d['id'] for d in documents if d['phase'] == phase and not (phase == 3 and d['id'] in tactics_ids)],
                                       key=lambda i: ((market_order if phase == 2 else tactics_order).index(i) if i in (market_order if phase == 2 else tactics_order) else 999, i))))
    market_answers = ['market-breakdown-answers-20261016'] + [f'market-breakdown-q{n:02d}-20261016' for n in range(1,29)]
    market_cases = ['market-career-sample-5x5-20261016', 'market-career-evidence-matrix-20261016'] + [d['id'] for d in documents if d['phase']==2 and (d['id'].startswith('network-25-') or re.match(r'market-career-s[13]-',d['id']))]
    for group in groups:
        if group['id']=='market': group['docs']=[i for i in group['docs'] if i not in set(market_answers+market_cases)]
    groups.append(dict(id='market-answers', phase=2, title='Galeri dünyası · 28 cevap', desc='Program, ilişki, ekonomi, kurum ve piyasa: 28 kaynaklı analitik cevap.', docs=market_answers))
    groups.append(dict(id='market-careers', phase=2, title='Kariyer karşılaştırması · 5 × 5', desc='Ölçütleri açık aktif örneklem; dört yeni vaka ve önceki kaynak kartları.', docs=market_cases))
    strategy_order = ['strategy-index-20261016', 'strategy-weekly-pattern-20261016', 'strategy-content-playbook-20261016', 'strategy-calendar-90days-20261016', 'strategy-ad-plan-20261016', 'strategy-measurement-20261016', 'strategy-experiments-20261016', 'strategy-art-world-20261016', 'strategy-conflicts-20261016', 'strategy-evidence-coverage-20261016', 'strategy-validation-20261016']
    for group in groups:
        if group['id'] == 'strategy':
            group['docs'].sort(key=lambda i: (strategy_order.index(i) if i in strategy_order else 999, i))
    groups.extend(tactics_rooms)
    linked = [i for g in groups for i in g['docs']]
    # New algorithm appendices remain visible without silently disappearing from search.
    for d in documents:
        if d['id'] not in linked:
            groups[0]['docs'].append(d['id'])
    missing = {i for g in groups for i in g['docs']} - set(ids)
    if missing:
        raise ValueError(f'Navigation refers to missing documents: {missing}')
    return dict(schema='instagram-research-v1', updatedAt=max(d['date'] for d in documents), activePhase=4,
                phases=[dict(id=1, title='Algoritma analizi', status='system_framework_written'),
                        dict(id=2, title='Piyasa analizi', status='research_answers_28_and_revised_5x5_sample_written'),
                        dict(id=3, title='Taktik araştırması', status='research_answers_60_of_60_written'),
                        dict(id=4, title='Uygulama stratejisi', status='plan_written_not_launched')],
                documents=documents,
                navigation=dict(schema='instagram-atlas-v2', groups=groups),
                workflow=dict(canonical='Markdown files in phase folders',
                              audit='System architecture, surfaces, dynamics, 2025–2026 changes and ads written; legacy questions audited',
                              account_data='not a prerequisite for system research', stories='research_ready',
                              user_phase1_approval=False, phase2_parallel_authorized=True, phase2_direct_instagram_sequence_audit_completed=False, phase2_career_hierarchy_validated=False, phase2_universal_career_hierarchy_asserted=False, phase2_operational_5x5_sample_completed=True, phase2_gallery_answer_count=28, phase2_selected_visual_object_count=25, phase2_direct_instagram_scope='excluded_at_user_request_2026-10-16',
                              phase3_room_count=3, phase3_question_count=60, phase3_answer_count=60, phase3_answered_question_ids=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60], phase3_experiments_run=0, phase3_answers_completed=True, phase4_plan_written=True, phase4_launched=False, phase4_plan_start='2026-10-19', phase4_plan_end_inclusive='2027-01-16', phase4_plan_day_count=90, phase4_planned_feed_posts=65, phase4_planned_ad_flights=26, phase4_planned_media_budget_eur=390, phase4_actual_spend_eur=None, phase4_followers_baseline=None, phase4_organic_niche_followers_target=5000, phase4_outcomes_verified=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if findings.json differs from Markdown')
    args = parser.parse_args()
    content = json.dumps(build(), ensure_ascii=False, indent=2) + '\n'
    target = ROOT / 'findings.json'
    if args.check:
        if target.read_text(encoding='utf-8') != content:
            raise SystemExit('findings.json is stale; run python instagram/sync_findings.py')
        print('Markdown, JSON and navigation are synchronized.')
    else:
        target.write_text(content, encoding='utf-8')
        print(f'Wrote {len(json.loads(content)["documents"])} documents.')
