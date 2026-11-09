# articulo attack on mandarin · details

21 s · 1080 × 1920 · 30 fps · H.264 · no audio stream · no on-screen text. No publishing date assigned.

Catalog: `decentralize-dfw/yigit/v3/content/works.json`, blob `3c643323bffb2153bef1adedc4ac80977e24aa09`. Both description and artist note were read before selecting the composition route.

## Points of interest

Coordinates are normalized inside the named EXIF-oriented source, not the Reel frame. Each point names the depicted region that motivates its shot.

| Point | Source | (cx, cy) | Visible interest and selection reason |
| --- | --- | --- | --- |
| 1 | A0135 | (0.515, 0.500) | Upper blue bird: streaked wing to long beak |
| 2 | A0136 | (0.495, 0.500) | Next group: connected blue-white birds across the flock |
| 3 | A0140 | (0.550, 0.495) | Thin figure from face down through the hands on the pole |
| 4 | A0139 | (0.500, 0.500) | Boat: stacked round figures with X eyes |
| 5 | A0194 rectified | (0.510, 0.688) | Boat side toward the painted STUGOTZ letters |
| 6 | A0194 rectified | (0.240, 0.695) | Lower-left bird and chain down to the two anchors |

## Shot route

| Shot | Duration | Start (cx, cy) | End (cx, cy) | Axis | Visible connection |
| --- | --- | --- | --- | --- | --- |
| 1 | 2.5 s | (0.320, 0.500) | (0.710, 0.500) | x | Upper blue bird: streaked wing to long beak |
| 2 | 2.5 s | (0.700, 0.500) | (0.290, 0.500) | x | Next group: connected blue-white birds across the flock |
| 3 | 2.5 s | (0.550, 0.270) | (0.550, 0.720) | y | Thin figure from face down through the hands on the pole |
| 4 | 2.5 s | (0.260, 0.500) | (0.740, 0.500) | x | Boat: stacked round figures with X eyes |
| 5 | 2.5 s | (0.680, 0.688) | (0.340, 0.688) | x | Boat side toward the painted STUGOTZ letters |
| 6 | 2.5 s | (0.240, 0.620) | (0.240, 0.770) | y | Lower-left bird and chain down to the two anchors |

Intermediate shots keep a constant scale and move on a single axis until the cut. All cuts lie on the 0.5-second grid. The last shot alone zooms: fixed centre, close view → complete painting fitting on white, 6 seconds total, specified 2-second hold.

## Excluded files and eligibility

IMG_6639 copy is a horizontally cropped camera detail and cannot serve as the full painting. A0191 explicitly names image_gpt; painting.png and 12000-square Yeni Proje.png have uncertain enlarged/synthetic presentation provenance, so all are excluded. A0192 is only 1890 square: the required final cover 1.3 would exceed 1.25x upscale. Instead the original real full photo A0194 is perspective-rectified from its four canvas corners to 3500 square; no colour/contrast edits. PROCES-SFRAMED 0/0-0/aaa/aaaaaa are sketches or drawing exports, not painted stages. Use five genuine painted states 1–5.

## Sources

- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_2_mandarin articulo odisey\detay\arcitul0_detail_1.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_2_mandarin articulo odisey\detay\arcitul0_detail_2.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_2_mandarin articulo odisey\detay\arcitul0_detail_6.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_2_mandarin articulo odisey\detay\arcitul0_detail_5.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\INSTAGRAM\_sources\mandarin-full-photo-rectified.png`

Full-image derivative: original A0194 4284 × 5712; four physical canvas corners only, rectified to 3500 × 3500. No colour, contrast, synthetic reconstruction or artwork extension. Original source is unchanged. Reproducible corner data and original SHA-256 are saved locally in `INSTAGRAM/_sources/mandarin-source.json`. The 1890-square ready-framed painted stages keep their native pixels.

## Music mood suggestions

- Sparse instrumental jazz, dry percussion.
- Minimal electronic pulse around 120 BPM, no vocals.
- Restrained ambient texture.

Music is selected and added by Yiğit in Instagram; no audio has been embedded.

## Validation

```json
{
  "slug": "articulo-attack-on-mandarin",
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
