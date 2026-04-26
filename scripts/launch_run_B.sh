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
  python3 bench.py --tasks all --run B --force
  echo "[RUN-B] End: $(date)"
} >"$LOG" 2>&1
