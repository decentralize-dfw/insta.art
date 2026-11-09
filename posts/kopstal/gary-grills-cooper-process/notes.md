# gary grills cooper · process

7.5 s · 1080 × 1920 · 30 fps · H.264 · no audio stream · no on-screen text. No publishing date assigned.

Catalog: `decentralize-dfw/yigit/v3/content/works.json`, blob `3c643323bffb2153bef1adedc4ac80977e24aa09`. Both description and artist note were read before selecting the composition route.

The previously approved MP4 and cover are preserved byte-for-byte. The spec keeps its historical cloud source aliases; it is a provenance copy, not a claim that a new local render was made.

## Points of interest

The camera remains completely static. Each genuine stage is shown once for 0.5 seconds, whole and in its own aspect ratio on white, then the complete finished painting for 2 seconds. Short process reels are not padded or repeated to reach the generic detail-Reel duration.

## Excluded files and eligibility

Existing approved process and details preserved byte-for-byte. No new render. The reference press photograph remains excluded. Historical cloud aliases remain in the preserved spec; no unsupported local-source equivalence is claimed.

## Sources

- `yigit:img/full/process/gary-grills-cooper-02.jpg`
- `yigit:img/full/process/gary-grills-cooper-03.jpg`
- `yigit:img/full/process/gary-grills-cooper-04.jpg`
- `yigit:img/full/process/gary-grills-cooper-05.jpg`
- `yigit:img/full/process/gary-grills-cooper-06.jpg`
- `yigit:img/full/process/gary-grills-cooper-07.jpg`
- `yigit:img/full/process/gary-grills-cooper-08.jpg`
- `yigit:img/full/process/gary-grills-cooper-09.jpg`
- `yigit:img/full/process/gary-grills-cooper-10.jpg`
- `yigit:img/full/process/gary-grills-cooper-11.jpg`
- `yigit:img/full/process/gary-grills-cooper-12.jpg`
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
  "type": "process",
  "duration": 7.5,
  "frames": 225,
  "video_only": true,
  "h264_1080x1920_30fps": true,
  "full_decode": true,
  "approved_preserved": true,
  "distinct_frames": 12,
  "expected_distinct_frames": 12,
  "distinct_count_matches": true
}
```

Renderer fixes: the original unbounded decoded-image cache and eager stage retention were replaced with one-source retention; identical static frames are reused. Encoder uses four threads to bound memory, keeping preset slow and CRF 17. A one-frame-early target interpolation was fixed: new detail renders now hold the final view for exactly 60 frames, not 61. Camera rejection rules are unchanged. Regression checks confirm diagonal motion, off-centre zoom, process motion and cropped process frames still fail, and unchanged frame geometry matches the original pixel-for-pixel. Approved historical videos are not modified by these fixes.

Visual review: the actual 15-frame encoded strip was inspected for the selected detail route, final complete-artwork fit and stage-only sequence; crop choices and exclusions are documented above. Original source photographs and Milano folders were not modified.
