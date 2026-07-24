from pathlib import Path

import pandas as pd

sample_info = Path("/mnt/90-connectome/Personal/CQW/midbrain/mb_sample_info.xlsx")
roots = [
    Path("/mnt/112-seqdata/macaque/snRNA/resolved/20250429-VTA-snRNA"),
    Path("/mnt/112-seqdata/macaque/snRNA/resolved/20250430-zmy-anno"),
    Path("/mnt/112-seqdata/macaque/snRNA/resolved/SoupX_decontaminated_Midbrain_pons"),
    Path("/mnt/112-seqdata/macaque/snRNA/resolved/20250522-zmy-anno"),
]

df = pd.read_excel(sample_info)
for root in roots:
    print(f"\nROOT {root}")
    found = 0
    for lib in df["Library"]:
        lib_dir = root / lib
        matrix_files = sorted(lib_dir.rglob("matrix.mtx*")) if lib_dir.exists() else []
        if matrix_files:
            found += 1
            matrix_dir = matrix_files[0].parent
            has_features = bool(list(matrix_dir.glob("features.tsv*")) or list(matrix_dir.glob("genes.tsv*")))
            has_barcodes = bool(list(matrix_dir.glob("barcodes.tsv*")))
            print(lib, matrix_dir, has_features, has_barcodes)
    print("found", found, "of", len(df))
