from pathlib import Path
import re

import anndata as ad
import pandas as pd
from anndata import AnnData
from scipy.io import mmread


SAMPLE_INFO = Path("/mnt/90-connectome/Personal/CQW/midbrain/mb_sample_info_resolved_paths.xlsx")
OUTPUT_DIR = Path("/mnt/90-connectome/Personal/CQW/midbrain/area_h5ad")


def safe_name(value: str) -> str:
    return re.sub(r"[^0-9A-Za-z._-]+", "_", value).strip("_")


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
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    sample_info = pd.read_excel(SAMPLE_INFO)
    sample_info["matrix_dir"] = sample_info["filter_matrix_path"]

    manifest_rows: list[dict[str, object]] = []
    for area, area_info in sample_info.groupby("area", sort=False):
        area_adatas: list[AnnData] = []
        for _, row in area_info.iterrows():
            matrix_dir = Path(row["matrix_dir"])
            sample_adata = read_matrix(matrix_dir)

            for key, value in row.items():
                sample_adata.obs[key] = value
            sample_adata.obs_names = [f"{row['Library']}:{barcode}" for barcode in sample_adata.obs_names]
            area_adatas.append(sample_adata)

            manifest_rows.append(
                {
                    "area": area,
                    "Library": row["Library"],
                    "sample_name": row["sample_name"],
                    "Animal": row["Animal"],
                    "n_cells": sample_adata.n_obs,
                    "n_genes": sample_adata.n_vars,
                    "matrix_dir": str(matrix_dir),
                }
            )
            print(area, row["Library"], sample_adata.shape, matrix_dir, flush=True)

        area_adata = ad.concat(area_adatas, join="outer", merge="same", index_unique=None)
        area_adata.write_h5ad(OUTPUT_DIR / f"{safe_name(str(area))}.h5ad")
        print("wrote", OUTPUT_DIR / f"{safe_name(str(area))}.h5ad", area_adata.shape, flush=True)

    pd.DataFrame(manifest_rows).to_csv(OUTPUT_DIR / "manifest.csv", index=False)
    sample_info.to_csv(OUTPUT_DIR / "sample_info_with_matrix_dir.csv", index=False)


if __name__ == "__main__":
    main()
