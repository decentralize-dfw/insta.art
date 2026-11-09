# sept neuf · details

21 s · 1080 × 1920 · 30 fps · H.264 · no audio stream · no on-screen text. No publishing date assigned.

Catalog: `decentralize-dfw/yigit/v3/content/works.json`, blob `3c643323bffb2153bef1adedc4ac80977e24aa09`. Both description and artist note were read before selecting the composition route.

## Points of interest

Coordinates are normalized inside the named EXIF-oriented source, not the Reel frame. Each point names the depicted region that motivates its shot.

| Point | Source | (cx, cy) | Visible interest and selection reason |
| --- | --- | --- | --- |
| 1 | A1157 | (0.390, 0.300) | Cigarette hand toward the face and two different eyes |
| 2 | A1157 | (0.360, 0.460) | Yellow dress line down to red chest squares |
| 3 | A1157 | (0.220, 0.655) | White nails on the chair arm toward the mint coils |
| 4 | A1157 | (0.480, 0.716) | Crossed legs down to white shoes |
| 5 | A1157 | (0.738, 0.550) | Chair edge across to black table structure |
| 6 | A1157 | (0.770, 0.470) | Table top up through the pale bird to its turned head |

## Shot route

| Shot | Duration | Start (cx, cy) | End (cx, cy) | Axis | Visible connection |
| --- | --- | --- | --- | --- | --- |
| 1 | 2.5 s | (0.510, 0.300) | (0.270, 0.300) | x | Cigarette hand toward the face and two different eyes |
| 2 | 2.5 s | (0.360, 0.350) | (0.360, 0.570) | y | Yellow dress line down to red chest squares |
| 3 | 2.5 s | (0.220, 0.550) | (0.220, 0.760) | y | White nails on the chair arm toward the mint coils |
| 4 | 2.5 s | (0.480, 0.660) | (0.480, 0.773) | y | Crossed legs down to white shoes |
| 5 | 2.5 s | (0.650, 0.550) | (0.826, 0.550) | x | Chair edge across to black table structure |
| 6 | 2.5 s | (0.770, 0.590) | (0.770, 0.350) | y | Table top up through the pale bird to its turned head |

Intermediate shots keep a constant scale and move on a single axis until the cut. All cuts lie on the 0.5-second grid. The last shot alone zooms: fixed centre, close view → complete painting fitting on white, 6 seconds total, specified 2-second hold.

## Excluded files and eligibility

inverted-silvia--7-9.png and HIGHRES-sfx2/sfx3 excluded. Otto Dix, David and Caravaggio images are reference paintings, not stages. 1-P/1-P-2 are alternate drawing exports; use actual canvas photo 1.png once. KOLAJ and grok directories excluded. Real brush footage is outside this photo-stage task.

## Sources

- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_7_nine-eleven\SEPT-NEUF-HIGHRES.png`

## Music mood suggestions

- Sparse instrumental jazz, dry percussion.
- Minimal electronic pulse around 120 BPM, no vocals.
- Restrained ambient texture.

Music is selected and added by Yiğit in Instagram; no audio has been embedded.

## Validation

```json
{
  "slug": "sept-neuf",
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
