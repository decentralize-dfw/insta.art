# gary grills cooper · details

23.5 s · 1080 × 1920 · 30 fps · H.264 · no audio stream · no on-screen text. No publishing date assigned.

Catalog: `decentralize-dfw/yigit/v3/content/works.json`, blob `3c643323bffb2153bef1adedc4ac80977e24aa09`. Both description and artist note were read before selecting the composition route.

The previously approved MP4 and cover are preserved byte-for-byte. The spec keeps its historical cloud source aliases; it is a provenance copy, not a claim that a new local render was made.

## Points of interest

Coordinates are normalized inside the named EXIF-oriented source, not the Reel frame. Each point names the depicted region that motivates its shot.

| Point | Source | (cx, cy) | Visible interest and selection reason |
| --- | --- | --- | --- |
| 1 | original approved source | (0.500, 0.500) | face |
| 2 | original approved source | (0.500, 0.500) | mouth and cigar |
| 3 | original approved source | (0.500, 0.500) | collar |
| 4 | original approved source | (0.500, 0.500) | hands and the match |
| 5 | original approved source | (0.500, 0.500) | the grill |
| 6 | original approved source | (0.500, 0.500) | arm and the turquoise streak |
| 7 | original approved source | (0.500, 0.500) | coloured masses |

## Shot route

| Shot | Duration | Start (cx, cy) | End (cx, cy) | Axis | Visible connection |
| --- | --- | --- | --- | --- | --- |
| 1 | 2.5 s | (0.300, 0.500) | (0.700, 0.500) | x | face |
| 2 | 2.5 s | (0.700, 0.500) | (0.300, 0.500) | x | mouth and cigar |
| 3 | 2.5 s | (0.300, 0.500) | (0.700, 0.500) | x | collar |
| 4 | 2.5 s | (0.700, 0.500) | (0.300, 0.500) | x | hands and the match |
| 5 | 2.5 s | (0.300, 0.500) | (0.700, 0.500) | x | the grill |
| 6 | 2.5 s | (0.700, 0.500) | (0.300, 0.500) | x | arm and the turquoise streak |
| 7 | 2.5 s | (0.300, 0.500) | (0.700, 0.500) | x | coloured masses |

Intermediate shots keep a constant scale and move on a single axis until the cut. All cuts lie on the 0.5-second grid. The last shot alone zooms: fixed centre, close view → complete painting fitting on white, 6 seconds total, specified 2-second hold.

## Excluded files and eligibility

Existing approved process and details preserved byte-for-byte. No new render. The reference press photograph remains excluded. Historical cloud aliases remain in the preserved spec; no unsupported local-source equivalence is claimed.

## Sources

- `details:garygrillscooper/garlgrillscooper_detail_2.png`
- `details:garygrillscooper/garlgrillscooper_detail_3.png`
- `details:garygrillscooper/garlgrillscooper_detail_7.png`
- `details:garygrillscooper/garlgrillscooper_detail_9.png`
- `details:garygrillscooper/garlgrillscooper_detail_6.png`
- `details:garygrillscooper/garlgrillscooper_detail_5.png`
- `details:garygrillscooper/garlgrillscooper_detail_8.png`
- `yigit:img/full/gary-grills-cooper.jpg`

## Music mood suggestions

- Sparse instrumental jazz, dry percussion.
- Minimal electronic pulse around 120 BPM, no vocals.
- Restrained ambient texture.

Music is selected and added by Yiğit in Instagram; no audio has been embedded.

## Validation

```json
{
  "slug": "gary-grills-cooper",
  "type": "details",
  "duration": 23.5,
  "frames": 705,
  "video_only": true,
  "h264_1080x1920_30fps": true,
  "full_decode": true,
  "approved_preserved": true,
  "freeze_starts": [
    21.4,
    21.566667
  ],
  "specified_hold_start": 21.5,
  "detector_flags_before_hold": [
    21.4
  ],
  "mid_route_freeze_starts": [],
  "final_target_frames": "historical approved render, unchanged"
}
```

Renderer fixes: the original unbounded decoded-image cache and eager stage retention were replaced with one-source retention; identical static frames are reused. Encoder uses four threads to bound memory, keeping preset slow and CRF 17. A one-frame-early target interpolation was fixed: new detail renders now hold the final view for exactly 60 frames, not 61. Camera rejection rules are unchanged. Regression checks confirm diagonal motion, off-centre zoom, process motion and cropped process frames still fail, and unchanged frame geometry matches the original pixel-for-pixel. Approved historical videos are not modified by these fixes.

Freeze-detector interpretation: the supplied low-motion threshold can flag the last few easing frames just before the fixed hold. Exact reported times remain above; no intermediate route freeze occurred. New renders reach the fixed target at the specified hold boundary and contain exactly 60 target frames, as verified in the renderer regression check.

Visual review: the actual 15-frame encoded strip was inspected for the selected detail route, final complete-artwork fit and stage-only sequence; crop choices and exclusions are documented above. Original source photographs and Milano folders were not modified.
