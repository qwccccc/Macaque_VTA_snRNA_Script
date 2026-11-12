# Macaque VTA snRNA-seq Analysis

猕猴腹侧被盖区（VTA）单核 RNA 测序分析脚本，涵盖数据预处理、细胞类型注释、亚群聚类，以及与大鼠和小鼠的跨物种比较。

Notebooks for macaque VTA single-nucleus RNA-seq preprocessing, cell annotation, subclustering, and cross-species comparisons with rat and mouse.

## 项目结构 / Project Structure

下列结构列出全部分析 notebook 和主要配置文件；本地依赖、缓存及备份目录不展开。

All analysis notebooks and main configuration files are listed below. Local dependencies, caches, and backups are omitted.

```text
Macaque_VTA_snRNA_Script/
├── Script/
│   ├── 0_soupX.ipynb
│   ├── 1_VTA_new.ipynb
│   ├── 2_VTA_DA_cluster.ipynb
│   ├── 2_VTA_neuron_cluster.ipynb
│   ├── 2_VTA_nonneuron_cluster.ipynb
│   ├── 3_VTA_merge_datasets.ipynb
│   ├── 4_VTA_compare_to_rat.ipynb
│   ├── 4_VTA_compare_to_rat_SCT.ipynb
│   ├── 4_VTA_species_compare_published.ipynb
│   ├── 5_VTA_DEGs_species_compare.ipynb
│   └── 5_VTA_DEGs_species_compare_with_mouse.ipynb
├── .vscode/
│   └── settings.json
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml
└── uv.lock
```

## 脚本用途 / Notebook Guide

| Notebook | 用途 / Purpose |
|---|---|
| [0_soupX.ipynb](Script/0_soupX.ipynb) | 使用 SoupX 校正 VTA 样本中的环境 RNA 污染。 / Correct ambient RNA contamination in VTA samples with SoupX. |
| [1_VTA_new.ipynb](Script/1_VTA_new.ipynb) | 对猕猴 VTA 数据进行质量控制、去双细胞、标准化、批次整合和初步细胞类型注释。 / Perform QC, doublet removal, normalization, batch integration, and initial cell annotation. |
| [2_VTA_DA_cluster.ipynb](Script/2_VTA_DA_cluster.ipynb) | 提取多巴胺能（DA）神经元，进行亚群聚类、标记基因分析和注释。 / Recluster dopaminergic neurons and analyze subtype markers. |
| [2_VTA_neuron_cluster.ipynb](Script/2_VTA_neuron_cluster.ipynb) | 对非 DA 神经元进行亚群聚类、标记基因分析和注释。 / Recluster non-DA neurons and annotate their subtypes. |
| [2_VTA_nonneuron_cluster.ipynb](Script/2_VTA_nonneuron_cluster.ipynb) | 对胶质细胞及血管相关细胞等非神经元进行亚群聚类和注释。 / Recluster and annotate non-neuronal populations, including glial and vascular cells. |
| [3_VTA_merge_datasets.ipynb](Script/3_VTA_merge_datasets.ipynb) | 合并各细胞群的分析结果，统一注释，并展示整体细胞组成和表达特征。 / Merge cell populations, harmonize annotations, and summarize cell composition and expression. |
| [4_VTA_compare_to_rat.ipynb](Script/4_VTA_compare_to_rat.ipynb) | 整合猕猴与大鼠 DA 神经元，比较亚群对应关系及基因表达差异。 / Integrate macaque and rat DA neurons and compare subtypes and gene expression. |
| [4_VTA_compare_to_rat_SCT.ipynb](Script/4_VTA_compare_to_rat_SCT.ipynb) | 猕猴与大鼠 DA 神经元比较的另一版本，包含大鼠亚群处理和标记基因表达展示。 / Alternative macaque-rat comparison with rat subcluster processing and marker-expression visualization. |
| [4_VTA_species_compare_published.ipynb](Script/4_VTA_species_compare_published.ipynb) | 使用已发表的小鼠数据，与猕猴 DA 神经元进行整合和亚群比较。 / Integrate published mouse data with macaque DA neurons and compare subtypes. |
| [5_VTA_DEGs_species_compare.ipynb](Script/5_VTA_DEGs_species_compare.ipynb) | 按对应亚群进行猕猴与大鼠的 pseudobulk 差异表达分析，筛选物种偏高和保守候选基因。 / Perform paired-subcluster pseudobulk DE analysis and identify species-enriched and conserved candidate genes. |
| [5_VTA_DEGs_species_compare_with_mouse.ipynb](Script/5_VTA_DEGs_species_compare_with_mouse.ipynb) | 比较候选基因在猕猴和小鼠 DA 亚群中的表达，进行基因分组并绘制热图和小提琴图。 / Compare candidate-gene expression across macaque and mouse DA subtypes, group genes, and visualize heatmaps and violins. |

## 环境 / Environment

主要分析使用 R/Jupyter；Python 环境由 `uv` 管理，要求 Python 3.12 或更高版本。

Analysis primarily uses R/Jupyter. Python dependencies are managed with `uv` and require Python 3.12 or later.

```bash
uv sync
```

R 包依赖、输入数据路径及分析参数以各 notebook 中的代码为准。

Refer to each notebook for R package dependencies, input paths, and analysis parameters.
