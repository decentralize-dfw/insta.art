# articulo attack on mandarin · process

4.5 s · 1080 × 1920 · 30 fps · H.264 · no audio stream · no on-screen text. No publishing date assigned.

Catalog: `decentralize-dfw/yigit/v3/content/works.json`, blob `3c643323bffb2153bef1adedc4ac80977e24aa09`. Both description and artist note were read before selecting the composition route.

## Points of interest

The camera remains completely static. Each genuine stage is shown once for 0.5 seconds, whole and in its own aspect ratio on white, then the complete finished painting for 2 seconds. Short process reels are not padded or repeated to reach the generic detail-Reel duration.

## Excluded files and eligibility

IMG_6639 copy is a horizontally cropped camera detail and cannot serve as the full painting. A0191 explicitly names image_gpt; painting.png and 12000-square Yeni Proje.png have uncertain enlarged/synthetic presentation provenance, so all are excluded. A0192 is only 1890 square: the required final cover 1.3 would exceed 1.25x upscale. Instead the original real full photo A0194 is perspective-rectified from its four canvas corners to 3500 square; no colour/contrast edits. PROCES-SFRAMED 0/0-0/aaa/aaaaaa are sketches or drawing exports, not painted stages. Use five genuine painted states 1–5.

## Sources

- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_2_mandarin articulo odisey\PROCES-SFRAMED\1.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_2_mandarin articulo odisey\PROCES-SFRAMED\2.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_2_mandarin articulo odisey\PROCES-SFRAMED\3.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_2_mandarin articulo odisey\PROCES-SFRAMED\4.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\KOPSTAL\kopstal_2_mandarin articulo odisey\PROCES-SFRAMED\5.png`
- `C:\Users\yigit\Desktop\RESSAMS\RESİMLER DETAY\INSTAGRAM\_sources\mandarin-full-photo-rectified.png`

Full-image derivative: original A0194 4284 × 5712; four physical canvas corners only, rectified to 3500 × 3500. No colour, contrast, synthetic reconstruction or artwork extension. Original source is unchanged. Reproducible corner data and original SHA-256 are saved locally in `INSTAGRAM/_sources/mandarin-source.json`. The 1890-square ready-framed painted stages keep their native pixels.

## Music mood suggestions

- Sparse instrumental jazz, dry percussion.
- Minimal electronic pulse around 120 BPM, no vocals.
- Restrained ambient texture.

Music is selected and added by Yiğit in Instagram; no audio has been embedded.

## Validation

```json
{
  "slug": "articulo-attack-on-mandarin",
  "type": "process",
  "duration": 4.5,
  "frames": 135,
  "video_only": true,
  "h264_1080x1920_30fps": true,
  "full_decode": true,
  "approved_preserved": false,
  "distinct_frames": 6,
  "expected_distinct_frames": 6,
  "distinct_count_matches": true
}
```

Renderer fixes: the original unbounded decoded-image cache and eager stage retention were replaced with one-source retention; identical static frames are reused. Encoder uses four threads to bound memory, keeping preset slow and CRF 17. A one-frame-early target interpolation was fixed: new detail renders now hold the final view for exactly 60 frames, not 61. Camera rejection rules are unchanged. Regression checks confirm diagonal motion, off-centre zoom, process motion and cropped process frames still fail, and unchanged frame geometry matches the original pixel-for-pixel. Approved historical videos are not modified by these fixes.

Visual review: the actual 15-frame encoded strip was inspected for the selected detail route, final complete-artwork fit and stage-only sequence; crop choices and exclusions are documented above. Original source photographs and Milano folders were not modified.
