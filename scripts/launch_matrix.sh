#!/bin/bash
# Launch the 5 remaining configs for the 6-config matrix benchmark.
#
# Assumes Opus/A (opus-base) and Opus/B (opus-ts) are already in results/raw/.
# Splits them into raw-opus-base/ and raw-opus-ts/, then runs the 5 remaining
# configs sequentially, moving raw/ into raw-{config_id}/ after each.
#
# Each config is a (model, run_letter) pair. bench.py selects the model via
# TSBENCH_MODEL and the mode via --run (A=base, B=ts).
#
# Logs: results/matrix-{config_id}-{stamp}.log
# Rebuild matrix.json after each config so partial progress is visible.

set -u
cd /root/projects/tsbench

RAW=results/raw
STAMP_RUN=$(date +%Y%m%d-%H%M%S)
MASTER_LOG="results/matrix-master-${STAMP_RUN}.log"

log() {
    echo "[launch_matrix $(date +%H:%M:%S)] $*" | tee -a "$MASTER_LOG"
}

archive_current_raw() {
    # Split whatever is currently in raw/ (Opus A + B mixed) into per-config
    # dirs. Idempotent: skipped if both target dirs already exist and are
    # non-empty.
    local base_dir="results/raw-opus-base"
    local ts_dir="results/raw-opus-ts"
    if [ -d "$base_dir" ] && [ -n "$(ls -A "$base_dir" 2>/dev/null)" ] \
       && [ -d "$ts_dir" ] && [ -n "$(ls -A "$ts_dir" 2>/dev/null)" ]; then
        log "opus-base and opus-ts already archived, skip split"
        return 0
    fi
    mkdir -p "$base_dir" "$ts_dir"
    local moved_a=0 moved_b=0
    for f in "$RAW"/TASK-*-run-A.json; do
        [ -e "$f" ] || continue
        local tid=$(basename "$f" | sed 's/-run-A\.json$//')
        mv "$f" "$base_dir/${tid}.json"
        moved_a=$((moved_a + 1))
    done
    for f in "$RAW"/TASK-*-run-B.json; do
        [ -e "$f" ] || continue
        local tid=$(basename "$f" | sed 's/-run-B\.json$//')
        mv "$f" "$ts_dir/${tid}.json"
        moved_b=$((moved_b + 1))
    done
    log "archived opus: $moved_a -> raw-opus-base, $moved_b -> raw-opus-ts"
}

move_raw_to_config() {
    local config_id=$1
    local run_letter=$2
    local dest="results/raw-${config_id}"
    mkdir -p "$dest"
    local moved=0
    for f in "$RAW"/TASK-*-run-${run_letter}.json; do
        [ -e "$f" ] || continue
        local tid=$(basename "$f" | sed "s/-run-${run_letter}\.json$//")
        mv "$f" "$dest/${tid}.json"
        moved=$((moved + 1))
    done
    log "archived $moved raw files -> $dest"
}

run_config() {
    local config_id=$1
    local model=$2
    local run_letter=$3
    local dest="results/raw-${config_id}"

    if [ -d "$dest" ] && [ "$(ls -A "$dest" 2>/dev/null | wc -l)" -gt 0 ]; then
        log "SKIP $config_id (already archived in $dest)"
        return 0
    fi

    local stamp=$(date +%Y%m%d-%H%M%S)
    local log_file="results/matrix-${config_id}-${stamp}.log"

    log "START $config_id  model=$model run=$run_letter  log=$log_file"
    {
        echo "[$config_id] Start: $(date)"
        echo "[$config_id] Model: $model"
        echo "[$config_id] Run:   $run_letter"
        TSBENCH_MODEL="$model" python3 bench.py --tasks all --run "$run_letter" --force
        echo "[$config_id] End:   $(date)"
    } >"$log_file" 2>&1
    local rc=$?
    log "END   $config_id rc=$rc"

    move_raw_to_config "$config_id" "$run_letter"

    log "rebuild matrix.json"
    python3 scripts/build_matrix.py >>"$MASTER_LOG" 2>&1 || log "build_matrix failed (non-fatal)"

    return $rc
}

log "=== matrix launch start ==="
archive_current_raw

# Rebuild once up front so matrix.json reflects the Opus runs alone.
python3 scripts/build_matrix.py >>"$MASTER_LOG" 2>&1 || log "initial build_matrix failed"

# 5 remaining configs. Sonnet first (cheaper, shorter feedback), then Haiku.
run_config "sonnet-base" "claude-sonnet-4-6"         "A"
run_config "sonnet-ts"   "claude-sonnet-4-6"         "B"
run_config "haiku-base"  "claude-haiku-4-5-20251001" "A"
run_config "haiku-ts"    "claude-haiku-4-5-20251001" "B"

# The 6th config (opus-ts vs opus-base) is already archived by archive_current_raw.
# If opus-base is missing for any reason, uncomment to run it:
# run_config "opus-base" "claude-opus-4-7" "A"

log "=== matrix launch done ==="
log "master log: $MASTER_LOG"
log "matrix.json: results/matrix.json"
