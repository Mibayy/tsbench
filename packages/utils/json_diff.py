def json_diff(a: dict, b: dict) -> dict:
    added: dict = {}
    removed: dict = {}
    changed: dict = {}

    for key in b:
        if key not in a:
            added[key] = b[key]

    for key in a:
        if key not in b:
            removed[key] = a[key]

    for key in a:
        if key not in b:
            continue
        av, bv = a[key], b[key]
        if isinstance(av, dict) and isinstance(bv, dict):
            sub = json_diff(av, bv)
            for sk, sv in sub["added"].items():
                added[f"{key}.{sk}"] = sv
            for sk, sv in sub["removed"].items():
                removed[f"{key}.{sk}"] = sv
            for sk, sv in sub["changed"].items():
                changed[f"{key}.{sk}"] = sv
        elif av != bv:
            changed[key] = {"before": av, "after": bv}

    return {"added": added, "removed": removed, "changed": changed}
