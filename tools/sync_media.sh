#!/usr/bin/env bash
# Copy every reel (full quality, untouched) into the media repo next to this
# one, keeping the posts/... paths that index.html links to, then commit there.
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
media="${1:-$here/../insta-media}"
cd "$here"
git ls-files 'posts/*.mp4' 'posts/**/*.mp4' | sort -u | while read -r f; do
  mkdir -p "$media/$(dirname "$f")"
  cmp -s "$f" "$media/$f" || cp "$f" "$media/$f"
done
touch "$media/.nojekyll"
echo "synced to $media"
