# 7 fam board game · details

21 s · 1080 × 1920 · 30 fps · H.264 · no audio stream · no on-screen text. No publishing date assigned.

Catalog: `decentralize-dfw/yigit/v3/content/works.json`, blob `3c643323bffb2153bef1adedc4ac80977e24aa09`. Both description and artist note were read before selecting the composition route.

## Points of interest

Coordinates are normalized inside the named EXIF-oriented source, not the Reel frame. Each point names the depicted region that motivates its shot.

| Point | Source | (cx, cy) | Visible interest and selection reason |
| --- | --- | --- | --- |
| 1 | A0591 | (0.260, 0.380) | Rounded large head down to its tapering tube |
| 2 | A0591 | (0.505, 0.380) | Large player toward the scowling player opposite |
| 3 | A0591 | (0.700, 0.575) | White collar cords down into the board |
| 4 | A0591 | (0.395, 0.706) | Separate wrapped pink cones across the board |
| 5 | A0591 | (0.635, 0.650) | Blue heads from small stacks to the dense eared group |
| 6 | A0591 | (0.760, 0.670) | Upper blue stack down to the pieces at the near edge |

## Shot route

| Shot | Duration | Start (cx, cy) | End (cx, cy) | Axis | Visible connection |
| --- | --- | --- | --- | --- | --- |
| 1 | 2.5 s | (0.260, 0.250) | (0.260, 0.510) | y | Rounded large head down to its tapering tube |
| 2 | 2.5 s | (0.310, 0.380) | (0.700, 0.380) | x | Large player toward the scowling player opposite |
| 3 | 2.5 s | (0.700, 0.440) | (0.700, 0.710) | y | White collar cords down into the board |
| 4 | 2.5 s | (0.300, 0.706) | (0.490, 0.706) | x | Separate wrapped pink cones across the board |
| 5 | 2.5 s | (0.470, 0.650) | (0.800, 0.650) | x | Blue heads from small stacks to the dense eared group |
| 6 | 2.5 s | (0.760, 0.590) | (0.760, 0.750) | y | Upper blue stack down to the pieces at the near edge |

Intermediate shots keep a constant scale and move on a single axis until the cut. All cuts lie on the 0.5-second grid. The last shot alone zooms: fixed centre, close view → complete painting fitting on white, 6 seconds total, specified 2-second hold.

## Excluded files and eligibility

Image-1.jpg is a film/reference still. Untitled-3.jpg is a reference drawing. effct and effct2 excluded. FRAMED merged files are stage mosaics, excluded. RAW, LOW and sideways camera duplicates excluded in favour of aligned stage originals.

## Sources

- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_6_7thsela\7fam-board-game-FULLSIZE.png`

## Music mood suggestions

- Sparse instrumental jazz, dry percussion.
- Minimal electronic pulse around 120 BPM, no vocals.
- Restrained ambient texture.

Music is selected and added by Yiğit in Instagram; no audio has been embedded.

## Validation

```json
{
  "slug": "7-fam-board-game",
  "type": "details",
  "duration": 21.0,
  "frames": 630,
  "video_only": true,
  "h264_1080x1920_30fps": true,
  "full_decode": true,
  "approved_preserved": false,
  "freeze_starts": [
    18.933333
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
