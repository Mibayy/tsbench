# Token Savior — Benchmark Results v2.5.1
tsbench · 60 tâches · Claude Sonnet · Avril 2026

## Chiffres clés
- Précision : 56% → 96% (+40pts)
- Chars injectés : −84% (1.43M → 235K)
- Wall time : −45% (51s → 27.9s / tâche)
- 21 tâches impossibles sans TS
- 32 wins / 0 loses / 28 égalités

## Hero case — TASK-043
Baseline : 13 Read → 197K chars → 159s → score 1/2
Token Savior : 6×get_functions → 16K chars → 54s → score 2/2
−92% chars · −66% wall time · meilleur score

## Limites honnêtes
- Active tokens +29% (coût fixe MCP schema)
- Call_chain +88% wall time (navigation structurelle)
- Localisation simple +24% wall time

## Reproductibilité
github.com/Mibayy/tsbench — `python generate.py --seed 42`
