#!/bin/bash
set -u
cd /root/projects/tsbench

STAMP=$(date +%Y%m%d-%H%M%S)
LOG="results/v27-sample-${STAMP}.log"
DEST="results/raw-haiku-ts-v27-sample"
mkdir -p "$DEST"

TASKS=(TASK-001 TASK-004 TASK-022 TASK-027 TASK-031 TASK-045 TASK-050 TASK-053 TASK-054 TASK-055 TASK-056 TASK-058)

{
  echo "[v27-sample] Start: $(date)"
  for tid in "${TASKS[@]}"; do
    echo "[v27-sample] Running $tid ..."
    TSBENCH_MODEL="claude-haiku-4-5-20251001" python3 bench.py --tasks "$tid" --run B --force
    rc=$?
    echo "[v27-sample] $tid rc=$rc"
    src="results/raw/${tid}-run-B.json"
    if [ -e "$src" ]; then
      mv "$src" "$DEST/${tid}.json"
      echo "[v27-sample] archived $tid"
    else
      echo "[v27-sample] WARN: $src missing"
    fi
  done
  echo "[v27-sample] End: $(date)"
} >"$LOG" 2>&1
echo "$LOG"
