from pathlib import Path

import anndata as ad

p = Path("/mnt/90-connectome/Personal/CQW/midbrain/area_h5ad/vta_new.h5ad")
x = ad.read_h5ad(p, backed="r")
print(p, x.shape)
print(sorted(x.obs["Library"].unique().tolist()))
x.file.close()
