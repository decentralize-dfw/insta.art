# walls of perception · details

21 s · 1080 × 1920 · 30 fps · H.264 · no audio stream · no on-screen text. No publishing date assigned.

Catalog: `decentralize-dfw/yigit/v3/content/works.json`, blob `3c643323bffb2153bef1adedc4ac80977e24aa09`. Both description and artist note were read before selecting the composition route.

## Points of interest

Coordinates are normalized inside the named EXIF-oriented source, not the Reel frame. Each point names the depicted region that motivates its shot.

| Point | Source | (cx, cy) | Visible interest and selection reason |
| --- | --- | --- | --- |
| 1 | A0278 | (0.500, 0.230) | Cream brim across the purple hat band |
| 2 | A0278 | (0.460, 0.425) | Dark mouth and blue triangle into the yellow grain column |
| 3 | A0278 | (0.490, 0.655) | Grain column continues down into the bowl |
| 4 | A0278 | (0.525, 0.762) | Bowl and red octagonal cloth across toward the utensil |
| 5 | A0278 | (0.760, 0.635) | Grey beaded utensil up toward the lavender flower |

## Shot route

| Shot | Duration | Start (cx, cy) | End (cx, cy) | Axis | Visible connection |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 s | (0.270, 0.230) | (0.730, 0.230) | x | Cream brim across the purple hat band |
| 2 | 3 s | (0.460, 0.310) | (0.460, 0.540) | y | Dark mouth and blue triangle into the yellow grain column |
| 3 | 3 s | (0.490, 0.540) | (0.490, 0.770) | y | Grain column continues down into the bowl |
| 4 | 3 s | (0.360, 0.762) | (0.690, 0.762) | x | Bowl and red octagonal cloth across toward the utensil |
| 5 | 3 s | (0.760, 0.760) | (0.760, 0.510) | y | Grey beaded utensil up toward the lavender flower |

Intermediate shots keep a constant scale and move on a single axis until the cut. All cuts lie on the 0.5-second grid. The last shot alone zooms: fixed centre, close view → complete painting fitting on white, 6 seconds total, specified 2-second hold.

The route uses five 3-second pans so the grain column reads continuously; the redundant second flower detail was removed. No repeated flower shot was added to fill time.

## Excluded files and eligibility

sketch.png is a separate clean line drawing. LOW JPG and uncropped room photographs excluded in favour of the already aligned 1–5 stages. No effect or colour correction applied.

## Sources

- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_3_wall of perception\Walls-of-perception-HIGHRES.png`

## Music mood suggestions

- Sparse instrumental jazz, dry percussion.
- Minimal electronic pulse around 120 BPM, no vocals.
- Restrained ambient texture.

Music is selected and added by Yiğit in Instagram; no audio has been embedded.

## Validation

```json
{
  "slug": "walls-of-perception",
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
