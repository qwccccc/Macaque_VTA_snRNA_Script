from pathlib import Path

import pandas as pd

sample_info = Path("/mnt/90-connectome/Personal/CQW/midbrain/mb_sample_info_resolved_paths.xlsx")
soupx_vta_dir = Path("/mnt/90-connectome/Personal/CQW/midbrain/soupx_vta")

df = pd.read_excel(sample_info).query("area == 'VTA'")
for row in df.itertuples(index=False):
    d = soupx_vta_dir / row.Library
    matrix = sorted(d.glob("matrix.mtx*"))
    features = sorted(d.glob("features.tsv*")) or sorted(d.glob("genes.tsv*"))
    barcodes = sorted(d.glob("barcodes.tsv*"))
    print(row.Library, d.exists(), bool(matrix), bool(features), bool(barcodes), d)
