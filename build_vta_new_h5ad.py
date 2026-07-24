from pathlib import Path

import anndata as ad
import pandas as pd
from anndata import AnnData
from scipy.io import mmread


SAMPLE_INFO = Path("/mnt/90-connectome/Personal/CQW/midbrain/mb_sample_info_resolved_paths.xlsx")
SOUPX_VTA_DIR = Path("/mnt/90-connectome/Personal/CQW/midbrain/soupx_vta")
OUTPUT_H5AD = Path("/mnt/90-connectome/Personal/CQW/midbrain/area_h5ad/vta_new-1.h5ad")
OUTPUT_MANIFEST = Path("/mnt/90-connectome/Personal/CQW/midbrain/area_h5ad/vta_new-1_manifest.csv")


def read_first_column(path: Path) -> list[str]:
    return pd.read_csv(path, sep="\t", header=None, usecols=[0])[0].astype(str).tolist()


def read_matrix(root: Path) -> AnnData:
    matrix_path = next(iter(sorted(root.glob("matrix.mtx*"))))
    feature_paths = sorted(root.glob("features.tsv*")) or sorted(root.glob("genes.tsv*"))
    barcode_paths = sorted(root.glob("barcodes.tsv*"))

    features = read_first_column(feature_paths[0])
    barcodes = read_first_column(barcode_paths[0])
    x = mmread(matrix_path).tocsr().T

    adata = AnnData(X=x)
    adata.var_names = features
    adata.obs_names = barcodes
    adata.var_names_make_unique()
    return adata


def main() -> None:
    OUTPUT_H5AD.parent.mkdir(parents=True, exist_ok=True)
    sample_info = pd.read_excel(SAMPLE_INFO)
    vta_info = sample_info.query("area == 'VTA'").copy()
    vta_info["matrix_dir"] = vta_info["Library"].map(lambda x: str(SOUPX_VTA_DIR / str(x)))

    adatas: list[AnnData] = []
    manifest_rows: list[dict[str, object]] = []
    for _, row in vta_info.iterrows():
        matrix_dir = Path(row["matrix_dir"])
        sample_adata = read_matrix(matrix_dir)

        for key, value in row.items():
            sample_adata.obs[key] = value
        sample_adata.obs["dataset"] = "vta_new"
        sample_adata.obs_names = [f"{row['Library']}:{barcode}" for barcode in sample_adata.obs_names]
        adatas.append(sample_adata)

        manifest_rows.append(
            {
                "dataset": "vta_new",
                "area": row["area"],
                "Library": row["Library"],
                "sample_name": row["sample_name"],
                "Animal": row["Animal"],
                "n_cells": sample_adata.n_obs,
                "n_genes": sample_adata.n_vars,
                "matrix_dir": str(matrix_dir),
            }
        )
        print(row["Library"], sample_adata.shape, matrix_dir, flush=True)

    vta_new = ad.concat(adatas, join="outer", merge="same", index_unique=None)
    vta_new.write_h5ad(OUTPUT_H5AD)
    pd.DataFrame(manifest_rows).to_csv(OUTPUT_MANIFEST, index=False)
    print("wrote", OUTPUT_H5AD, vta_new.shape, flush=True)


if __name__ == "__main__":
    main()
