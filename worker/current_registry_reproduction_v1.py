#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,pathlib,urllib.request

CORE_REPO="dmaillot95-ui/cerebron-omega-ai"
CORE_COMMIT="cd6b614ef27becbbf1a4a008bc38c5d15b280e2a"
REGISTRY_PATH="config/farms.json"

def main():
    url=f"https://raw.githubusercontent.com/{CORE_REPO}/{CORE_COMMIT}/{REGISTRY_PATH}"
    with urllib.request.urlopen(url,timeout=30) as r:
        raw=r.read()
    d=json.loads(raw); farms=d["farms"]
    ids=[x["id"] for x in farms]; repos=[x["repo"] for x in farms]
    checks={
      "json_parsed":True,
      "count_172":len(farms)==172,
      "ids_1_to_172":ids==list(range(1,173)),
      "ids_unique":len(ids)==len(set(ids)),
      "repos_unique":len(repos)==len(set(repos))
    }
    ok=all(checks.values())
    out={
      "schema":"F71_CURRENT_REGISTRY_REPRODUCTION_V1",
      "farm_id":71,
      "status":"PASS" if ok else "FAIL",
      "source":{"repo":CORE_REPO,"commit":CORE_COMMIT,"path":REGISTRY_PATH},
      "source_file_sha256":hashlib.sha256(raw).hexdigest(),
      "observed":{"farm_count":len(farms),"first_id":ids[0] if ids else None,"last_id":ids[-1] if ids else None},
      "checks":checks,
      "reproduction":"PASS" if ok else "FAIL",
      "independent_method":"Pinned-commit recomputation from config/farms.json; no workflow result trusted.",
      "global_promotion_release":False,
      "claim_ceiling":"PINNED_CURRENT_REGISTRY_FACT_REPRODUCTION_ONLY_NO_GLOBAL_F72_RELEASE"
    }
    out["receipt_sha256"]=hashlib.sha256(json.dumps(out,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    pathlib.Path("artifacts").mkdir(exist_ok=True)
    pathlib.Path("artifacts/current_registry_reproduction_v1.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,sort_keys=True))
    if not ok: raise SystemExit(2)

if __name__=="__main__":
    main()
