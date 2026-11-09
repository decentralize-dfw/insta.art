# sept neuf · process

11 s · 1080 × 1920 · 30 fps · H.264 · no audio stream · no on-screen text. No publishing date assigned.

Catalog: `decentralize-dfw/yigit/v3/content/works.json`, blob `3c643323bffb2153bef1adedc4ac80977e24aa09`. Both description and artist note were read before selecting the composition route.

## Points of interest

The camera remains completely static. Each genuine stage is shown once for 0.5 seconds, whole and in its own aspect ratio on white, then the complete finished painting for 2 seconds. Short process reels are not padded or repeated to reach the generic detail-Reel duration.

## Excluded files and eligibility

inverted-silvia--7-9.png and HIGHRES-sfx2/sfx3 excluded. Otto Dix, David and Caravaggio images are reference paintings, not stages. 1-P/1-P-2 are alternate drawing exports; use actual canvas photo 1.png once. KOLAJ and grok directories excluded. Real brush footage is outside this photo-stage task.

## Sources

- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_7_nine-eleven\PROCESS ihpne\1.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_7_nine-eleven\PROCESS ihpne\2.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_7_nine-eleven\PROCESS ihpne\3.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_7_nine-eleven\PROCESS ihpne\4.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_7_nine-eleven\PROCESS ihpne\5.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_7_nine-eleven\PROCESS ihpne\6.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_7_nine-eleven\PROCESS ihpne\7.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_7_nine-eleven\PROCESS ihpne\8.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_7_nine-eleven\PROCESS ihpne\9.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_7_nine-eleven\PROCESS ihpne\10.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_7_nine-eleven\PROCESS ihpne\11.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_7_nine-eleven\PROCESS ihpne\12.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_7_nine-eleven\PROCESS ihpne\13.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_7_nine-eleven\PROCESS ihpne\14.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_7_nine-eleven\PROCESS ihpne\15.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_7_nine-eleven\PROCESS ihpne\16.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_7_nine-eleven\PROCESS ihpne\17.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_7_nine-eleven\PROCESS ihpne\18.png`
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
  "type": "process",
  "duration": 11.0,
  "frames": 330,
  "video_only": true,
  "h264_1080x1920_30fps": true,
  "full_decode": true,
  "approved_preserved": false,
  "distinct_frames": 19,
  "expected_distinct_frames": 19,
  "distinct_count_matches": true
}
```

Renderer fixes: the original unbounded decoded-image cache and eager stage retention were replaced with one-source retention; identical static frames are reused. Encoder uses four threads to bound memory, keeping preset slow and CRF 17. A one-frame-early target interpolation was fixed: new detail renders now hold the final view for exactly 60 frames, not 61. Camera rejection rules are unchanged. Regression checks confirm diagonal motion, off-centre zoom, process motion and cropped process frames still fail, and unchanged frame geometry matches the original pixel-for-pixel. Approved historical videos are not modified by these fixes.

Visual review: the actual 15-frame encoded strip was inspected for the selected detail route, final complete-artwork fit and stage-only sequence; crop choices and exclusions are documented above. Original source photographs and Milano folders were not modified.
