#!/usr/bin/env bash
set -euo pipefail

# Insert YAML front matter date for .md and .qmd files if missing.
# - Adds 'date: YYYY-MM-DD' in existing front matter, or creates a new block.
# - Skips files in docs/ and .github/, and README.md.

DATE="$(TZ=Asia/Tokyo date +%Y-%m-%d)"

mapfile -t FILES < <(git ls-files '*.md' '*.qmd' | grep -vE '^(docs/|\.github/)' | grep -vE '^README\.md$')

changed=0
for f in "${FILES[@]}"; do
  # Skip empty or binary-like files
  if [ ! -s "$f" ]; then
    continue
  fi

  # Detect if file already has date in front matter
  # Consider only the first front matter block if present
  if head -n 1 "$f" | grep -qx '---'; then
    # Extract front matter block (until next ---) and check for date:
    if awk 'BEGIN{inblock=0}
      NR==1 && $0=="---"{inblock=1; next}
      inblock && $0=="---"{inblock=0; exit}
      inblock && $0 ~ /^date:/{found=1}
      END{exit found?0:1}' "$f" ; then
      # date exists -> skip
      continue
    fi
    # Insert date as the second line (after opening ---)
    tmp="$(mktemp)"
    awk -v d="$DATE" 'NR==1 && $0=="---"{print; print "date: " d; next} {print}' "$f" > "$tmp"
    mv "$tmp" "$f"
    changed=1
  else
    # No front matter -> prepend a new one
    tmp="$(mktemp)"
    {
      echo '---'
      echo "date: $DATE"
      echo '---'
      echo
      cat "$f"
    } > "$tmp"
    mv "$tmp" "$f"
    changed=1
  fi
done

if [ "$changed" -eq 0 ]; then
  echo "No date insertions needed."
else
  echo "Inserted date front matter where missing."
fi


