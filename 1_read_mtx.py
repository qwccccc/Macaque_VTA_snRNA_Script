# %%
from fast_mtx_reader import batch_read
from pathlib import Path
import anndata
import matplotlib.pyplot as plt
import numpy as np
import pyarrow as pa
import pandas as pd
import polars as pl
import scanpy as sc
import seaborn as sns
import stackprinter
from anndata import AnnData
from scipy.sparse import csr_matrix
import os
from functools import reduce
# import omicverse as ov
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from scipy.cluster.hierarchy import ward, fcluster,dendrogram,linkage
from scipy.stats import spearmanr
from sklearn import model_selection
from sklearn.cluster import AgglomerativeClustering
# %%
adata = sc.read_h5ad(Path('/mnt/90-connectome/Personal/CQW/midbrain/area_h5ad/SN.h5ad'))
adata
# %%
adata.obs.head()

# %%
adata

# %%%
random_idx = np.random.default_rng(42).permutation(adata.n_obs)
split_at = adata.n_obs // 2

adata_1 = adata[random_idx[:split_at]].copy()
adata_2 = adata[random_idx[split_at:]].copy()

adata_1.write_h5ad('/mnt/90-connectome/Personal/CQW/midbrain/area_h5ad/SN_split_1.h5ad')
adata_2.write_h5ad('/mnt/90-connectome/Personal/CQW/midbrain/area_h5ad/SN_split_2.h5ad')
# %%
adata_1
adata_2

# %%%
adata.obs.drop(columns=adata.obs.columns[-8:], inplace=True)
# %%

adata.write_h5ad('/mnt/90-connectome/Personal/CQW/midbrain/area_h5ad/SN_new.h5ad')
# %%
datalist = pd.read_excel('/mnt/90-connectome/Personal/CQW/midbrain/mb_sample_info.xlsx')
datalist

# %%
mbpath = datalist.path + '/' + datalist.Library
# clapath = datalist.clapath
mbpath
# %%
adatas = [read_matrix(Path(filename)) for filename in path]
# %%
# F5用
# unique list function
def unique(list1):
    ans = reduce(lambda re, x: re+[x] if x not in re else re, list1, [])
    return ans

# 读取单细胞函数
def read_matrix(root: Path, separator='\t'):
    if (root / 'matrix.mtx.gz').exists():
        base_df = pl.read_csv(
            root / 'matrix.mtx.gz', has_header=False, comment_prefix='%',
            separator=separator, 
            new_columns=['gene_index', 'cell_index', 'count']
        )
        # print(base_df)
        # print('matrix.mtx.gz')
    elif (root / 'matrix.mtx').exists():
        base_df = pl.read_csv(
            root / 'matrix.mtx', has_header=False, comment_prefix='%',
            separator=separator, 
            new_columns=['gene_index', 'cell_index', 'count']
        )
        # print('matrix.mtx')
    else:
        print(root / 'matrix.mtx No matrix file found')
        
    m = csr_matrix((
            base_df['count'].cast(pl.Float32).to_numpy(),
            (base_df['cell_index'].to_numpy() - 1, base_df['gene_index'].to_numpy() - 1)
            ))  

    if (root / 'barcodes.tsv.gz').exists():
        cell_barcodes_df = pl.read_csv(
            root / 'barcodes.tsv.gz', has_header=False, comment_prefix='%',
            separator='\t', 
            new_columns=['cell_barcode']
        )
    elif (root / 'barcodes.tsv').exists():
        cell_barcodes_df = pl.read_csv(
            root / 'barcodes.tsv', has_header=False, comment_prefix='%',
            separator='\t', 
            new_columns=['cell_barcode']
        )

    if (root / 'features.tsv.gz').exists():
        genes_df = pl.read_csv(
            root / 'features.tsv.gz', has_header=False, comment_prefix='%',
            separator='\t', 
            new_columns=['gene_name']  # 为所有列提供列名
        ).select(['gene_name'])  # 选择第一列
        print(genes_df)
    elif (root / 'genes.tsv.gz').exists():
        genes_df = pl.read_csv(
            root / 'genes.tsv.gz', has_header=False, comment_prefix='%',
            separator=separator, 
            new_columns=['gene_name', 'gene_name_2']
        )
        # print(genes_df)
    elif (root / 'features.tsv').exists():
        genes_df = pl.read_csv(
            root / 'features.tsv', has_header=False, comment_prefix='%',
            separator=separator, 
            new_columns=['gene_name']
        )
        print(genes_df)
    elif (root / 'genes.tsv').exists():
        genes_df = pl.read_csv(
            root / 'genes.tsv', has_header=False, comment_prefix='%',
            separator=separator, 
            new_columns=['gene_name', 'gene_name_2']
        )
        print(genes_df)
    raw_adata = AnnData(X=m)
    raw_adata.var_names = genes_df.to_pandas()['gene_name']
    raw_adata.obs_names = cell_barcodes_df.to_pandas()['cell_barcode']
    # obs 是 observation，要观察的目标，比如细胞
    # var 是 variable，观察对象的属性、特征，比如基因

    return raw_adata
# %%
path = Path('/mnt/112-rawdata-112/marmoset/snRNA/development/MT103-test_260409001/02.count/filter_matrix/')
# %%
adata= [read_matrix(Path(path))]
adata
# %%
adata[0].write_h5ad('MT103-test_260409001.h5ad')
# %%
adata[0]

# %%
