#!/bin/bash
# Run B (token-savior MCP) with Haiku 4.5 — the only missing config in the 6-config matrix.
set -u
cd /root/projects/tsbench

STAMP=$(date +%Y%m%d-%H%M%S)
LOG="results/matrix-haiku-ts-${STAMP}.log"
DEST="results/raw-haiku-ts"
mkdir -p results "$DEST"

{
  echo "[haiku-ts] Start: $(date)"
  echo "[haiku-ts] Model: claude-haiku-4-5-20251001"
  TSBENCH_MODEL="claude-haiku-4-5-20251001" python3 bench.py --tasks all --run B --force
  rc=$?
  echo "[haiku-ts] bench rc=$rc"

  echo "[haiku-ts] archiving raw/ -> $DEST"
  moved=0
  for f in results/raw/TASK-*-run-B.json; do
    [ -e "$f" ] || continue
    tid=$(basename "$f" | sed 's/-run-B\.json$//')
    mv "$f" "$DEST/${tid}.json"
    moved=$((moved + 1))
  done
  echo "[haiku-ts] archived $moved files"

  echo "[haiku-ts] rebuild matrix.json"
  python3 scripts/build_matrix.py
  echo "[haiku-ts] End: $(date)"
} >"$LOG" 2>&1
