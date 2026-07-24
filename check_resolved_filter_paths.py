from pathlib import Path

import pandas as pd

p = Path("/mnt/90-connectome/Personal/CQW/midbrain/mb_sample_info_resolved_paths.xlsx")
df = pd.read_excel(p)
for row in df.itertuples(index=False):
    d = Path(row.filter_matrix_path)
    matrix = sorted(d.glob("matrix.mtx*"))
    features = sorted(d.glob("features.tsv*")) or sorted(d.glob("genes.tsv*"))
    barcodes = sorted(d.glob("barcodes.tsv*"))
    print(row.Library, d.exists(), bool(matrix), bool(features), bool(barcodes), d)
