# Angora Mergvs · process

9 s · 1080 × 1920 · 30 fps · H.264 · no audio stream · no on-screen text. No publishing date assigned.

Catalog: `decentralize-dfw/yigit/v3/content/works.json`, blob `3c643323bffb2153bef1adedc4ac80977e24aa09`. Both description and artist note were read before selecting the composition route.

## Points of interest

The camera remains completely static. Each genuine stage is shown once for 0.5 seconds, whole and in its own aspect ratio on white, then the complete finished painting for 2 seconds. Short process reels are not padded or repeated to reach the generic detail-Reel duration.

## Excluded files and eligibility

All remix/MIX files, synthetic reference renders and process collages excluded. FRAMED has no 11.png; no missing stage invented. 0.png is the initial canvas drawing, visually followed by underpainting and painted stages. Approved detail MP4 preserved without rendering.

## Sources

- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_9_charizard angora\PROCESS\FRAMED\0.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_9_charizard angora\PROCESS\FRAMED\1.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_9_charizard angora\PROCESS\FRAMED\2.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_9_charizard angora\PROCESS\FRAMED\3.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_9_charizard angora\PROCESS\FRAMED\4.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_9_charizard angora\PROCESS\FRAMED\5.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_9_charizard angora\PROCESS\FRAMED\6.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_9_charizard angora\PROCESS\FRAMED\7.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_9_charizard angora\PROCESS\FRAMED\8.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_9_charizard angora\PROCESS\FRAMED\9.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_9_charizard angora\PROCESS\FRAMED\10.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_9_charizard angora\PROCESS\FRAMED\12.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_9_charizard angora\PROCESS\FRAMED\13.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_9_charizard angora\PROCESS\FRAMED\14.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_9_charizard angora\ANGORA-MERGVS-normal.jpg`

## Music mood suggestions

- Sparse instrumental jazz, dry percussion.
- Minimal electronic pulse around 120 BPM, no vocals.
- Restrained ambient texture.

Music is selected and added by Yiğit in Instagram; no audio has been embedded.

## Validation

```json
{
  "slug": "angora-mergvs",
  "type": "process",
  "duration": 9.0,
  "frames": 270,
  "video_only": true,
  "h264_1080x1920_30fps": true,
  "full_decode": true,
  "approved_preserved": false,
  "distinct_frames": 15,
  "expected_distinct_frames": 15,
  "distinct_count_matches": true
}
```

Renderer fixes: the original unbounded decoded-image cache and eager stage retention were replaced with one-source retention; identical static frames are reused. Encoder uses four threads to bound memory, keeping preset slow and CRF 17. A one-frame-early target interpolation was fixed: new detail renders now hold the final view for exactly 60 frames, not 61. Camera rejection rules are unchanged. Regression checks confirm diagonal motion, off-centre zoom, process motion and cropped process frames still fail, and unchanged frame geometry matches the original pixel-for-pixel. Approved historical videos are not modified by these fixes.

Visual review: the actual 15-frame encoded strip was inspected for the selected detail route, final complete-artwork fit and stage-only sequence; crop choices and exclusions are documented above. Original source photographs and Milano folders were not modified.
