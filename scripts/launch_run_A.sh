#!/bin/bash
# Launched by `at` — runs full bench (90 tasks) pour Run A uniquement
set -u
cd /root/projects/tsbench

STAMP=$(date +%Y%m%d-%H%M%S)
LOG="results/run-A-full-${STAMP}.log"
mkdir -p results

{
  echo "[RUN-A] Start: $(date)"
  echo "[RUN-A] Host: $(hostname)"
  python3 bench.py --tasks all --run A --force
  echo "[RUN-A] End: $(date)"
} >"$LOG" 2>&1
