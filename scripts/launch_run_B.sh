#!/bin/bash
# Full bench (90 tasks) pour Run B uniquement (token-savior MCP)
set -u
cd /root/projects/tsbench

STAMP=$(date +%Y%m%d-%H%M%S)
LOG="results/run-B-full-${STAMP}.log"
mkdir -p results

{
  echo "[RUN-B] Start: $(date)"
  echo "[RUN-B] Host: $(hostname)"
  # Default workers=2 — empirically 4 caused MCP server boot races on parallel
  # subprocess starts (TASK-012..015 saw "tools not exposed" errors). Two
  # workers stays safe and still gives ~3x parallel speedup on long-tail tasks.
  python3 bench.py --tasks all --run B --force --workers "${TSBENCH_WORKERS:-2}"
  echo "[RUN-B] End: $(date)"
} >"$LOG" 2>&1
