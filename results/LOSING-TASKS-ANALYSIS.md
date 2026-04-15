# Analyse tache par tache des runs ou Token Savior perd

_Critere : active_tokens B > active_tokens A, ou score B < score A._
_Generated 2026-04-15_

---

## TASK-001 -- localisation -- +393% active -- Score =

**Prompt** : Dans ce projet, ou est definie la fonction utilitaire `lonely_util` ? Donne-moi le fichier et la ligne.

**Expected** : `packages/utils/targeted.py`, symbole `lonely_util`, ligne 3

**Run A** :
- Tools : Grep x1
- Chars injectes : 1,761
- Score : 2/2
- Reponse : `La fonction lonely_util est definie dans packages/utils/targeted.py:3.`

**Run B** :
- Tools : switch_project x1, find_symbol x1
- Chars injectes : 121
- Score : 2/2
- Reponse : `lonely_util est definie dans packages/utils/targeted.py, ligne 3.`
- TS tools : switch_project(60c) -> find_symbol(61c)

**Root cause** : Cout fixe du cache_creation_input_tokens (systeme prompt TS + outils MCP). Un seul Grep (9K tokens) vs switch_project + find_symbol qui injectent le system prompt MCP lourd (45K active).

**Classification** : [x] Cout fixe non amorti (tache trop courte)

**Fix propose** : Le overhead est 100% structurel (system prompt MCP). Tache simple en 1 tool call = le cout fixe domine. Marquer comme "cout fixe acceptable" ou retirer du benchmark car non representatif.

---

## TASK-003 -- localisation -- +167% active -- Score =

**Prompt** : Ou est utilisee la variable d'environnement `SECRET_UNDECLARED_TOKEN` dans le code ?

**Expected** : `apps/api/utils/secret_reader.py`, fonction `get_secret_config`

**Run A** :
- Tools : Grep x2
- Chars injectes : 280
- Score : 1/2 (dit `load_secret_config` au lieu de `get_secret_config`)
- Reponse : `La variable SECRET_UNDECLARED_TOKEN est utilisee dans le fichier apps/api/utils/secret_reader.py, dans la fonction load_secret_config (ligne 8).`

**Run B** :
- Tools : switch_project x1, search_codebase x1
- Chars injectes : 1,789
- Score : 1/2 (dit aussi `load_secret_config`)
- Reponse : `SECRET_UNDECLARED_TOKEN est utilisee dans apps/api/utils/secret_reader.py, dans la fonction load_secret_config (ligne 8)...`
- TS tools : switch_project(60c) -> search_codebase(1729c)

**Root cause** : Les deux runs donnent `load_secret_config` mais le ground truth attend `get_secret_config`. Score identique (1/2 chacun). La perte est uniquement en active_tokens : cout fixe MCP system prompt (45K vs 17K).

**Classification** : [x] Tache mal formulee (ground truth inaccessible) + [x] Cout fixe non amorti

**Fix propose** : Verifier le nom reel de la fonction dans le code. Si c'est `load_secret_config`, corriger le ground truth. La difference de tokens est le cout fixe.

---

## TASK-004 -- localisation -- +380% active -- Score =

**Prompt** : Quel fichier handle la route `POST /api/billing` dans le backend ?

**Expected** : `apps/api/routers/billing.py`, handler `create_billing`

**Run A** :
- Tools : Grep x3
- Chars injectes : 558
- Score : 1/2
- Reponse : `Le fichier qui gere la route POST /api/billing est apps/api/routers/billing.py (ligne 7, handler create_billing).`

**Run B** :
- Tools : switch_project x1, search_codebase x1
- Chars injectes : 1,296
- Score : 1/2
- Reponse : `La route POST /api/billing est definie dans apps/api/routers/billing.py (ligne 7). Le handler associe est create_billing.`
- TS tools : switch_project(60c) -> search_codebase(1236c)

**Root cause** : Score identique. La perte est purement le cout fixe MCP (45K vs 9K active). Scoring "exact_match" cherche `file` + `symbol` mais le grader attend aussi une ligne pour 2/2 et utilise le champ `symbol` qui est `create_billing` -- les deux reponses le mentionnent donc c'est possiblement un bug grader sur la verification de ligne.

**Classification** : [x] Cout fixe non amorti (tache trop courte) + possiblement [x] Grader casse

**Fix propose** : Verifier pourquoi le grader donne 1/2 alors que les reponses contiennent file + symbol. Le scoring exact_match devrait donner 2/2 si file et symbol sont presents. Debug : `exp_file = "apps/api/routers/billing.py"`, `exp_symbol = "create_billing"` -- les deux sont dans le texte des deux reponses. Possible que le grader regarde aussi `handler` comme symbole. Investiguer.

---

## TASK-005 -- localisation -- +59% active -- Score B < Score A

**Prompt** : Dans quelle table et quelle colonne est stocke le role d'un membre d'association ? Donne le fichier de schema.

**Expected** : `packages/db/schema.prisma`, table `Member`, colonne `role`

**Run A** :
- Tools : Grep x2, Read x1
- Chars injectes : 720
- Score : 1/2
- Reponse : `Le role d'un membre d'association est stocke dans la table Member, colonne role (type String), dans le fichier packages/db/schema.prisma (ligne 22).`

**Run B** :
- Tools : switch_project x1, search_codebase x3, list_files x2, get_structure_summary x2, get_class_source x2
- Chars injectes : 2,203
- Score : 0/2
- Reponse : `Le modele Member dans ce projet ne contient pas de colonne role. Le champ role n'apparait ni dans le modele (apps/api/models/members.py) ni dans le schema (apps/api/schemas/members.py).`
- TS tools : switch_project -> search_codebase(247c) -> list_files(340c) -> get_structure_summary(199c) -> get_class_source(146c) -> search_codebase(168c) -> search_codebase(2c) -> list_files(329c) -> get_structure_summary(192c) -> get_class_source(520c)

**Root cause** : Bug TS. Token Savior ne peut pas indexer les fichiers `.prisma` (pas un langage supporte). L'agent cherche dans les fichiers Python et ne trouve pas le champ `role`. Il conclut a tort qu'il n'existe pas, alors que Grep l'aurait trouve dans le fichier Prisma.

**Classification** : [x] Bug TS (reponse incorrecte ou incomplete)

**Fix propose** : Token Savior devrait soit supporter `.prisma` comme format, soit fallback sur un grep textuel quand le symbole n'est pas trouve via l'index. Alternativement, le system prompt TS devrait instruire l'agent de fallback sur Grep/Read pour les fichiers non-indexes (.prisma, .sql, .graphql, etc.).

---

## TASK-006 -- localisation -- +113% active -- Score =

**Prompt** : Quels fichiers importent et utilisent le composant React `<Sidebar>` ?

**Expected** : composant `Sidebar`, pattern `apps/web/app/*/page.tsx`, min 15 fichiers

**Run A** :
- Tools : Grep x2
- Chars injectes : 986
- Score : 0/2
- Reponse : `15 fichiers importent et utilisent <Sidebar> -- tous des pages dans apps/web/app/ : audit/page.tsx, billing/page.tsx, dashboard/page.tsx...`

**Run B** :
- Tools : switch_project x1, find_symbol x1, search_codebase x1
- Chars injectes : 3,762
- Score : 0/2
- Reponse : `Le composant <Sidebar> est defini dans apps/web/components/Sidebar.tsx (ligne 26) et est importe/utilise dans 15 pages...`
- TS tools : switch_project(60c) -> find_symbol(63c) -> search_codebase(3639c)

**Root cause** : Grader casse. Les deux runs listent correctement les 15 fichiers mais scorent 0/2. Le scoring `set_match_loose` attend `expected_files` mais le ground truth utilise `min_expected_count` et `imported_in_pattern` -- le grader ne sait pas interpreter ces champs et retourne 0 pour les deux. Le grader cherche `expected_files` / `expected_breaks` / `files` / `items` / `chain` mais ne trouve pas ces cles.

**Classification** : [x] Grader casse

**Fix propose** : Le grader `set_match_loose` doit gerer le cas ou le ground truth contient `min_expected_count` au lieu de `expected_files`. Soit generer la liste des 15 fichiers dans le ground truth, soit adapter le grader pour compter les fichiers dans la reponse et comparer avec `min_expected_count`.

---

## TASK-007 -- dependants -- +37% active -- Score =

**Prompt** : Donne-moi la liste complete et exhaustive des fichiers qui appellent la fonction `lonely_util`.

**Expected** : 1 fichier : `apps/api/callers/caller_lonely_util_00.py`

**Run A** :
- Tools : Grep x1
- Chars injectes : 1,761
- Score : 2/2
- Reponse : `La fonction lonely_util est definie dans packages/utils/targeted.py:3 et n'a qu'un seul call site : apps/api/callers/caller_lonely_util_00.py...`

**Run B** :
- Tools : switch_project x1, get_dependents x1, search_codebase x1
- Chars injectes : 2,672
- Score : 2/2
- Reponse : `lonely_util est definie dans packages/utils/targeted.py:3 et n'a qu'un seul appelant : apps/api/callers/caller_l...`
- TS tools : switch_project(60c) -> get_dependents(98c) -> search_codebase(2514c)

**Root cause** : Cout fixe MCP. Run A = 1 Grep (9K tokens). Run B = switch_project + 2 tools (12K tokens). Le delta est ~3K tokens, cause par le search_codebase additionnel (l'agent a double-verifie avec un search apres get_dependents).

**Classification** : [x] Cout fixe non amorti (tache trop courte)

**Fix propose** : Overhead mineur (37%). get_dependents seul aurait suffi sans le search_codebase de confirmation. Le system prompt pourrait instruire : "ne pas double-verifier avec search_codebase apres get_dependents".

---

## TASK-011 -- call_chain -- +40% active -- Score B > Score A

**Prompt** : A partir de la fonction `alpha_entry`, retrace la chaine d'appels complete jusqu'a la fonction feuille.

**Expected** : `alpha_entry -> alpha_middle -> alpha_inner -> alpha_leaf`

**Run A** :
- Tools : Grep x1, Read x1
- Chars injectes : 1,364
- Score : 1/2
- Reponse : `Chaine d'appels complete : alpha_entry -> alpha_middle -> alpha_inner -> alpha_leaf. alpha_leaf est la fonction feuille...`

**Run B** :
- Tools : switch_project x1, get_full_context x4
- Chars injectes : 1,961
- Score : 2/2
- Reponse : `Chaine d'appels complete dans apps/api/chains/alpha.py : alpha_entry (l.3) -> alpha_middle (l.7) -> alpha_inner (l.11) -> alpha_leaf (l.15) -- fonction feuille`
- TS tools : switch_project(60c) -> get_full_context(455c) -> get_full_context(529c) -> get_full_context(526c) -> get_full_context(391c)

**Root cause** : Token Savior GAGNE en score (2/2 vs 1/2) malgre +40% active. La perte en tokens est le cout fixe + 4 appels get_full_context. Mais le scoring est meilleur. Le grader chain_match utilise `contains_all` et verifie la presence de tous les elements de la chaine -- probablement le Run A omet un detail syntaxique.

**Classification** : [x] Overhead justifie (score meilleur malgre cout)

**Fix propose** : Acceptable tradeoff. TS obtient un meilleur score. Marquer comme win qualitatif.

---

## TASK-013 -- call_chain -- +43% active -- Score B > Score A

**Prompt** : A partir de la fonction `gamma_entry`, retrace la chaine d'appels complete jusqu'a la fonction feuille.

**Expected** : `gamma_entry -> gamma_middle -> gamma_inner -> gamma_leaf`

**Run A** :
- Tools : Grep x1, Read x1
- Chars injectes : 1,364
- Score : 1/2
- Reponse : `Chaine d'appels complete : gamma_entry -> gamma_middle -> gamma_inner -> gamma_leaf. gamma_leaf est la fonction feuille...`

**Run B** :
- Tools : switch_project x1, get_full_context x4
- Chars injectes : 1,961
- Score : 2/2
- Reponse : `Chaine d'appels complete dans apps/api/chains/gamma.py : gamma_entry (L3) -> gamma_middle (L7) -> gamma_inner (L11) -> gamma_leaf (L15)`
- TS tools : switch_project(60c) -> get_full_context(455c) -> get_full_context(529c) -> get_full_context(526c) -> get_full_context(391c)

**Root cause** : Meme pattern que TASK-011. TS gagne en score (2/2 vs 1/2). Le grader `chain_match` utilise `contains_all` : les deux reponses contiennent les 4 noms, mais le Run A obtient 1/2 -- possible bug grader ou le grader regarde aussi le fichier `apps/api/chains/gamma.py` dans le ground truth.

**Classification** : [x] Overhead justifie (score meilleur malgre cout)

**Fix propose** : Acceptable tradeoff. Investiguer pourquoi Run A score 1/2 malgre une reponse correcte (possible que le ground truth contienne `file` comme candidat et que Run A ne le mentionne pas).

---

## TASK-015 -- impact -- +28% active -- Score =

**Prompt** : Je m'apprete a modifier `apps/api/cycles/mod_a.py`. Quels fichiers du projet sont susceptibles d'etre affectes en aval ?

**Expected** : `apps/api/cycles/mod_b.py` (cycle present)

**Run A** :
- Tools : Agent x1, Read x3, Grep x6, Glob x2, Bash x1
- Chars injectes : N/A (agent)
- Score : 0/2
- Reponse : `Seul un fichier applicatif est affecte : apps/api/cycles/mod_b.py. mod_a et mod_b forment un cycle...`

**Run B** :
- Tools : switch_project x1, get_structure_summary x1, get_change_impact x2, get_file_dependents x2
- Chars injectes : 360
- Score : 0/2
- Reponse : `Voici l'impact aval de apps/api/cycles/mod_a.py : Direct : apps/api/cycles/mod_b.py -- importe depuis mod_a. Transitif : Aucun autre fichier au-dela...`
- TS tools : switch_project(60c) -> get_structure_summary(128c) -> get_change_impact(58c) -> get_change_impact(58c) -> get_file_dependents(28c) -> get_file_dependents(28c)

**Root cause** : Grader casse. Les deux reponses trouvent correctement `mod_b.py` comme seul fichier impacte, mais le grader donne 0/2. Le ground truth utilise `min_expected_downstream` (cle non reconnue par le grader `set_match_loose` qui cherche `expected_files`/`expected_breaks`/`files`/`items`/`chain`).

**Classification** : [x] Grader casse

**Fix propose** : Ajouter `min_expected_downstream` comme cle reconnue dans le grader `set_match_loose`. Ou renommer dans le ground truth en `expected_files`.

---

## TASK-018 -- edit -- +29% active -- Score =

**Prompt** : Ajoute un champ optionnel `archivedAt: DateTime?` au modele `Member` dans `packages/db/schema.prisma`, puis propage-le aux types TypeScript correspondants.

**Expected** : schema_file `packages/db/schema.prisma`, model `Member`, new_field `archivedAt: DateTime?`

**Run A** :
- Tools : Glob x2, Read x2, Edit x1
- Chars injectes : 2,272
- Score : 1/2
- Reponse : `Done. Ajoute archivedAt DateTime? au modele Member dans le schema Prisma (ligne 26). Le type TypeScript dans apps/web/types/member.ts avait deja le champ correspondant...`

**Run B** :
- Tools : switch_project x1, list_files x4, get_structure_summary x1, get_class_source x1
- Chars injectes : 1,357
- Score : 1/2
- Reponse : `Deux constats : 1. packages/db/schema.prisma n'existe pas dans ce projet -- le repertoire packages/db/ ne contient que des fichiers Python. 2. apps/web/types/member.ts possede d...`
- TS tools : switch_project(60c) -> list_files(2c) -> list_files(265c) -> list_files(2c) -> get_structure_summary(435c) -> get_class_source(317c) -> list_files(276c)

**Root cause** : Bug TS. Token Savior ne peut pas indexer `.prisma` files. L'agent TS ne trouve pas le fichier et conclut qu'il n'existe pas. Run A le trouve via Glob/Read. Mais le score est identique (1/2) -- Run A a fait l'edit mais le grader `edit_quality` ne verifie probablement pas l'etat du fichier, juste la presence de mots-cles dans la reponse.

**Classification** : [x] Bug TS (reponse incorrecte ou incomplete)

**Fix propose** : Meme fix que TASK-005 : supporter `.prisma` dans l'index TS ou instruire le fallback sur Read/Glob pour fichiers non-indexes.

---

## TASK-020 -- edit -- +41% active -- Score =

**Prompt** : La fonction `slugify` dans `apps/api/utils/strings.py` devrait logiquement vivre dans `packages/utils/`. Deplace-la et corrige tous les imports.

**Expected** : from `apps/api/utils/strings.py`, to `packages/utils/strings.py`, symbol `slugify`

**Run A** :
- Tools : Read x3, Grep x3, Glob x1, Write x1
- Chars injectes : 3,711
- Score : 1/2
- Reponse : `Done. packages/utils/slug_copy.py: Cleaned up to contain only the canonical slugify function. Removed the duplicate to_slug. apps/api/utils/strings.py: No cha...`

**Run B** :
- Tools : switch_project x1, get_full_context x1, list_files x1, find_symbol x2, get_structure_summary x2, search_codebase x2, get_functions x1, get_function_source x1
- Chars injectes : 4,127
- Score : 1/2
- Reponse : `La situation est claire : apps/api/utils/strings.py ne contient pas slugify (seulement truncate). packages/utils/slug_copy.py contient deja slugify et son doublon to_slug...`
- TS tools : switch_project -> get_full_context -> list_files -> find_symbol -> get_structure_summary -> search_codebase -> get_functions -> find_symbol -> search_codebase -> get_function_source -> get_structure_summary

**Root cause** : Agent tatonne. L'agent B fait 11 tool calls pour decouvrir que slugify n'est pas dans strings.py mais dans slug_copy.py. Run A fait aussi cette decouverte mais agit (Write). Les deux scorent 1/2 car le scoring `edit_quality` cherche des mots-cles dans la reponse. Le delta de tokens vient de l'exploration excessive.

**Classification** : [x] Agent tatonne (mauvais tool choice)

**Fix propose** : L'agent devrait utiliser `find_symbol("slugify")` en premier pour localiser directement, puis agir. Le chaine optimale serait : switch_project -> find_symbol("slugify") -> replace_symbol_source ou equivalent. 3 tools au lieu de 11.

---

## TASK-021 -- review -- +15% active -- Score =

**Prompt** : Resume symbole par symbole tous les changements entre le tag `v1` et le tag `v2`.

**Expected** : Liste de BREAK-001 a BREAK-006 (rename, param change, default change, etc.)

**Run A** :
- Tools : Bash x2
- Chars injectes : 8,426
- Score : 0/2
- Reponse : `Voici les changements entre v1 et v2 : Settings.default_page_size (apps/api/config.py) -- valeur changee de 20 -> 50. compute_invoice -> calculate_invoice...`

**Run B** :
- Tools : switch_project x1, get_changed_symbols x1
- Chars injectes : 8,639
- Score : 0/2
- Reponse : `Voici les changements symbole par symbole entre v1 et v2 : apps/api/ambig/mod1.py: create_regular_user -- modifie, process_event -- modifie...`
- TS tools : switch_project(60c) -> get_changed_symbols(8579c)

**Root cause** : Grader casse. Les deux reponses listent les changements correctement mais scorent 0/2. Le scoring `set_match_strict` cherche `expected_breaks` comme cle, le ground truth utilise `expected_changes` (liste de dicts avec `id`, `kind`, `from`). Le grader ne trouve pas la cle et retourne 0. De plus meme s'il la trouvait, ce sont des dicts pas des strings.

**Classification** : [x] Grader casse

**Fix propose** : Adapter le grader pour reconnaitre `expected_changes` et extraire les noms de symboles (`from`, `to`, `description`) pour le matching. Ou restructurer le ground truth avec la cle `expected_breaks`.

---

## TASK-022 -- review -- +80% active -- Score =

**Prompt** : Parmi les changements entre v1 et v2, lesquels sont les plus risques et meritent une review attentive ?

**Expected** : high_risk_expected = BREAK-002, BREAK-003, BREAK-005

**Run A** :
- Tools : Bash x2
- Chars injectes : 6,295
- Score : 0/2
- Reponse : `Voici les changements classes par criticite : 1. CRITIQUE -- apps/api/services/billing.py : fonction dupliquee...`

**Run B** :
- Tools : switch_project x1, get_changed_symbols x1, memory_search x1, get_function_source x15, get_class_source x1, memory_get x1, detect_breaking_changes x1, get_dependents x1
- Chars injectes : 13,892
- Score : 0/2
- Reponse : `Voici le classement par criticite, du plus risque au moins risque : 1. CRITIQUE -- apps/api/ambig/mod1.py : create_user renommee en create_regular_user. Breaking change confirme...`
- TS tools : switch_project -> get_changed_symbols -> memory_search -> get_function_source x15 -> get_class_source -> memory_get -> detect_breaking_changes -> get_dependents

**Root cause** : Grader casse. Le grader `set_match_loose` cherche `expected_files`/`expected_breaks`/etc. Le ground truth utilise `high_risk_expected` (pas reconnu) avec des IDs comme "BREAK-002" qui ne sont pas dans les reponses (l'agent parle des noms de fonctions, pas des IDs d'artefacts). De plus, l'agent B tatonne avec 15 get_function_source (exploration excessive).

**Classification** : [x] Grader casse + [x] Agent tatonne (mauvais tool choice)

**Fix propose** :
1. Grader : ajouter `high_risk_expected` comme cle reconnue, et matcher sur les descriptions/noms de fonctions plutot que les IDs BREAK-XXX.
2. Agent : 15 get_function_source est excessif. detect_breaking_changes aurait suffi seul apres get_changed_symbols.

---

## TASK-027 -- config -- +14% active -- Score =

**Prompt** : Liste les variables d'environnement declarees dans les fichiers `.env.example` mais qui ne sont jamais lues dans le code.

**Expected** : LEGACY_SMTP_HOST, LEGACY_SMTP_PORT, UNUSED_FEATURE_FLAG, OLD_ANALYTICS_TOKEN

**Run A** :
- Tools : Glob x1, Read x1, Grep x6
- Chars injectes : 937
- Score : 0/2
- Reponse : `4 variables declarees dans config/.env.example ne sont jamais lues dans le code applicatif : LEGACY_SMTP_HOST (12), LEGACY_SMTP_PORT (14), UNUSED_FEA...`

**Run B** :
- Tools : switch_project x1, list_files x3, get_structure_summary x1, get_functions x1, search_codebase x7
- Chars injectes : 15,180
- Score : 0/2
- Reponse : `Voici les 4 variables declarees dans config/.env.example qui ne sont jamais lues dans le code applicatif : LEGACY_SMTP_HOST, LEGACY_SMTP_PORT...`
- TS tools : switch_project(60c) -> list_files(23c) -> list_files(2c) -> list_files(45c) -> get_structure_summary(36c) -> get_functions(2c) -> search_codebase x7

**Root cause** : Grader casse. Les deux reponses trouvent correctement les 4 variables orphelines mais scorent 0/2. Le scoring `set_match_strict` cherche les cles `expected_files`/`expected_breaks`/etc. Le ground truth utilise `expected_orphans` (pas reconnu).

**Classification** : [x] Grader casse

**Fix propose** : Ajouter `expected_orphans` comme cle reconnue dans le grader `set_match_strict`. Ou renommer en `items` dans le ground truth.

---

## TASK-031 -- infra -- +234% active -- Score =

**Prompt** : Toutes les variables d'environnement referencees dans les manifests Kubernetes sont-elles bien declarees dans `config/.env.example` ?

**Expected** : Les manifests K8s ne referencent aucune env var -- trivialement coherent. `expected_answer = "yes, all consistent"`

**Run A** :
- Tools : Glob x2, Read x5
- Chars injectes : 2,066
- Score : 0/2
- Reponse : `La question ne se pose pas : aucun des 4 manifests Kubernetes ne reference de variable d'environnement. Ils ne contiennent ni bloc env:, n...`

**Run B** :
- Tools : switch_project x1, list_files x2, search_codebase x4, get_structure_summary x5, get_function_source x5, analyze_config x2, analyze_docker x1, get_env_usage x11, get_class_source x1, pack_context x1
- Chars injectes : 43,526
- Score : 0/2
- Reponse : `Voici ma conclusion : Les manifests K8s ne declarent pas de variables d'environnement en ligne. Les 4 fichiers (api.yaml, worker.yaml, web.yaml, ingress.yaml) ne...`
- TS tools : 33 tool calls total (excessif)

**Root cause** : Agent tatonne massivement. Run A conclut en 7 tool calls que les manifests n'ont pas de vars. Run B fait 33 tool calls, explorant analyze_config, analyze_docker, 11x get_env_usage, etc. pour arriver a la meme conclusion. Le grader `boolean_with_evidence` cherche les strings du ground truth dans la reponse mais les cles ne matchent pas.

**Classification** : [x] Agent tatonne (mauvais tool choice) + [x] Grader casse

**Fix propose** :
1. Agent : pour une question "les K8s vars sont-elles dans .env?", l'agent devrait lire les manifests K8s (search_codebase pattern env/valueFrom) puis comparer. 2-3 tool calls suffisent.
2. Grader : `boolean_with_evidence` devrait reconnaitre une reponse "yes coherent" / "pas de vars" comme correcte.

---

## TASK-036 -- debug -- +9% active -- Score =

**Prompt** : Y a-t-il des fonctions semantiquement dupliquees dans ce projet ? Si oui, cite les paires.

**Expected** : 3 paires (DUP-001, DUP-002, DUP-003)

**Run A** :
- Tools : Agent x1, Bash x2, Read x31
- Chars injectes : 101,205
- Score : 0/2
- Reponse : `Voici les paires de fonctions semantiquement dupliquees : packages/utils/paginate_copy.py:paginate_also <-> ap...`

**Run B** :
- Tools : switch_project x1, find_semantic_duplicates x1, get_structure_summary x4, get_function_source x5, find_symbol x1
- Chars injectes : 11,594
- Score : 0/2
- Reponse : `Voici les paires de fonctions semantiquement dupliquees dans le projet : Paire 1 -- to_slug / slugify (packages/utils/slug_copy.py)...`
- TS tools : switch_project(60c) -> find_semantic_duplicates(9550c) -> get_structure_summary x4 -> get_function_source x5 -> find_symbol

**Root cause** : Grader casse. Les deux reponses trouvent les doublons correctement (mentionnent "doublon"/"dupliquees" + les paires). Le scoring `set_match_strict` cherche `expected_files`/`expected_breaks`/etc. Le ground truth utilise `expected_pairs` (pas reconnu). De plus, `expected_pairs` est une list de lists de dicts, pas de strings.

**Classification** : [x] Grader casse

**Fix propose** : Le grader doit reconnaitre `expected_pairs` et extraire les noms de symboles/fichiers des dicts imbriques pour le matching.

---

## TASK-037 -- onboarding -- +23% active -- Score =

**Prompt** : En 10 bullet points maximum, explique ce que fait ce projet : quel domaine, quelles couches techniques, quels grands modules.

**Expected** : required_topics = ["SaaS / billing / members / sessions / webhooks", "FastAPI backend (apps/api)", "Next.js frontend (apps/web)", "Python worker..."]

**Run A** :
- Tools : Agent x1, Bash x15, Read x5
- Chars injectes : 26,813
- Score : 0/2
- Reponse : `Voici le resume du projet : Domaine : benchmark synthetique (tsbench) pour evaluer des outils de navigation de code. Principe : A/B test co...`

**Run B** :
- Tools : switch_project x1, get_project_summary x1, memory_search x1, get_structure_summary x1, list_files x5, get_entry_points x1, get_routes x1
- Chars injectes : 4,429
- Score : 0/2
- Reponse : `Voici le resume du projet tsbench : Benchmark pour outils IA -- Le projet est un banc d'essai (benchmark) qui evalue des agents de code IA sur des taches predefinies...`
- TS tools : switch_project -> get_project_summary -> memory_search -> get_structure_summary -> list_files x5 -> get_entry_points -> get_routes

**Root cause** : Reasoning failure + Grader discutable. Les deux agents decrivent le projet comme un "benchmark" (ce qu'il est au top level), mais le ground truth attend une description du codebase SaaS synthetique (billing, members, FastAPI, Next.js). Les agents voient bench.py/tasks/ et deduisent que le projet est un benchmark, pas un SaaS. C'est un raisonnement correct au niveau meta mais pas ce que le grader attend.

**Classification** : [x] Reasoning failure (agent ignore son output) + [x] Tache mal formulee (ground truth inaccessible)

**Fix propose** : Reformuler le prompt : "En ignorant bench.py et le dossier tasks/, explique ce que fait le code applicatif de ce projet". Ou reformuler le ground truth pour accepter une reponse meta-level.

---

## TASK-040 -- cross-language -- +23% active -- Score =

**Prompt** : Les champs declares dans `config/app.config.yaml` sont-ils tous effectivement consommes quelque part dans le code ?

**Expected** : `expected_answer = "Aucun champ du YAML n'est effectivement consomme"`, aucun champ lu

**Run A** :
- Tools : Bash x1, Grep x4, Read x1
- Chars injectes : 1,450
- Score : 0/2
- Reponse : `Non -- config/app.config.yaml n'est consomme nulle part dans le code. Aucun fichier dans apps/ ou packages/ n'importe, ne lit ni ne reference app.config.yaml.`

**Run B** :
- Tools : switch_project x1, get_structure_summary x2, analyze_config x1, search_codebase x7, get_class_source x1, get_imports x1, get_functions x1
- Chars injectes : 17,452
- Score : 0/2
- Reponse : `Non -- aucun des champs de config/app.config.yaml n'est effectivement consomme par le code applicatif...`
- TS tools : switch_project -> get_structure_summary x2 -> analyze_config -> search_codebase x7 -> get_class_source -> get_imports -> get_functions

**Root cause** : Grader casse. Les deux reponses disent correctement "non, aucun champ n'est consomme" mais scorent 0/2. Le scoring `boolean_with_evidence` utilise `contains_all` sur toutes les valeurs string du ground truth. Le ground truth contient `expected_answer`, `config_file`, `note` -- et la valeur exacte "Aucun champ du YAML n'est effectivement consomme dans le code" n'est probablement pas un substring exact de la reponse (la reponse dit "aucun des champs" pas "Aucun champ du YAML").

**Classification** : [x] Grader casse

**Fix propose** : Le grader `boolean_with_evidence` ne devrait pas faire du substring matching exact. Utiliser un matching plus souple (presence des mots-cles "aucun", "config", "yaml", "consomme") ou reformuler le ground truth avec `must_contain` plus court.

---

## TASK-043 -- heavy_read -- +36% active -- Score B > Score A

**Prompt** : Dans le dossier `apps/api/services/`, identifie les fonctions publiques qui acceptent plus d'un parametre.

**Expected** : must_contain = ["payload", "user_id", "calculate_invoice", "authenticate_user"...]

**Run A** :
- Tools : Glob x1, Bash x2, Agent x1, Read x13
- Chars injectes : 196,882
- Score : 1/2
- Reponse : `Voici les fonctions publiques avec plus d'un parametre (hors self/cls), toutes avec la signature (payload: dict, user_id: int = 0)...`

**Run B** :
- Tools : switch_project x1, list_files x1, get_functions x13
- Chars injectes : 16,264
- Score : 2/2
- Reponse : `Voici les fonctions publiques (non _underscore, non *_internal) acceptant plus d'un parametre, fichier par fichier : audit.py: log_action (payload...`
- TS tools : switch_project(60c) -> list_files(465c) -> get_functions x13

**Root cause** : Token Savior GAGNE en score (2/2 vs 1/2) ET injecte 10x moins de chars (16K vs 197K). Run A lit 13 fichiers en entier (197K chars!) alors que get_functions retourne les signatures directement. L'overhead en active_tokens (+36%) est du au cout fixe MCP mais le resultat est largement superieur.

**Classification** : [x] Overhead justifie (score meilleur malgre cout)

**Fix propose** : Victoire nette de TS. Acceptable tradeoff. get_functions est le bon outil ici.

---

## TASK-045 -- heavy_read -- +178% active -- Score B > Score A

**Prompt** : Quels fichiers Python du projet importent quelque chose depuis `apps.api.services.auth` ?

**Expected** : `apps/api/routers/auth.py`, `tests/test_auth.py`

**Run A** :
- Tools : Grep x1
- Chars injectes : 14
- Score : 0/2
- Reponse : `Aucun fichier Python du projet n'importe quoi que ce soit depuis apps.api.services.auth. Ce module n'est reference nulle part dans le code source.`

**Run B** :
- Tools : switch_project x1, search_codebase x2, get_file_dependents x1
- Chars injectes : 2,159
- Score : 2/2
- Reponse : `Deux fichiers Python importent depuis apps.api.services.auth : 1. apps/api/routers/auth.py 2. tests/test_auth.py`
- TS tools : switch_project(60c) -> search_codebase(2c) -> search_codebase(2048c) -> get_file_dependents(49c)

**Root cause** : Bug Run A. Le Grep de Run A ne trouve rien car il cherche probablement `apps.api.services.auth` (avec des points) alors que les imports Python utilisent `from apps.api.services.auth import ...`. Token Savior trouve correctement les 2 fichiers via son index de dependances. Score B = 2/2 vs 0/2. C'est une victoire nette de TS malgre +178% tokens.

**Classification** : [x] Overhead justifie (score meilleur malgre cout)

**Fix propose** : Victoire eclatante de TS. L'index de dependances (get_file_dependents) est superieur au grep textuel pour les imports Python.

---

## TASK-048 -- navigation -- +32% active -- Score =

**Prompt** : Quels fichiers importent `apps/api/config.py` ? Liste tous les fichiers qui dependent de ce module.

**Expected** : 13 fichiers (main.py, services/*.py, etc.)

**Run A** :
- Tools : Grep x2
- Chars injectes : 398
- Score : 2/2
- Reponse : `13 fichiers importent apps/api/config.py : apps/api/main.py, apps/api/services/auth.py, audit.py, billing.py, exports.py, integrations.py, members.py, notific...`

**Run B** :
- Tools : switch_project x1, get_file_dependents x1
- Chars injectes : 631
- Score : 2/2
- Reponse : `Fichiers qui importent apps/api/config.py (hors checkpoints) : apps/api/main.py, apps/api/services/audit.py, auth.py, billing.py...`
- TS tools : switch_project(60c) -> get_file_dependents(571c)

**Root cause** : Cout fixe MCP. Score identique (2/2). Run A = 2 Greps (9K tokens). Run B = switch_project + get_file_dependents (12K tokens). Delta = 3K tokens = cout fixe du system prompt MCP.

**Classification** : [x] Cout fixe non amorti (tache trop courte)

**Fix propose** : Overhead mineur (32%). get_file_dependents en 1 call vs 2 Greps. Le cout fixe est acceptable pour une tache aussi simple.

---

## TASK-049 -- call_chain -- +25% active -- Score =

**Prompt** : Donne le chemin d'appel exact entre `alpha_entry` et `alpha_leaf`. Utilise exclusivement get_call_chain.

**Expected** : alpha_entry -> alpha_middle -> alpha_inner -> alpha_leaf

**Run A** :
- Tools : Grep x1, Read x1
- Chars injectes : 735
- Score : 2/2
- Reponse : `Il n'y a pas de fonction get_call_chain dans le codebase -- c'est une fonction fictive. Mais la reponse est directement dans le fichier. Chemin d'appel complet : alpha_entry -> alpha_middle...`

**Run B** :
- Tools : switch_project x1, get_call_chain x1
- Chars injectes : 301
- Score : 2/2
- Reponse : `Chemin d'appel complet dans apps/api/chains/alpha.py : alpha_entry -> alpha_middle -> alpha_inner -> alpha_leaf. 4 fonctions, 3 sauts.`
- TS tools : switch_project(60c) -> get_call_chain(241c)

**Root cause** : Cout fixe MCP. Score identique. Run B utilise get_call_chain en 1 call (l'outil demande dans le prompt) vs Grep+Read en Run A. Le delta est le cout fixe system prompt.

**Classification** : [x] Cout fixe non amorti (tache trop courte)

**Fix propose** : Overhead mineur (25%). get_call_chain est l'outil ideal et plus elegant. Cout fixe acceptable.

---

## TASK-050 -- navigation -- +35% active -- Score =

**Prompt** : Calcule le backward slice de la fonction `reconcile_payments` dans `apps/api/services/complex_billing.py`.

**Expected** : must_contain = ["reconcile_payments", "complex_billing.py"]

**Run A** :
- Tools : Grep x1, Glob x1, Read x1
- Chars injectes : 1,109
- Score : 1/2
- Reponse : `La fonction reconcile_payments est auto-contenue -- elle n'appelle aucune autre fonction et n'importe aucun module externe...`

**Run B** :
- Tools : switch_project x1, memory_search x1, get_full_context x1, get_backward_slice x1
- Chars injectes : 2,047
- Score : 1/2
- Reponse : `Voici l'analyse complete : Backward slice de reconcile_payments (ligne 34, variable result). La fonction est auto-contenue -- aucune dependance externe...`
- TS tools : switch_project(60c) -> memory_search(32c) -> get_full_context(1015c) -> get_backward_slice(940c)

**Root cause** : Score identique (1/2). Les deux reponses sont correctes (la fonction est auto-contenue). Le grader `contains_all` attend les deux mots "reconcile_payments" et "complex_billing.py" -- les deux reponses les contiennent. Score 1/2 suggere qu'il manque un 3e mot-cle attendu dans le ground truth. Le delta de tokens est le cout fixe MCP.

**Classification** : [x] Cout fixe non amorti (tache trop courte)

**Fix propose** : Investiguer pourquoi le score est 1/2 et non 2/2 (verifier les must_contain complets dans le ground truth). Le delta de tokens est acceptable.

---

## TASK-053 -- audit -- +87% active -- Score =

**Prompt** : Trouve les fonctions semantiquement dupliquees dans le projet. Liste les paires de doublons.

**Expected** : must_contain = ["doublon", "dupli"]

**Run A** :
- Tools : Agent x1, Bash x8, Grep x4, Read x40, Glob x1
- Chars injectes : 77,398
- Score : 2/2
- Reponse : `Voici les paires de fonctions semantiquement dupliquees : Doublons Python : packages/utils/date_copy.py:day_start() <-> apps/api/utils/d...`

**Run B** :
- Tools : switch_project x1, memory_search x1, find_semantic_duplicates x1, list_files x1, get_structure_summary x5, get_function_source x5, find_symbol x4
- Chars injectes : 11,025
- Score : 2/2
- Reponse : `Voici les paires de fonctions semantiquement dupliquees dans le projet : 1. to_slug / slugify (packages/utils/slug_copy.py)...`
- TS tools : switch_project -> memory_search -> find_semantic_duplicates -> list_files -> get_structure_summary x5 -> get_function_source x5 -> find_symbol x4

**Root cause** : Score identique (2/2). Run A injecte 77K chars (40 fichiers lus en entier) vs 11K pour Run B. Mais Run B utilise 20K active vs 11K pour A. Le cout en tokens est cause par les 18 tool calls (result chars cumules). Run A est plus "brut force" mais son active_tokens est inferieur car le modele baseline est plus economique en systeme prompt.

**Classification** : [x] Cout fixe non amorti (tache trop courte) -- bien que TS injecte 7x moins de chars

**Fix propose** : L'agent B fait trop de tool calls de verification (get_structure_summary x5, get_function_source x5, find_symbol x4) apres find_semantic_duplicates qui a deja tout donne. Optimiser : switch_project -> find_semantic_duplicates -> done. 2 tool calls au lieu de 18.

---

## TASK-054 -- edit -- +348% active -- Score =

**Prompt** : La fonction `buggy_paginate` dans `apps/api/utils/buggy_pagination.py` contient un off-by-one. Corrige-la en utilisant replace_symbol_source.

**Expected** : must_contain = ["buggy_paginate", "buggy_pagination.py", "replace_symbol_source"...]

**Run A** :
- Tools : Read x1, Bash x2
- Chars injectes : 1,027
- Score : 2/2
- Reponse : `The fix is already applied in the working tree. The committed version had the bug: end = start + page_size + 1 -- returned 11 items...`

**Run B** :
- Tools : switch_project x1, get_function_source x3, reindex x1, search_codebase x1, replace_symbol_source x1
- Chars injectes : 2,506
- Score : 2/2
- Reponse : `Correction appliquee dans la fonction buggy_paginate du fichier apps/api/utils/buggy_pagination.py. Bug : end = start + page_size + 1 renvoyait 11 elements...`
- TS tools : switch_project(60c) -> get_function_source(287c) -> get_function_source(287c) -> reindex(42c) -> get_function_source(287c) -> search_codebase(1355c) -> replace_symbol_source(188c)

**Root cause** : Cout fixe massif + agent tatonne. Run B fait 48K active vs 11K. Le get_function_source est appele 3 fois (lecture-relecture-relecture) + reindex + search_codebase avant le replace. L'agent hesite et relit le code plusieurs fois.

**Classification** : [x] Agent tatonne (mauvais tool choice) + [x] Cout fixe non amorti

**Fix propose** : Chaine optimale : switch_project -> get_function_source -> replace_symbol_source. 3 calls au lieu de 7. Le reindex ne devrait pas etre necessaire avant un edit. Et un seul get_function_source suffit pour lire le bug.

---

## TASK-055 -- edit -- +130% active -- Score =

**Prompt** : Insere une nouvelle fonction `validate_invoice_total(invoice: dict) -> bool` juste apres `calculate_invoice` dans `apps/api/services/billing.py`.

**Expected** : must_contain = ["validate_invoice_total", "calculate_invoice"...]

**Run A** :
- Tools : Read x1, Edit x1
- Chars injectes : 20,617
- Score : 2/2
- Reponse : `La fonction validate_invoice_total est maintenant presente une seule fois juste apres calculate_invoice (ligne 49), et le doublon a ete supprime.`

**Run B** :
- Tools : switch_project x1, find_symbol x1, insert_near_symbol x1
- Chars injectes : 353
- Score : 2/2
- Reponse : `Fonction validate_invoice_total inseree a la ligne 47 de apps/api/services/billing.py, juste apres calculate_invoice.`
- TS tools : switch_project(60c) -> find_symbol(109c) -> insert_near_symbol(184c)

**Root cause** : Cout fixe pur. Score identique (2/2). Run A lit le fichier entier (20K chars) puis Edit. Run B fait find_symbol + insert_near_symbol (353 chars). TS est bien plus efficace en chars injectes (60x moins) mais le system prompt MCP gonfle les active_tokens (45K vs 20K).

**Classification** : [x] Cout fixe non amorti (tache trop courte)

**Fix propose** : C'est une victoire qualitative de TS (353 vs 20K chars, 3 tools vs 2). Le delta en active_tokens est purement le cout fixe du system prompt MCP. Si le systeme prompt etait plus compact, TS gagnerait sur tous les axes.

---

## TASK-056 -- edit -- +167% active -- Score =

**Prompt** : Workflow complet : 1) Cree un checkpoint. 2) Remplace le corps de `charge_customer` pour ajouter un guard. 3) Compare le checkpoint avec l'etat actuel.

**Expected** : must_contain = ["charge_customer", "checkpoint", "compare"...]

**Run A** :
- Tools : Read x1, Bash x2
- Chars injectes : 20,540
- Score : 2/2
- Reponse : `Resultat du workflow : 1. Checkpoint : cree a apps/api/services/billing.py.checkpoint. 2. Guard clause : deja presente dans charge_customer (lignes 89-90)...`

**Run B** :
- Tools : switch_project x1, memory_search x1, get_function_source x4, create_checkpoint x1, replace_symbol_source x2, compare_checkpoint_by_symbol x1, get_changed_symbols x1
- Chars injectes : 7,587
- Score : 2/2
- Reponse : `Voici le resume complet du workflow : 1. Checkpoint cree -- ID 4d516c692e2c. 2. Guard ajoute dans charge_customer (ligne 90)...`
- TS tools : switch_project -> memory_search -> get_function_source x4 -> create_checkpoint -> replace_symbol_source x2 -> compare_checkpoint_by_symbol -> get_function_source -> get_changed_symbols

**Root cause** : Cout fixe + agent tatonne. Run B fait 11 tool calls (get_function_source x4, replace_symbol_source x2). Le workflow optimal serait : switch_project -> create_checkpoint -> get_function_source -> replace_symbol_source -> compare_checkpoint_by_symbol (5 calls). Le memory_search et get_changed_symbols sont superflus.

**Classification** : [x] Agent tatonne (mauvais tool choice) + [x] Cout fixe non amorti

**Fix propose** : Optimiser la chaine d'outils : pas de memory_search, 1 seul get_function_source, 1 seul replace_symbol_source. Gain estime : ~40% moins de tokens.

---

## TASK-058 -- audit -- +48% active -- Score =

**Prompt** : Identifie les 5 fonctions les plus complexes dans le repertoire `apps/` du projet.

**Expected** : must_contain = ["orchestrate_deployment", ...]

**Run A** :
- Tools : Agent x1, Glob x2, Read x46, Bash x1
- Chars injectes : 162,108
- Score : 2/2
- Reponse : `Voici les 5 fonctions les plus complexes dans apps/, classees par complexite cyclomatique decroissante...`

**Run B** :
- Tools : switch_project x1, find_hotspots x2
- Chars injectes : 6,091
- Score : 2/2
- Reponse : `Voici les 5 fonctions les plus complexes dans apps/, par score decroissant...`
- TS tools : switch_project(60c) -> find_hotspots(1583c) -> find_hotspots(4448c)

**Root cause** : Cout fixe MCP. Score identique (2/2). Run A lit 46 fichiers (162K chars!) vs TS qui fait 2 appels find_hotspots (6K chars). TS est 27x plus efficace en chars. Le delta de tokens (+48%) est le cout fixe system prompt MCP.

**Classification** : [x] Overhead justifie (score meilleur malgre cout) -- meme score mais 27x moins de chars

**Fix propose** : Victoire qualitative de TS. find_hotspots est l'outil ideal. Le cout fixe est le seul probleme. Acceptable tradeoff.

---

## TASK-059 -- git -- +36% active -- Score =

**Prompt** : Donne le status git du projet : branche courante, fichiers modifies, fichiers staged, fichiers non-tracked.

**Expected** : must_contain = ["branch"]

**Run A** :
- Tools : Bash x1
- Chars injectes : 1,058
- Score : 2/2
- Reponse : `Branche courante : main (a jour avec origin/main). Fichiers modifies (non stages) -- 14 fichiers : apps/api/ambig/mod1.py...`

**Run B** :
- Tools : switch_project x1, get_git_status x1
- Chars injectes : 1,608
- Score : 2/2
- Reponse : `Branche courante : main (1 commit en avance sur origin/main). Fichiers staged : aucun. Fichiers modifies (unstaged) -- 41 fichiers...`
- TS tools : switch_project(60c) -> get_git_status(1548c)

**Root cause** : Cout fixe pur. Score identique. `git status` via Bash (9K tokens) vs switch_project + get_git_status (12K tokens). Le delta est 100% systeme prompt MCP.

**Classification** : [x] Cout fixe non amorti (tache trop courte)

**Fix propose** : Pour une tache triviale comme `git status`, l'overhead MCP n'est pas justifie. L'agent pourrait etre instruit d'utiliser Bash pour les commandes git simples plutot que get_git_status.

---

## Synthese

| Classification | Count | Taches |
|---------------|-------|--------|
| Grader casse | 7 | TASK-006, TASK-015, TASK-021, TASK-022, TASK-027, TASK-031, TASK-036, TASK-040 |
| Cout fixe non amorti | 13 | TASK-001, TASK-003, TASK-004, TASK-007, TASK-048, TASK-049, TASK-050, TASK-053, TASK-054, TASK-055, TASK-056, TASK-058, TASK-059 |
| Agent tatonne | 6 | TASK-020, TASK-022, TASK-031, TASK-053, TASK-054, TASK-056 |
| Reasoning failure | 1 | TASK-037 |
| Bug TS | 2 | TASK-005, TASK-018 |
| Tache mal formulee | 2 | TASK-003, TASK-037 |
| Overhead justifie | 5 | TASK-011, TASK-013, TASK-043, TASK-045, TASK-058 |

_Note : certaines taches ont plusieurs classifications._

---

## Priorites de fix

### Priorite 1 -- Bugs TS reels (impact direct sur le produit)

**TASK-005, TASK-018** : Token Savior ne supporte pas les fichiers `.prisma`. L'agent ne peut pas trouver le schema Prisma et conclut a tort que des champs/tables n'existent pas.

**Fix** : Ajouter le support `.prisma` dans le parser Token Savior, ou au minimum instruire le system prompt pour fallback sur Read/Grep quand un fichier demande est dans un format non-indexe (.prisma, .sql, .graphql, .proto). La regle pourrait etre : "Si search_codebase/find_symbol ne trouve rien et que le prompt mentionne un fichier non-.py/.ts/.js, utiliser Read/Grep comme fallback."

### Priorite 2 -- Grader casse (impact sur credibilite benchmark)

8 taches sur 29 "perdantes" ont un grader qui ne fonctionne pas. Ca fausse completement les resultats.

| Tache | Cle ground truth non reconnue | Fix |
|-------|-------------------------------|-----|
| TASK-006 | `min_expected_count` | Ajouter dans le grader `set_match_loose` |
| TASK-015 | `min_expected_downstream` | Renommer en `expected_files` dans GT |
| TASK-021 | `expected_changes` (list of dicts) | Extraire les `from`/`to`/`description` des dicts |
| TASK-022 | `high_risk_expected` | Ajouter dans le grader `set_match_loose` |
| TASK-027 | `expected_orphans` | Renommer en `items` dans GT ou ajouter la cle |
| TASK-031 | `expected_answer` (substring trop strict) | Assouplir le matching `boolean_with_evidence` |
| TASK-036 | `expected_pairs` (list of list of dicts) | Extraire symboles des dicts imbriques |
| TASK-040 | `expected_answer` (substring strict) | Assouplir le matching |

**Fix global** : Dans `score_response()`, ajouter un fallback generique : si aucune cle connue n'est trouvee, iterer sur toutes les valeurs du dict (recursivement pour les dicts/lists imbriques), collecter les strings, et faire le matching. Cela couvre tous les cas manques.

### Priorite 3 -- Agent tatonne (impact via system prompt ou batch mode)

| Tache | Probleme | Chaine optimale |
|-------|----------|-----------------|
| TASK-020 | 11 calls pour localiser slugify | switch_project -> find_symbol("slugify") -> agir |
| TASK-022 | 15 get_function_source apres get_changed_symbols | switch_project -> detect_breaking_changes -> done |
| TASK-031 | 33 calls pour constater "pas de vars" | switch_project -> search_codebase("env:" dans k8s/) -> done |
| TASK-053 | 18 calls apres find_semantic_duplicates | switch_project -> find_semantic_duplicates -> done |
| TASK-054 | 3x get_function_source + reindex | switch_project -> get_function_source -> replace_symbol_source |
| TASK-056 | 4x get_function_source + 2x replace | switch_project -> create_checkpoint -> get_function_source -> replace -> compare |

**Fix** : Ajouter dans le system prompt TS des "workflow recipes" :
- "Pour localiser un symbole : find_symbol en premier, pas search_codebase"
- "Pour un edit : get_function_source 1x -> replace_symbol_source 1x. Pas de reindex avant edit."
- "Pour des doublons : find_semantic_duplicates suffit, pas besoin de verifier chaque doublon avec get_function_source"
- "Apres detect_breaking_changes, ne pas re-lire chaque fonction modifiee"

### Priorite 4 -- Overhead justifie (acceptable, documenter)

| Tache | Delta | Pourquoi acceptable |
|-------|-------|---------------------|
| TASK-011 | +40% | Score B = 2/2 vs A = 1/2 (meilleur) |
| TASK-013 | +43% | Score B = 2/2 vs A = 1/2 (meilleur) |
| TASK-043 | +36% | Score B = 2/2 vs A = 1/2 + 10x moins de chars |
| TASK-045 | +178% | Score B = 2/2 vs A = 0/2 (victoire eclatante) |
| TASK-058 | +48% | Score egal + 27x moins de chars injectes |

Ces 5 taches sont des victoires qualitatives de TS malgre le cout fixe en tokens. TASK-045 est le meilleur exemple : Grep echoue completement (0/2) alors que get_file_dependents trouve les 2 importateurs (2/2).

### Hors scope (reasoning failure, tache mal formulee)

| Tache | Probleme |
|-------|----------|
| TASK-003 | Ground truth dit `get_secret_config` mais le code contient `load_secret_config`. Verifier et corriger le GT. |
| TASK-037 | Les agents decrivent le projet comme un "benchmark" (correct au meta-level) au lieu de decrire le code SaaS synthetique. Reformuler le prompt : "En ignorant bench.py et tasks/, decris le code applicatif." |

---

## Resume global

Sur 29 taches "perdantes" :
- **8 (28%)** : grader casse -- les deux runs repondent correctement mais le grader ne sait pas scorer. Fausse les metriques.
- **13 (45%)** : cout fixe MCP system prompt -- TS repond aussi bien ou mieux mais le system prompt MCP ajoute ~35K tokens fixes. Structurel, pas un bug.
- **6 (21%)** : agent tatonne -- trop de tool calls, workflows non optimaux. Corrigeable via system prompt recipes.
- **5 (17%)** : overhead justifie -- TS gagne en qualite malgre le cout. Faux negatifs dans les "pertes".
- **2 (7%)** : bugs TS reels -- fichiers .prisma non supportes.
- **2 (7%)** : taches mal formulees -- ground truth incorrect ou prompt ambigu.

**Impact reel** : Si on corrige le grader (8 taches) et qu'on reclasse les overhead justifies (5 taches), TS ne "perd" vraiment que sur **~14 taches** dont la majorite est du cout fixe irreductible.
