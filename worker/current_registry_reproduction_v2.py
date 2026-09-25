#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,pathlib,urllib.request

CORE_REPO="dmaillot95-ui/cerebron-omega-ai"
CORE_COMMIT="9caab262e7190a060818bfe0a17330c1564b7f1a"
REGISTRY_PATH="config/farms.json"
EXPECTED_VERSION="2.27"
EXPECTED_COUNT=154
EXPECTED_MAX_ID=174
EXPECTED_MISSING=list(range(153,173))

def main():
    url=f"https://raw.githubusercontent.com/{CORE_REPO}/{CORE_COMMIT}/{REGISTRY_PATH}"
    with urllib.request.urlopen(url,timeout=30) as r:
        raw=r.read()
    d=json.loads(raw)
    farms=d["farms"]
    ids=[int(x["id"]) for x in farms]
    repos=[x["repo"] for x in farms]
    max_id=max(ids) if ids else 0
    missing=[i for i in range(1,max_id+1) if i not in set(ids)]
    checks={
      "json_parsed": True,
      "version_v227": d.get("version")==EXPECTED_VERSION,
      "entry_count_154": len(farms)==EXPECTED_COUNT,
      "max_registered_id_174": max_id==EXPECTED_MAX_ID,
      "max_farms_174": d.get("max_farms")==EXPECTED_MAX_ID,
      "farm_ceiling_174": d.get("farm_ceiling")==EXPECTED_MAX_ID,
      "ids_unique": len(ids)==len(set(ids)),
      "repos_unique": len(repos)==len(set(repos)),
      "sparse_gap_exact_153_to_172": missing==EXPECTED_MISSING,
      "f152_present": any(x.get("id")==152 and x.get("repo")=="cerebron-rdx-exchange" for x in farms),
      "f173_present": any(x.get("id")==173 for x in farms),
      "f174_present": any(x.get("id")==174 for x in farms)
    }
    ok=all(checks.values())
    out={
      "schema":"F71_CURRENT_REGISTRY_REPRODUCTION_V2",
      "farm_id":71,
      "status":"PASS" if ok else "FAIL",
      "source":{"repo":CORE_REPO,"commit":CORE_COMMIT,"path":REGISTRY_PATH},
      "source_file_sha256":hashlib.sha256(raw).hexdigest(),
      "observed":{
        "registry_version":d.get("version"),
        "entry_count":len(farms),
        "first_id":min(ids) if ids else None,
        "max_registered_id":max_id,
        "max_farms":d.get("max_farms"),
        "farm_ceiling":d.get("farm_ceiling"),
        "missing_ids":missing
      },
      "checks":checks,
      "reproduction":"PASS" if ok else "FAIL",
      "independent_method":"Pinned-commit raw registry retrieval and independent structural recomputation in F71 V2; no F72 result trusted.",
      "global_promotion_release":False,
      "gold_released":False,
      "training_released":False,
      "claim_ceiling":"PINNED_SPARSE_REGISTRY_STRUCTURE_REPRODUCTION_ONLY_NO_GLOBAL_F72_RELEASE"
    }
    out["receipt_sha256"]=hashlib.sha256(json.dumps(out,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    pathlib.Path("artifacts").mkdir(exist_ok=True)
    pathlib.Path("artifacts/current_registry_reproduction_v2.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,sort_keys=True))
    if not ok:
        raise SystemExit(2)

if __name__=="__main__":
    main()
