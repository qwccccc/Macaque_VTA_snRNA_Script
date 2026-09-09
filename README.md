# Macaque VTA snRNA-seq Analysis

本项目包含猕猴腹侧被盖区（VTA）单核 RNA 测序数据的预处理、质量控制、细胞类型聚类和结果整合 notebook。
This project contains notebooks for preprocessing, quality control, cell-type clustering, and integration of macaque ventral tegmental area (VTA) single-nucleus RNA sequencing data.


## 项目结构 / Project Structure

分析和后续维护使用 `Script/` 中对应的文件。
Use the corresponding notebooks in `Script/` for analysis and maintenance.


```text
Macaque_VTA_snRNA_Script/
├── Script/
│   ├── 0_soupX.ipynb                  # 环境 RNA 校正 / Ambient RNA correction
│   ├── 1_VTA_new.ipynb                # QC、去双细胞、整合和初步注释 / QC, doublet removal, integration, and preliminary annotation
│   ├── 2_VTA_DA_cluster.ipynb         # DA 细胞重聚类 / Dopaminergic cell reclustering
│   ├── 2_VTA_neuron_cluster.ipynb     # 非 DA 神经元重聚类 / Non-dopaminergic neuron reclustering
│   ├── 2_VTA_nonneurون_cluster.ipynb   # 非神经元重聚类 / Non-neuronal cell reclustering
│   ├── 3_VTA_merge_datasets.ipynb     # 合并各细胞群分析结果 / Merge results across cell populations
│   └── 4_VTA_compare_to_rat.ipynb     # 与大鼠 DA 神经元跨物种比较 / Cross-species comparison with rat dopaminergic neurons
├── pyproject.toml                    # Python 环境与依赖 / Python environment and dependencies
└── uv.lock                           # 依赖版本锁定文件 / Dependency lockfile
```

## 分析流程 / Analysis Workflow

推荐按以下顺序运行；每个 notebook 中的数据路径和关键参数均以代码为准。

Run the notebooks in the following order. Refer to the code in each notebook for data paths and analysis parameters.

1. **`Script/0_soupX.ipynb`**  
   读取样本信息表，针对 `area == "VTA"` 的每个文库进行 SoupX 校正；结果写入 `soupx_vta/`，并输出汇总 CSV 和 XLSX。  
   Read the sample metadata and perform SoupX ambient RNA correction for each library with `area == "VTA"`. Save corrected data to `soupx_vta/` and export summary tables in CSV and XLSX formats.

2. **`Script/1_VTA_new.ipynb`**  
   从 `vta_new-1.h5ad` 建立 Seurat 对象，计算 QC 指标、使用 `scDblFinder` 去除双细胞、进行 SCTransform、Harmony 整合和初步细胞类型注释。  
   Create a Seurat object from `vta_new-1.h5ad`, calculate QC metrics, remove doublets using `scDblFinder`, and perform SCTransform normalization, Harmony integration, and preliminary cell-type annotation.

3. **`Script/2_VTA_DA_cluster.ipynb`**  
   提取 DA 细胞，以 Animal 为批次进行 Harmony 重聚类，输出 DA 聚类 RDS 和图件。  
   Subset dopaminergic (DA) cells and recluster them using Harmony with `Animal` as the batch variable. Export the clustering results as an RDS file and generate figures.

4. **`Script/2_VTA_neuron_cluster.ipynb`**  
   对非 DA 神经元细胞进行重聚类，输出聚类 RDS 和图件。  
   Recluster non-dopaminergic neurons, export the clustering results as an RDS file, and generate figures.

5. **`Script/2_VTA_nonneuron_cluster.ipynb`**  
   对 Astro、Oligo、OPC、Micro、Endothelial 和 VLMC 等非神经元细胞进行重聚类，输出非神经元聚类 RDS 和图件。  
   Recluster non-neuronal populations, including astrocytes, oligodendrocytes, oligodendrocyte precursor cells, microglia, endothelial cells, and vascular leptomeningeal cells. Export the clustering results as an RDS file and generate figures.

6. **`Script/3_VTA_merge_datasets.ipynb`**  
   合并 DA、非神经元和其他神经元结果，统一细胞类别与 cluster 命名，并生成最终整合对象和概览图。  
   Merge results from DA cells, non-neuronal cells, and other neurons. Standardize cell-type and cluster labels, and generate the final combined object and overview figures.

7. **`Script/4_VTA_compare_to_rat.ipynb`**  
   对猕猴与大鼠的 DA 神经元进行整合，开展跨物种比较、分析物种特异性基因，并生成跨物种整合对象。  
   Integrate macaque and rat DA neurons, perform cross-species comparisons, analyze species-specific genes, and generate a cross-species integrated object.

## 环境 / Environment

Python 环境由 `uv` 管理，项目要求 Python 3.12 或更高版本：

The Python environment is managed using `uv` and requires Python 3.12 or later:

```bash
uv sync
```

主要分析在 R/Jupyter notebook 中执行，需安装 Seurat、Harmony、SoupX、scDblFinder、anndata、reticulate 及其依赖。

Most analyses are performed in R notebooks through Jupyter and require Seurat, Harmony, SoupX, scDblFinder, anndata, reticulate, and their dependencies.

涉及 Python 的 R notebook 应通过 `reticulate` 使用项目的 `.venv` 虚拟环境；具体解释器路径根据操作系统及项目位置设置。

R notebooks that call Python should use the project's `.venv` environment through `reticulate`. Configure the Python interpreter path according to the operating system and project location.