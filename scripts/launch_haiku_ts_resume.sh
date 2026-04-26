#!/bin/bash
# Resume Haiku-TS bench: 16 tasks already in results/raw/, run remaining 74 without --force.
set -u
cd /root/projects/tsbench

STAMP=$(date +%Y%m%d-%H%M%S)
LOG="results/matrix-haiku-ts-resume-${STAMP}.log"
DEST="results/raw-haiku-ts"
mkdir -p results "$DEST"

{
  echo "[haiku-ts-resume] Start: $(date)"
  echo "[haiku-ts-resume] Model: claude-haiku-4-5-20251001"
  TSBENCH_MODEL="claude-haiku-4-5-20251001" python3 bench.py --tasks all --run B
  rc=$?
  echo "[haiku-ts-resume] bench rc=$rc"

  echo "[haiku-ts-resume] archiving raw/ -> $DEST"
  moved=0
  for f in results/raw/TASK-*-run-B.json; do
    [ -e "$f" ] || continue
    mv "$f" "$DEST/$(basename "$f")"
    moved=$((moved + 1))
  done
  echo "[haiku-ts-resume] archived $moved files"

  echo "[haiku-ts-resume] rebuild matrix.json"
  python3 scripts/build_matrix.py
  echo "[haiku-ts-resume] End: $(date)"
} >"$LOG" 2>&1
echo "log: $LOG"
