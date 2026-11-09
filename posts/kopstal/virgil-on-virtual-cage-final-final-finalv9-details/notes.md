# Virgil on Virtual Cage (final_final-finalV9) · details

21 s · 1080 × 1920 · 30 fps · H.264 · no audio stream · no on-screen text. No publishing date assigned.

Catalog: `decentralize-dfw/yigit/v3/content/works.json`, blob `3c643323bffb2153bef1adedc4ac80977e24aa09`. Both description and artist note were read before selecting the composition route.

## Points of interest

Coordinates are normalized inside the named EXIF-oriented source, not the Reel frame. Each point names the depicted region that motivates its shot.

| Point | Source | (cx, cy) | Visible interest and selection reason |
| --- | --- | --- | --- |
| 1 | A0581 | (0.490, 0.355) | White wig down to the hand resting at the cheek |
| 2 | A0581 | (0.500, 0.238) | Grey ceiling and thin white cage line |
| 3 | A0581 | (0.220, 0.360) | Left upright down to where the drawn line stops |
| 4 | A0581 | (0.305, 0.560) | Small curly figure toward the central drapery |
| 5 | A0581 | (0.735, 0.510) | Central arm toward the blonde inward-facing figure and wing |
| 6 | A0581 | (0.650, 0.731) | Reclining grey-haired figure and raised legs into coral paint |

## Shot route

| Shot | Duration | Start (cx, cy) | End (cx, cy) | Axis | Visible connection |
| --- | --- | --- | --- | --- | --- |
| 1 | 2.5 s | (0.490, 0.240) | (0.490, 0.470) | y | White wig down to the hand resting at the cheek |
| 2 | 2.5 s | (0.220, 0.238) | (0.780, 0.238) | x | Grey ceiling and thin white cage line |
| 3 | 2.5 s | (0.220, 0.260) | (0.220, 0.460) | y | Left upright down to where the drawn line stops |
| 4 | 2.5 s | (0.230, 0.560) | (0.380, 0.560) | x | Small curly figure toward the central drapery |
| 5 | 2.5 s | (0.640, 0.510) | (0.830, 0.510) | x | Central arm toward the blonde inward-facing figure and wing |
| 6 | 2.5 s | (0.650, 0.690) | (0.650, 0.773) | y | Reclining grey-haired figure and raised legs into coral paint |

Intermediate shots keep a constant scale and move on a single axis until the cut. All cuts lie on the 0.5-second grid. The last shot alone zooms: fixed centre, close view → complete painting fitting on white, 6 seconds total, specified 2-second hold.

## Excluded files and eligibility

IN ORDER- FRAMED/0.png (A0427) is a Leonardo reference painting, definitively excluded. DETAYLAR2 drawings and digital-artwork are source references, not stages or finished-painted details. COLOR and COLOR-EDITED variants, MERGE mosaics and v2 alternate exports excluded. RESOLUTION without COLOR is used as the highest normal whole export; no enhancement performed here.

## Sources

- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_5_virginonrocks\virgil-on-virtual-cage-RESOLUTION.png`

## Music mood suggestions

- Sparse instrumental jazz, dry percussion.
- Minimal electronic pulse around 120 BPM, no vocals.
- Restrained ambient texture.

Music is selected and added by Yiğit in Instagram; no audio has been embedded.

## Validation

```json
{
  "slug": "virgil-on-virtual-cage-final-final-finalv9",
  "type": "details",
  "duration": 21.0,
  "frames": 630,
  "video_only": true,
  "h264_1080x1920_30fps": true,
  "full_decode": true,
  "approved_preserved": false,
  "freeze_starts": [
    19.0
  ],
  "specified_hold_start": 19.0,
  "detector_flags_before_hold": [],
  "mid_route_freeze_starts": [],
  "final_target_frames": 60
}
```

Renderer fixes: the original unbounded decoded-image cache and eager stage retention were replaced with one-source retention; identical static frames are reused. Encoder uses four threads to bound memory, keeping preset slow and CRF 17. A one-frame-early target interpolation was fixed: new detail renders now hold the final view for exactly 60 frames, not 61. Camera rejection rules are unchanged. Regression checks confirm diagonal motion, off-centre zoom, process motion and cropped process frames still fail, and unchanged frame geometry matches the original pixel-for-pixel. Approved historical videos are not modified by these fixes.

Freeze-detector interpretation: the supplied low-motion threshold can flag the last few easing frames just before the fixed hold. Exact reported times remain above; no intermediate route freeze occurred. New renders reach the fixed target at the specified hold boundary and contain exactly 60 target frames, as verified in the renderer regression check.

Visual review: the actual 15-frame encoded strip was inspected for the selected detail route, final complete-artwork fit and stage-only sequence; crop choices and exclusions are documented above. Original source photographs and Milano folders were not modified.
