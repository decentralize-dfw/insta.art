# Angora Mergvs · details

30 s · 1080 × 1920 · 30 fps · H.264 · no audio stream · no on-screen text. No publishing date assigned.

Catalog: `decentralize-dfw/yigit/v3/content/works.json`, blob `3c643323bffb2153bef1adedc4ac80977e24aa09`. Both description and artist note were read before selecting the composition route.

The previously approved MP4 and cover are preserved byte-for-byte. The spec keeps its historical cloud source aliases; it is a provenance copy, not a claim that a new local render was made.

## Points of interest

Coordinates are normalized inside the named EXIF-oriented source, not the Reel frame. Each point names the depicted region that motivates its shot.

| Point | Source | (cx, cy) | Visible interest and selection reason |
| --- | --- | --- | --- |
| 1 | original approved source | (0.470, 0.500) | face: eyes down to teeth |
| 2 | original approved source | (0.500, 0.450) | creature and wings |
| 3 | original approved source | (0.480, 0.550) | claw to claw |
| 4 | original approved source | (0.450, 0.500) | claw on the post |
| 5 | original approved source | (0.550, 0.500) | window up to the roof |
| 6 | original approved source | (0.500, 0.500) | roof edges |
| 7 | original approved source | (0.450, 0.500) | burning tail |
| 8 | original approved source | (0.450, 0.500) | wing |
| 9 | original approved source | (0.550, 0.450) | from the creature down to the houses |

## Shot route

| Shot | Duration | Start (cx, cy) | End (cx, cy) | Axis | Visible connection |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 s | (0.470, 0.320) | (0.470, 0.680) | y | face: eyes down to teeth |
| 2 | 2.5 s | (0.350, 0.450) | (0.650, 0.450) | x | creature and wings |
| 3 | 2.5 s | (0.220, 0.550) | (0.740, 0.550) | x | claw to claw |
| 4 | 2.5 s | (0.450, 0.320) | (0.450, 0.680) | y | claw on the post |
| 5 | 2.5 s | (0.550, 0.680) | (0.550, 0.320) | y | window up to the roof |
| 6 | 2.5 s | (0.300, 0.500) | (0.700, 0.500) | x | roof edges |
| 7 | 2.5 s | (0.450, 0.680) | (0.450, 0.320) | y | burning tail |
| 8 | 2.5 s | (0.250, 0.500) | (0.650, 0.500) | x | wing |
| 9 | 2.5 s | (0.550, 0.200) | (0.550, 0.700) | y | from the creature down to the houses |
| 10 | 2 s | (0.300, 0.500) | (0.700, 0.500) | x | roofs |

Intermediate shots keep a constant scale and move on a single axis until the cut. All cuts lie on the 0.5-second grid. The last shot alone zooms: fixed centre, close view → complete painting fitting on white, 6 seconds total, specified 2-second hold.

## Excluded files and eligibility

All remix/MIX files, synthetic reference renders and process collages excluded. FRAMED has no 11.png; no missing stage invented. A1554 / FRAMED/0.png is a cleaned black-on-white line-art export: native pixels do not establish it as a photographed making stage, so it is conservatively excluded. The video begins with 1.png, whose canvas surface and initial yellow underpainting are visible. Approved detail MP4 preserved without rendering.

## Sources

- `details:angora-mergvs/angora-mergvs-detail-6.jpg`
- `details:angora-mergvs/angora-mergvs-detail-11.jpg`
- `details:angora-mergvs/angora-mergvs-detail-5.jpg`
- `details:angora-mergvs/angora-mergvs-detail-4.jpg`
- `details:angora-mergvs/angora-mergvs-detail-1.jpg`
- `details:angora-mergvs/angora-mergvs-detail-3.jpg`
- `details:angora-mergvs/angora-mergvs-detail-9.jpg`
- `details:angora-mergvs/angora-mergvs-detail-8.jpg`
- `details:angora-mergvs/angora-mergvs-10mb.jpg`
- `details:angora-mergvs/angora-mergvs-detail-2.jpg`

## Music mood suggestions

- Sparse instrumental jazz, dry percussion.
- Minimal electronic pulse around 120 BPM, no vocals.
- Restrained ambient texture.

Music is selected and added by Yiğit in Instagram; no audio has been embedded.

## Validation

```json
{
  "slug": "angora-mergvs",
  "type": "details",
  "duration": 30.0,
  "frames": 900,
  "video_only": true,
  "h264_1080x1920_30fps": true,
  "full_decode": true,
  "approved_preserved": true,
  "freeze_starts": [
    27.933333,
    28.366667
  ],
  "specified_hold_start": 28.0,
  "detector_flags_before_hold": [
    27.933333
  ],
  "mid_route_freeze_starts": [],
  "final_target_frames": "historical approved render, unchanged"
}
```

Renderer fixes: the original unbounded decoded-image cache and eager stage retention were replaced with one-source retention; identical static frames are reused. Encoder uses four threads to bound memory, keeping preset slow and CRF 17. A one-frame-early target interpolation was fixed: new detail renders now hold the final view for exactly 60 frames, not 61. Camera rejection rules are unchanged. Regression checks confirm diagonal motion, off-centre zoom, process motion and cropped process frames still fail, and unchanged frame geometry matches the original pixel-for-pixel. Approved historical videos are not modified by these fixes.

Freeze-detector interpretation: the supplied low-motion threshold can flag the last few easing frames just before the fixed hold. Exact reported times remain above; no intermediate route freeze occurred. New renders reach the fixed target at the specified hold boundary and contain exactly 60 target frames, as verified in the renderer regression check.

Visual review: the actual 15-frame encoded strip was inspected for the selected detail route, final complete-artwork fit and stage-only sequence; crop choices and exclusions are documented above. Original source photographs and Milano folders were not modified.
