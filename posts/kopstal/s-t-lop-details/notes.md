# s(t)lop · details

21 s · 1080 × 1920 · 30 fps · H.264 · no audio stream · no on-screen text. No publishing date assigned.

Catalog: `decentralize-dfw/yigit/v3/content/works.json`, blob `3c643323bffb2153bef1adedc4ac80977e24aa09`. Both description and artist note were read before selecting the composition route.

## Points of interest

Coordinates are normalized inside the named EXIF-oriented source, not the Reel frame. Each point names the depicted region that motivates its shot.

| Point | Source | (cx, cy) | Visible interest and selection reason |
| --- | --- | --- | --- |
| 1 | A0134 | (0.405, 0.240) | Rounded head across the tapering beak |
| 2 | A0134 | (0.645, 0.400) | Open mouth across the row of red notches |
| 3 | A0134 | (0.320, 0.600) | Curved wing strokes into the lower body |
| 4 | A0134 | (0.290, 0.746) | Narrow legs toward the bottom edge |
| 5 | A0134 | (0.770, 0.354) | Purple bars in the upper rectangular panel |
| 6 | A0134 | (0.730, 0.625) | Lower yellow rectangle down to the boxed white head |

## Shot route

| Shot | Duration | Start (cx, cy) | End (cx, cy) | Axis | Visible connection |
| --- | --- | --- | --- | --- | --- |
| 1 | 2.5 s | (0.250, 0.240) | (0.560, 0.240) | x | Rounded head across the tapering beak |
| 2 | 2.5 s | (0.520, 0.400) | (0.770, 0.400) | x | Open mouth across the row of red notches |
| 3 | 2.5 s | (0.320, 0.480) | (0.320, 0.720) | y | Curved wing strokes into the lower body |
| 4 | 2.5 s | (0.290, 0.720) | (0.290, 0.773) | y | Narrow legs toward the bottom edge |
| 5 | 2.5 s | (0.770, 0.227) | (0.770, 0.480) | y | Purple bars in the upper rectangular panel |
| 6 | 2.5 s | (0.730, 0.530) | (0.730, 0.720) | y | Lower yellow rectangle down to the boxed white head |

Intermediate shots keep a constant scale and move on a single axis until the cut. All cuts lie on the 0.5-second grid. The last shot alone zooms: fixed centre, close view → complete painting fitting on white, 6 seconds total, specified 2-second hold.

## Excluded files and eligibility

Process skipped: folder contains finished painting, edited details and camera copies, but no four distinct making-stage photographs. Low detail exports A0087–A0094 excluded in favour of high-resolution files. No process sequence fabricated.

## Sources

- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_1_stlop\Stlop-full.png`

## Music mood suggestions

- Sparse instrumental jazz, dry percussion.
- Minimal electronic pulse around 120 BPM, no vocals.
- Restrained ambient texture.

Music is selected and added by Yiğit in Instagram; no audio has been embedded.

## Validation

```json
{
  "slug": "s-t-lop",
  "type": "details",
  "duration": 21.0,
  "frames": 630,
  "video_only": true,
  "h264_1080x1920_30fps": true,
  "full_decode": true,
  "approved_preserved": false,
  "freeze_starts": [
    18.933333,
    19.133333
  ],
  "specified_hold_start": 19.0,
  "detector_flags_before_hold": [
    18.933333
  ],
  "mid_route_freeze_starts": [],
  "final_target_frames": 60
}
```

Renderer fixes: the original unbounded decoded-image cache and eager stage retention were replaced with one-source retention; identical static frames are reused. Encoder uses four threads to bound memory, keeping preset slow and CRF 17. A one-frame-early target interpolation was fixed: new detail renders now hold the final view for exactly 60 frames, not 61. Camera rejection rules are unchanged. Regression checks confirm diagonal motion, off-centre zoom, process motion and cropped process frames still fail, and unchanged frame geometry matches the original pixel-for-pixel. Approved historical videos are not modified by these fixes.

Freeze-detector interpretation: the supplied low-motion threshold can flag the last few easing frames just before the fixed hold. Exact reported times remain above; no intermediate route freeze occurred. New renders reach the fixed target at the specified hold boundary and contain exactly 60 target frames, as verified in the renderer regression check.

Visual review: the actual 15-frame encoded strip was inspected for the selected detail route, final complete-artwork fit and stage-only sequence; crop choices and exclusions are documented above. Original source photographs and Milano folders were not modified.
