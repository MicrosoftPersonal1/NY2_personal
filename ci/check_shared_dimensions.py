"""Shared dimensions (Date, Store, Product, Customer) must be identical in every core model.
Compares the TMDL files of these tables across all models under workspace/, ignoring lineageTag lines."""
import glob, os, re, sys

SHARED = ["Date", "Store", "Product", "Customer"]   # table file names (without .tmdl) – demo model names

def norm(path):
    with open(path, encoding="utf-8") as f:
        return "\n".join(l.rstrip() for l in f if not re.match(r"\s*lineageTag:", l))

failed = False
for table in SHARED:
    files = glob.glob(f"workspace/*.SemanticModel/definition/tables/{table}.tmdl")
    if len(files) < 2:
        continue
    base = norm(files[0])
    for other in files[1:]:
        if norm(other) != base:
            print(f"DIFF  {table}: {os.path.dirname(os.path.dirname(os.path.dirname(other)))} differs from {files[0]}")
            failed = True
print("Shared dimensions: FAIL" if failed else "Shared dimensions: OK")
sys.exit(1 if failed else 0)
