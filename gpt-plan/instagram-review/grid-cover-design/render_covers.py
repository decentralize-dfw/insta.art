"""Native page composition; original paintings are never painted over or changed.

The page model is exported to editable, self-contained SVG (outlined type) and
PNG. Images are colour-managed and proportionally sampled for embedding only.
No generative image edits, invented details, or crop-to-fill of artwork.
"""
from pathlib import Path
import json, sys, io, hashlib, math, collections, re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / 'archive-audit/deps'))
import pymupdf as fitz
from PIL import Image, ImageOps, ImageCms
Image.MAX_IMAGE_PIXELS = None

FONT_FILE = str(HERE/'fonts/HankenGrotesk-400.ttf')
BOLD_FILE = str(HERE/'fonts/HankenGrotesk-500.ttf')
FONT = fitz.Font(fontfile=FONT_FILE)
BOLD = fitz.Font(fontfile=BOLD_FILE)
PAPER = (1, 1, 1)
INK = (0, 0, 0)
MUTED = (0, 0, 0)
STYLE_ID = 'website-hanken-400-500-white-black-v2'
load = lambda p: json.loads(p.read_text(encoding='utf-8'))
save = lambda p, x: p.write_text(json.dumps(x, ensure_ascii=False, indent=2), encoding='utf-8')
ASSETS = {x['id']:x for x in load(ROOT/'archive-audit/audit-files.json')}
PLAN = load(ROOT/'instagram-review/publication-plan-180-posts/PLAN-180-POST.json')
POSTS = {p['n']:p for p in PLAN['posts']}
BRIEF = load(HERE/'design-brief.json')
for folder in ['exports', 'tiles', 'crops', 'sources', 'grids/chronological', 'grids/pinned', 'review/cover-sheets', 'review/grid-sheets']:
    (HERE/folder).mkdir(parents=True, exist_ok=True)

PROVENANCE = {}
def source(asset_id):
    if asset_id in PROVENANCE:
        return PROVENANCE[asset_id]
    a = ASSETS[asset_id]
    assert a['kind']=='image', (asset_id, 'not a still image')
    original = Path(a['path'])
    with original.open('rb') as stream:
        current_sha256 = hashlib.file_digest(stream, 'sha256').hexdigest()
    if a.get('sha256') and current_sha256 != a['sha256']:
        raise RuntimeError(f'{asset_id}: source differs from audited bytes; re-inspect before design')
    with Image.open(original) as im:
        orig_size = im.size
        orientation = im.getexif().get(274, 1)
        profile = im.info.get('icc_profile')
        im = ImageOps.exif_transpose(im)
        oriented_size = im.size
        alpha = im.getchannel('A') if 'A' in im.getbands() else None
        colour_action = 'untagged; sRGB assumed for local web design'
        if profile:
            try:
                incoming = ImageCms.ImageCmsProfile(io.BytesIO(profile))
                description = ImageCms.getProfileDescription(incoming).strip()
                im = ImageCms.profileToProfile(im.convert('RGB'), incoming, ImageCms.createProfile('sRGB'), outputMode='RGB')
                colour_action = 'ICC appearance converted to sRGB: ' + description
            except Exception as exc:
                raise RuntimeError(f'{asset_id}: ICC conversion failed; do not silently discard profile') from exc
        else:
            im = im.convert('RGB')
        if alpha is not None:
            im.putalpha(alpha)
        im.thumbnail((2160, 2160), Image.Resampling.LANCZOS)
        target = HERE/'sources'/f'{asset_id}.webp'
        im.save(target, compress_level=4, icc_profile=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes())
        embedded_size = im.size
    PROVENANCE[asset_id] = {
        'id':asset_id, 'original_path':str(original),
        'original_sha256':a.get('sha256'), 'current_sha256':current_sha256,
        'matches_audited_bytes':current_sha256==a.get('sha256'), 'original_size':orig_size,
        'oriented_size':oriented_size, 'exif_orientation':orientation,
        'embedded_size':embedded_size, 'embedded_path':str(target),
        'colour_action':colour_action, 'source_modified':False,
        'source_role':'an existing archive image, including already selected details where chosen',
    }
    return PROVENANCE[asset_id]

def page_doc(w,h, background=PAPER):
    doc=fitz.open(); page=doc.new_page(width=w,height=h)
    page.insert_font(fontname='Regular',fontfile=FONT_FILE)
    page.insert_font(fontname='Bold',fontfile=BOLD_FILE)
    page.draw_rect(page.rect, color=None, fill=background)
    return doc,page

def put_text(page, x,y,text,size=20,bold=False,color=INK):
    page.insert_text((x,y),text,fontname='Bold' if bold else 'Regular',fontsize=size,color=color)

def fit_rect(width,height,box):
    box=fitz.Rect(box); scale=min(box.width/width,box.height/height)
    w,h=width*scale,height*scale
    return fitz.Rect(box.x0+(box.width-w)/2,box.y0+(box.height-h)/2,box.x0+(box.width+w)/2,box.y0+(box.height+h)/2)

def put_art(page, asset_id,box):
    s=source(asset_id); w,h=s['oriented_size']; r=fit_rect(w,h,box)
    page.insert_image(r, filename=s['embedded_path'], keep_proportion=True)
    return {'asset_id':asset_id, 'rect':[round(x,3) for x in r],
            'source_ratio':w/h, 'rendered_ratio':r.width/r.height,
            'upscale_factor':max(r.width/w,r.height/h), 'crop':'none; complete selected source image'}

def wrap_headline(text,max_width=900):
    words=text.split()
    for size in [104,100,96,92,88,84]:
        candidates=[]
        if BOLD.text_length(text,fontsize=size)<=max_width:
            candidates.append([text])
        for k in range(1,len(words)):
            lines=[' '.join(words[:k]),' '.join(words[k:])]
            widths=[BOLD.text_length(s,fontsize=size) for s in lines]
            if max(widths)<=max_width:
                candidates.append(lines)
        if candidates:
            # One line only if naturally short. Otherwise prefer balanced lines.
            best=min(candidates,key=lambda ls:(0 if len(ls)==1 else 100)+abs(BOLD.text_length(ls[0],fontsize=size)-BOLD.text_length(ls[-1],fontsize=size)))
            return best,size
    raise ValueError(f'Headline cannot fit two readable lines: {text!r}')

def contained(r, frame,epsilon=.1):
    r=fitz.Rect(r);f=fitz.Rect(frame)
    return r.x0>=f.x0-epsilon and r.y0>=f.y0-epsilon and r.x1<=f.x1+epsilon and r.y1<=f.y1+epsilon

def render_cover(c, square_adaptation=False):
    n=c['n']; post=POSTS[n]; pid=f'P{n:03}'
    core_h=1080 if square_adaptation else 1350
    h=1080 if square_adaptation else (1920 if post['format']=='Reel' else 1350)
    dy=(h-core_h)/2
    doc,page=page_doc(1080,h)
    ids=c['hero_ids']; layout=c['layout']; headline=c['headline_en'].strip()
    lines,fs=wrap_headline(headline) if headline else ([],None)
    assert (layout=='gallery') == (not headline), (n, 'gallery must be text-free')
    assert len(ids)==(2 if layout=='pair' else 1), (n,'invalid image count')
    art=[]; text_rects=[]; arrangement='single'
    if layout=='gallery':
        art=[put_art(page,ids[0],(60,dy+65,1020,dy+core_h-65))]
    else:
        line_h=fs*1.13
        title_h=line_h*len(lines)
        gap=54
        art_max_h=core_h-130-title_h-gap
        max_box=fitz.Rect(90,0,990,art_max_h)
        if layout=='question':
            sw,sh=source(ids[0])['oriented_size']
            fitted=fit_rect(sw,sh,max_box)
            art_h=fitted.height
            top=dy+(core_h-art_h-gap-title_h)/2
            art=[put_art(page,ids[0],(90,top,990,top+art_h))]
        else:
            # Maximise the smaller image's display area; equal boxes are NOT physical-scale evidence.
            options={}
            for orient in ['side_by_side','stacked']:
                if orient=='side_by_side':boxes=[(90,0,526,art_max_h),(554,0,990,art_max_h)]
                else:boxes=[(90,0,990,(art_max_h-28)/2),(90,(art_max_h+28)/2,990,art_max_h)]
                fit=[fit_rect(*source(i)['oriented_size'],b) for i,b in zip(ids,boxes)]
                options[orient]=(min(r.get_area() for r in fit),boxes,fit)
            arrangement=max(options,key=lambda k:options[k][0])
            _,boxes,fit=options[arrangement]
            used_y0=min(r.y0 for r in fit);used_y1=max(r.y1 for r in fit)
            art_h=used_y1-used_y0
            top=dy+(core_h-art_h-gap-title_h)/2
            for i,r in zip(ids,fit):
                r=fitz.Rect(r.x0,r.y0-used_y0+top,r.x1,r.y1-used_y0+top)
                art.append(put_art(page,i,r))
        first_baseline=top+art_h+gap+fs*.88
        for j,line in enumerate(lines):
            y=first_baseline+j*line_h
            put_text(page,90,y,line,fs,True)
            # Use actual font metrics, including ascenders/descenders for clipping checks.
            text_rects.append([90,y-BOLD.ascender*fs,90+BOLD.text_length(line,fontsize=fs),y-BOLD.descender*fs])
    if square_adaptation:
        assert all(contained(r,page.rect) for r in [x['rect'] for x in art]+text_rects)
        page.get_pixmap(alpha=False).save(HERE/'crops'/f'{pid}-square-adapted.webp')
        result={'path':f'crops/{pid}-square-adapted.webp','width':1080,'height':1080,
                'content_contained':True,'font_size':fs,'art_rects':art,
                'role':'Separate square composition; not the default feed or observed 3:4 grid.'}
        doc.close()
        return result
    crop_grid=fitz.Rect(0,(h-1440)/2,1080,(h+1440)/2) if h==1920 else fitz.Rect(33.75,0,1046.25,1350)
    crop_feed=fitz.Rect(0,dy,1080,dy+1350)
    crop_square=fitz.Rect(0,(h-1080)/2,1080,(h+1080)/2)
    content_rects=[x['rect'] for x in art]+text_rects
    grid_ok=all(contained(r,crop_grid) for r in content_rects)
    feed_ok=all(contained(r,crop_feed) for r in content_rects)
    square_ok=all(contained(r,crop_square) for r in content_rects)
    assert grid_ok and feed_ok, (pid,'content clipped in required project preview')
    page.get_pixmap(alpha=False).save(HERE/'exports'/f'{pid}.webp')
    (HERE/'exports'/f'{pid}.svg').write_text(page.get_svg_image(text_as_path=True),encoding='utf-8')
    page.get_pixmap(matrix=fitz.Matrix(270/crop_grid.width,360/crop_grid.height),clip=crop_grid,alpha=False).save(HERE/'tiles'/f'{pid}.webp')
    page.get_pixmap(matrix=fitz.Matrix(.4,.4),clip=crop_square,alpha=False).save(HERE/'crops'/f'{pid}-square.webp')
    if h==1920:
        page.get_pixmap(matrix=fitz.Matrix(.4,.4),clip=crop_feed,alpha=False).save(HERE/'crops'/f'{pid}-feed.webp')
    c['render']={'style_id':STYLE_ID,'width':1080,'height':h,'font_size':fs,'lines':lines,'arrangement':arrangement,
        'art_rects':art,'text_rects':text_rects,'grid_crop_rect':list(crop_grid),'grid_crop_ok':grid_ok,
        'reel_feed_crop_ok':feed_ok,'square_stress_crop_ok':square_ok,
        'title_size_at_120px_tile':round(fs*120/crop_grid.width,1) if fs else None,
        'platform_preview_checked':False,'cover_png':f'exports/{pid}.webp','cover_svg':f'exports/{pid}.svg',
        'profile_tile':f'tiles/{pid}.webp','square_stress_preview':f'crops/{pid}-square.webp',
        'source_upscaled':any(x['upscale_factor']>1.001 for x in art),
        'status':'local_cover_rendered_not_uploaded'}
    doc.close()
    return c

def raster_image(page,path,box):
    page.insert_image(fitz.Rect(box),filename=str(path),keep_proportion=True)

def make_baseline_tiles():
    for x in BRIEF['baseline']['items']:
        # Public-profile preview only. This centre crop models the measured box,
        # not a claim to know the account owner's crop offset.
        path=HERE/x['path']
        with Image.open(path) as im:
            w,h=im.size
        d,p=page_doc(w,h);p.insert_image(p.rect,filename=str(path))
        target_ratio=.75
        if w/h>target_ratio:
            cw=h*target_ratio;crop=fitz.Rect((w-cw)/2,0,(w+cw)/2,h)
        else:
            ch=w/target_ratio;crop=fitz.Rect(0,(h-ch)/2,w,(h+ch)/2)
        p.get_pixmap(matrix=fitz.Matrix(270/crop.width,360/crop.height),clip=crop).save(HERE/'tiles'/f'{x["id"]}.png')
        d.close()

def pins_for(n):
    return [p for p in ([1,3,5] if n<30 else [1,5,30]) if p<=n]

def state_items(n,mode):
    pinned=pins_for(n) if mode=='pinned' else []
    ids=[f'P{p:03}' for p in pinned]+[f'P{p:03}' for p in range(n,0,-1) if p not in pinned]+['B01','B02','B03']
    ids=ids[:12]
    ids+=['unknown']*(12-len(ids))
    assert len(ids)==12
    assert len([x for x in ids if x!='unknown'])==len(set(x for x in ids if x!='unknown'))
    return ids, [f'P{p:03}' for p in pinned]

def render_grid(n,mode):
    ids,pins=state_items(n,mode)
    d,p=page_doc(630,1158,(1,1,1))
    day=POSTS[n]['day'] if n else 0
    put_text(p,21,30,f'{"S"+str(n).zfill(3)}  /  Gün {day}',22,True)
    put_text(p,21,53,'Önerilen sabitler' if mode=='pinned' else 'Yeni yayınlar • kronolojik',14)
    put_text(p,21,74,'Yerel 3:4 model • hesapta uygulanmadı',12,color=MUTED)
    for j,i in enumerate(ids):
        x=21+(j%3)*198;y=94+(j//3)*260
        box=fitz.Rect(x,y,x+192,y+256)
        if i=='unknown':
            p.draw_rect(box,color=INK,fill=PAPER,width=.5)
            put_text(p,x+30,y+125,'Görülmeyen alan',14,color=MUTED)
        else:
            raster_image(p,HERE/'tiles'/f'{i}.webp',box)
            # Review labels outside the art; not part of the exported cover.
            label=i+(' · sabit' if i in pins else '')
            tw=FONT.text_length(label,fontsize=11)+12
            p.draw_rect(fitz.Rect(x+3,y+3,x+tw,y+21),color=None,fill=(1,1,1),fill_opacity=.93)
            put_text(p,x+8,y+16,label,11)
            if i.startswith('P') and POSTS[int(i[1:])]['format']!='Single':
                fmt=POSTS[int(i[1:])]['format']
                token='R' if fmt=='Reel' else 'C'
                p.draw_rect(fitz.Rect(x+170,y+4,x+188,y+23),color=None,fill=(1,1,1),fill_opacity=.93)
                put_text(p,x+175,y+18,token,11,True)
    out=HERE/'grids'/mode/f'S{n:03}.webp'
    p.get_pixmap().pil_save(out,format='JPEG',quality=91)
    d.close()
    return {'after_post':n,'day':day,'mode':mode,'ordered_top12':ids,'desired_pins_left_to_right':pins,
        'path':f'grids/{mode}/S{n:03}.webp','assumption':'newest first; proposed pins in explicit desired order, not current account pin state'}

def contact_sheets(covers):
    # Every full cover is reviewed at tile size; full resolution remains linked.
    for start in range(0,len(covers),12):
        group=covers[start:start+12]
        d,p=page_doc(1240,1420,(1,1,1))
        put_text(p,28,38,f'Kapak incelemesi · P{group[0]["n"]:03}–P{group[-1]["n"]:03}',25,True)
        for j,c in enumerate(group):
            x=28+(j%4)*302;y=64+(j//4)*446
            raster_image(p,HERE/'tiles'/f'P{c["n"]:03}.png',(x,y,x+280,y+373.333))
            put_text(p,x,y+397,f'P{c["n"]:03} · {POSTS[c["n"]]["format"]} · {c["layout"]}',17,True)
            put_text(p,x,y+420,' / '.join(c['hero_ids']),15,color=MUTED)
        p.get_pixmap().pil_save(HERE/'review/cover-sheets'/f'C{start/12+1:02}.webp',format='JPEG',quality=94)
        d.close()
    for mode in ['chronological','pinned']:
        for start in range(1,181,20):
            d,p=page_doc(1120,1820,(1,1,1))
            put_text(p,20,34,f'{mode} · S{start:03}–S{min(start+19,180):03}',24,True)
            for j,n in enumerate(range(start,min(start+20,181))):
                x=18+(j%5)*220;y=54+(j//5)*438
                raster_image(p,HERE/'grids'/mode/f'S{n:03}.webp',(x,y,x+208,y+382.324))
                put_text(p,x,y+405,f'S{n:03}',16,True)
            p.get_pixmap().pil_save(HERE/'review/grid-sheets'/f'{mode}-{(start-1)/20+1:02}.webp',format='JPEG',quality=91)
            d.close()

def main():
    args=sys.argv[1:]
    if '--prototype' in args:
        covers=[]
        for c in BRIEF['first6_locked']:
            c=dict(c); c.update({'why_visual_tr':'İlk 14 günün kilitli kaynak seçimi','grid_role_tr':'İlk altı','must_preserve_tr':'Bütün kaynak','first_frame_tr':'Ayrı kurgu','render_risk_tr':'Mobil önizleme henüz yok'})
            covers.append(render_cover(c))
        save(HERE/'prototype-first6.json',covers)
        make_baseline_tiles()
        for n in range(7):
            for mode in ['chronological','pinned']:render_grid(n,mode)
        contact_sheets(covers) if '--all-states' in args else None
        print('Prototype first six rendered',flush=True)
        return
    covers=load(HERE/'covers-001-090.json')+load(HERE/'covers-091-180.json')
    covers.sort(key=lambda c:c['n'])
    assert [c['n'] for c in covers]==list(range(1,181))
    prior={}
    if (HERE/'covers.json').exists():
        prior={c['n']:c for c in load(HERE/'covers.json')['covers']}
        PROVENANCE.update({s['id']:s for s in load(HERE/'source-provenance.json')})
    elif (HERE/'rendered-first90.json').exists():
        prior={c['n']:c for c in load(HERE/'rendered-first90.json')}
        PROVENANCE.update({s['id']:s for s in load(HERE/'source-provenance-first90.json')})
    for c in covers:
        old=prior.get(c['n'])
        if old and old.get('render',{}).get('style_id')==STYLE_ID and all(old.get(k)==v for k,v in c.items()) and (HERE/'exports'/f'P{c["n"]:03}.png').exists():
            c['render']=old['render']
        else:render_cover(c)
        adapted=c['render'].get('square_adaptation')
        if not adapted or not (HERE/adapted['path']).exists():
            c['render']['square_adaptation']=render_cover(c,square_adaptation=True)
        if c['n']%20==0:print(f'Rendered {c["n"]}/180 covers',flush=True)
    make_baseline_tiles()
    states=[]
    for mode in ['chronological','pinned']:
        for n in range(181):states.append(render_grid(n,mode))
        print(f'Rendered181 {mode} grid states',flush=True)
    contact_sheets(covers)
    signatures=collections.defaultdict(list)
    for c in covers:signatures[(c['layout'],tuple(c['hero_ids']),c['headline_en'])].append(c['n'])
    duplicates=[v for v in signatures.values() if len(v)>1]
    close_duplicates=[(a,b) for group in duplicates for a,b in zip(group,group[1:]) if b-a<12]
    meta={'version':2,'style_id':STYLE_ID,'created':'2026-11-04','covers':180,'grid_states':360,'baseline_states':2,
        'style_basis':'User explicitly restricted applied design to white background and black text. Hanken Grotesk 400/500 read from yigitozen.art and /paintings/ computed styles and its own font files.',
        'content_plan':'../publication-plan-180-posts/PLAN-180-POST.json','current_sequence_is_editorial_draft':True,
        'source_images_unchanged':True,'artwork_fit':'contain, no new crops of original art',
        'public_text_language':'English','render_method':'native vector composition; SVG with outlined type; PNG raster export of same page',
        'profile_grid_ratio_evidence':BRIEF['canvas']['profile_ratio_evidence'],
        'baseline':BRIEF['baseline'],'pin_order':'desired left-to-right; actual account state not established',
        'platform_preview_checked':False,'published':False,
        'production_scope':'180 covers only. Carousel interior slides, new captures, voice and finished videos remain separate deliverables.',
        'sequence_limitation':'Kapak tasarımı içerik sırasının büyüme başarısını doğrulamaz. Ana plandaki 90 günlük hedef ve geç keşif/format yoğunluğu ayrıca değerlendirilmelidir.'}
    save(HERE/'covers.json',{'meta':meta,'covers':covers})
    save(HERE/'source-provenance.json',list(PROVENANCE.values()))
    save(HERE/'grid-states.json',states)
    report={'post_count':len(covers),'grid_states':len(states),'all_sources_are_archive_images':True,
        'all_expected_grid_crops_keep_content':all(c['render']['grid_crop_ok'] for c in covers),
        'all_reel_feed_crops_keep_content':all(c['render']['reel_feed_crop_ok'] for c in covers),
        'aspect_ratio_errors':[(c['n'],a['asset_id']) for c in covers for a in c['render']['art_rects'] if abs(a['source_ratio']-a['rendered_ratio'])>.0001],
        'minimum_headline_size_at_120px_tile':min(c['render']['title_size_at_120px_tile'] for c in covers if c['render']['font_size']),
        'source_upscales':[c['n'] for c in covers if c['render']['source_upscaled']],
        'exact_cover_duplicates':duplicates,'close_duplicate_covers':close_duplicates,
        'square_stress_crop_content_losses':[c['n'] for c in covers if not c['render']['square_stress_crop_ok']],
        'square_note':'Alternative square centre-crop is a stress test, not the observed account grid. Loss means use a dedicated square adaptation if that surface is chosen.',
        'all_pin_states_have_no_duplicates':True,'source_hashes_from_audit':'current SHA-256 of every used original compared to audit records before rendering',
        'all_sources_match_audited_bytes':all(x['matches_audited_bytes'] for x in PROVENANCE.values()),
        'visual_review':'pending contact sheet review','platform_preview_checked':False,'published':False}
    save(HERE/'VALIDATION.json',report)
    print(json.dumps({'covers':180,'states':len(states),'close_duplicate_covers':close_duplicates,'upscales':report['source_upscales']},ensure_ascii=False),flush=True)

if __name__=='__main__':main()
