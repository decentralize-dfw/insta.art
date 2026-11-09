# Painstaking · details

21 s · 1080 × 1920 · 30 fps · H.264 · no audio stream · no on-screen text. No publishing date assigned.

Catalog: `decentralize-dfw/yigit/v3/content/works.json`, blob `3c643323bffb2153bef1adedc4ac80977e24aa09`. Both description and artist note were read before selecting the composition route.

## Points of interest

Coordinates are normalized inside the named EXIF-oriented source, not the Reel frame. Each point names the depicted region that motivates its shot.

| Point | Source | (cx, cy) | Visible interest and selection reason |
| --- | --- | --- | --- |
| 1 | A0028 | (0.500, 0.350) | Left panel: crimson brow to pale eye |
| 2 | A0028 | (0.530, 0.626) | Left panel: nose to swept mouth and chin |
| 3 | A0029 | (0.500, 0.340) | Middle panel: rounded eye forms |
| 4 | A0029 | (0.510, 0.615) | Middle panel: nostrils to white teeth |
| 5 | A0027 | (0.500, 0.350) | Right panel: uneven eyes and nose bridge |
| 6 | A0027 | (0.520, 0.656) | Right panel: open mouth to dark clothing and red tie |

## Shot route

| Shot | Duration | Start (cx, cy) | End (cx, cy) | Axis | Visible connection |
| --- | --- | --- | --- | --- | --- |
| 1 | 2.5 s | (0.340, 0.350) | (0.660, 0.350) | x | Left panel: crimson brow to pale eye |
| 2 | 2.5 s | (0.530, 0.480) | (0.530, 0.773) | y | Left panel: nose to swept mouth and chin |
| 3 | 2.5 s | (0.320, 0.340) | (0.680, 0.340) | x | Middle panel: rounded eye forms |
| 4 | 2.5 s | (0.510, 0.460) | (0.510, 0.770) | y | Middle panel: nostrils to white teeth |
| 5 | 2.5 s | (0.330, 0.350) | (0.670, 0.350) | x | Right panel: uneven eyes and nose bridge |
| 6 | 2.5 s | (0.520, 0.540) | (0.520, 0.773) | y | Right panel: open mouth to dark clothing and red tie |

Intermediate shots keep a constant scale and move on a single axis until the cut. All cuts lie on the 0.5-second grid. The last shot alone zooms: fixed centre, close view → complete painting fitting on white, 6 seconds total, specified 2-second hold.

## Excluded files and eligibility

Process skipped: A0023 and A0084 show an early state; A0022 is a collage of the same panels, not four distinct stage photos. Separate finished panels are not process stages. A0024 SFX excluded; A0026 black-gap presentation excluded in favour of white gaps.

## Sources

- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_10_painstaking\paıinstake-s.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_10_painstaking\paıinstake-y.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_10_painstaking\paıinstake-h.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_10_painstaking\painstaking-triptic-boş.png`

## Music mood suggestions

- Sparse instrumental jazz, dry percussion.
- Minimal electronic pulse around 120 BPM, no vocals.
- Restrained ambient texture.

Music is selected and added by Yiğit in Instagram; no audio has been embedded.

## Validation

```json
{
  "slug": "painstaking",
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
