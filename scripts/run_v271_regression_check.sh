#!/bin/bash
set -u
cd /root/projects/tsbench

STAMP=$(date +%Y%m%d-%H%M%S)
LOG="results/v271-regcheck-${STAMP}.log"
DEST="results/raw-haiku-ts-v271-regcheck"
mkdir -p "$DEST"

TASKS=(TASK-001 TASK-004 TASK-027 TASK-058 TASK-045 TASK-050)

{
  echo "[v271] Start: $(date)"
  for tid in "${TASKS[@]}"; do
    echo "[v271] Running $tid ..."
    TSBENCH_MODEL="claude-haiku-4-5-20251001" python3 bench.py --tasks "$tid" --run B --force
    src="results/raw/${tid}-run-B.json"
    [ -e "$src" ] && mv "$src" "$DEST/${tid}.json" && echo "[v271] archived $tid"
  done
  echo "[v271] End: $(date)"
} >"$LOG" 2>&1
echo "$LOG"
