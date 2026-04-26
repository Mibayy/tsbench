#!/bin/bash
# Smoke test — 10 tasks × run both (A + B) pour valider pipeline bout-en-bout
# Couverture : exact_match, set_match_loose, contains_all, llm_judge (Sonnet)

set -u
cd "$(dirname "$0")/.."

TASKS=(
  "TASK-001"  # navigation exact_match
  "TASK-024"  # audit set_match_loose
  "TASK-061"  # explanation llm_judge
  "TASK-062"  # code_gen contains_all
  "TASK-063"  # bug_fix contains_all
  "TASK-069"  # code_gen contains_all (pagination)
  "TASK-081"  # bug_fix contains_all (off-by-one)
  "TASK-095"  # writing_tests contains_all
  "TASK-102"  # explanation llm_judge
  "TASK-106"  # documentation llm_judge
)

LOG="results/smoke-$(date +%Y%m%d-%H%M%S).log"
mkdir -p results
echo "[SMOKE] Starting at $(date)" | tee "$LOG"
echo "[SMOKE] Tasks: ${#TASKS[@]} × runs A+B = $((${#TASKS[@]}*2)) invocations" | tee -a "$LOG"

START=$(date +%s)
for i in "${!TASKS[@]}"; do
  T="${TASKS[$i]}"
  echo "[SMOKE] [$((i+1))/${#TASKS[@]}] Running $T with --run both..." | tee -a "$LOG"
  python3 bench.py --tasks "$T" --run both --force 2>&1 | tee -a "$LOG"
  echo "[SMOKE] $T done at $(date)" | tee -a "$LOG"
done

END=$(date +%s)
echo "[SMOKE] Complete. Wall time: $((END-START))s" | tee -a "$LOG"
echo "[SMOKE] Results in: results/raw/" | tee -a "$LOG"
echo "[SMOKE] Log: $LOG" | tee -a "$LOG"
