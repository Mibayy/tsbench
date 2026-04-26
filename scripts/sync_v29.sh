#!/bin/bash
# Sync v2.9 bench results: backup raw-opus-ts, replace, regen matrix, copy to docs.
# Usage: bash scripts/sync_v29.sh
set -e

cd /root/projects/tsbench

echo "==> Backup raw-opus-ts (prev 21/04 snapshot)"
if [ ! -d results/raw-opus-ts-prev-21042026 ]; then
    cp -r results/raw-opus-ts results/raw-opus-ts-prev-21042026
    echo "    backed up to raw-opus-ts-prev-21042026"
else
    echo "    backup already exists, skipping"
fi

echo "==> Copy raw/TASK-XXX-run-B.json -> raw-opus-ts/TASK-XXX.json (drop -run-B)"
rm -f results/raw-opus-ts/TASK-*.json
for f in results/raw/TASK-*-run-B.json; do
    base=$(basename "$f" -run-B.json)
    cp "$f" "results/raw-opus-ts/${base}.json"
done
echo "    raw-opus-ts now has $(ls results/raw-opus-ts/TASK-*.json | wc -l) files"

echo "==> Regenerate matrix.json"
python3 scripts/build_matrix.py

echo "==> Sync matrix.json to token-savior/docs/"
cp results/matrix.json /root/token-savior/docs/matrix.json

echo "==> Done. matrix.json updated:"
python3 -c "
import json
m=json.load(open('results/matrix.json'))
for cid in ['opus-base','opus-ts','sonnet-base','sonnet-ts','haiku-base','haiku-ts']:
    s=m['summary'][cid]
    print(f'  {cid:14s} score={s[\"score_total\"]}/{s[\"score_max_total\"]} ({s[\"score_pct\"]}%)  active_mean={s[\"active_tokens_mean\"]:.0f}')
"
