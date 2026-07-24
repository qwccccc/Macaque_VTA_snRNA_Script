from pathlib import Path

import anndata as ad

d = Path("/mnt/90-connectome/Personal/CQW/midbrain/area_h5ad")
for p in sorted(d.glob("*.h5ad")):
    x = ad.read_h5ad(p, backed="r")
    print(p.name, x.shape)
    x.file.close()
