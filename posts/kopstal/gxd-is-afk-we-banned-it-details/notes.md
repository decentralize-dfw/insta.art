# Gxd is AFK, We banned it · details

21 s · 1080 × 1920 · 30 fps · H.264 · no audio stream · no on-screen text. No publishing date assigned.

Catalog: `decentralize-dfw/yigit/v3/content/works.json`, blob `3c643323bffb2153bef1adedc4ac80977e24aa09`. Both description and artist note were read before selecting the composition route.

## Points of interest

Coordinates are normalized inside the named EXIF-oriented source, not the Reel frame. Each point names the depicted region that motivates its shot.

| Point | Source | (cx, cy) | Visible interest and selection reason |
| --- | --- | --- | --- |
| 1 | A1299 | (0.500, 0.500) | Old figure: open orange hand to white hair and face |
| 2 | A1302 | (0.500, 0.500) | Raised orange hand across to the split face and other raised hand |
| 3 | A1303 | (0.500, 0.500) | Turbaned hand at mouth toward the blue-scarfed face |
| 4 | A1206 | (0.270, 0.706) | Hanging pink arm to red fingertips at the step |
| 5 | A1206 | (0.520, 0.762) | Purple drape across ledge to ochre feet |
| 6 | A1206 | (0.730, 0.641) | Carrier feet up the green robe toward the supported body |

## Shot route

| Shot | Duration | Start (cx, cy) | End (cx, cy) | Axis | Visible connection |
| --- | --- | --- | --- | --- | --- |
| 1 | 2.5 s | (0.280, 0.500) | (0.720, 0.500) | x | Old figure: open orange hand to white hair and face |
| 2 | 2.5 s | (0.280, 0.500) | (0.720, 0.500) | x | Raised orange hand across to the split face and other raised hand |
| 3 | 2.5 s | (0.720, 0.500) | (0.280, 0.500) | x | Turbaned hand at mouth toward the blue-scarfed face |
| 4 | 2.5 s | (0.270, 0.640) | (0.270, 0.773) | y | Hanging pink arm to red fingertips at the step |
| 5 | 2.5 s | (0.340, 0.762) | (0.700, 0.762) | x | Purple drape across ledge to ochre feet |
| 6 | 2.5 s | (0.730, 0.762) | (0.730, 0.520) | y | Carrier feet up the green robe toward the supported body |

Intermediate shots keep a constant scale and move on a single axis until the cut. All cuts lie on the 0.5-second grid. The last shot alone zooms: fixed centre, close view → complete painting fitting on white, 6 seconds total, specified 2-second hold.

Opening revised after visual inspection: three original high-resolution detail photographs replace black-heavy whole-master crops. The route then follows the hanging arm into its contact with the step, the feet and the green carrier.

## Excluded files and eligibility

FULL.png and temiz-sketchü.png are line drawings, not finished art. DETAYSHOW presentation and numbered export copies excluded. SİE JPEG files include the room; the already aligned, uncropped stage PNGs are used instead.

## Sources

- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_8_gxd-is-banned\makine\selected\IMG_6729.JPG`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_8_gxd-is-banned\makine\selected\IMG_6733.JPG`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_8_gxd-is-banned\makine\selected\IMG_6734.JPG`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_8_gxd-is-banned\gxd-is-banned-HIGHres-2.png`

## Music mood suggestions

- Sparse instrumental jazz, dry percussion.
- Minimal electronic pulse around 120 BPM, no vocals.
- Restrained ambient texture.

Music is selected and added by Yiğit in Instagram; no audio has been embedded.

## Validation

```json
{
  "slug": "gxd-is-afk-we-banned-it",
  "type": "details",
  "duration": 21.0,
  "frames": 630,
  "video_only": true,
  "h264_1080x1920_30fps": true,
  "full_decode": true,
  "approved_preserved": false,
  "freeze_starts": [
    18.966667
  ],
  "specified_hold_start": 19.0,
  "detector_flags_before_hold": [
    18.966667
  ],
  "mid_route_freeze_starts": [],
  "final_target_frames": 60
}
```

Renderer fixes: the original unbounded decoded-image cache and eager stage retention were replaced with one-source retention; identical static frames are reused. Encoder uses four threads to bound memory, keeping preset slow and CRF 17. A one-frame-early target interpolation was fixed: new detail renders now hold the final view for exactly 60 frames, not 61. Camera rejection rules are unchanged. Regression checks confirm diagonal motion, off-centre zoom, process motion and cropped process frames still fail, and unchanged frame geometry matches the original pixel-for-pixel. Approved historical videos are not modified by these fixes.

Freeze-detector interpretation: the supplied low-motion threshold can flag the last few easing frames just before the fixed hold. Exact reported times remain above; no intermediate route freeze occurred. New renders reach the fixed target at the specified hold boundary and contain exactly 60 target frames, as verified in the renderer regression check.

Visual review: the actual 15-frame encoded strip was inspected for the selected detail route, final complete-artwork fit and stage-only sequence; crop choices and exclusions are documented above. Original source photographs and Milano folders were not modified.
