# Macaque VTA snRNA-seq Analysis

本项目包含猕猴腹侧被盖区（VTA）单核 RNA 测序数据的预处理、质量控制、细胞类型聚类和结果整合 notebook。

## 当前目录状态

分析 notebook 正在从项目根目录逐步整理至 `Script/`。部分根目录 notebook 仍在运行，因此当前保留原位置；待其运行结束后再完成迁移。新分析和后续维护应优先使用 `Script/` 中对应的文件，避免在同一分析步骤维护两份版本。

```text
mb/
├── Script/                         # 正在整理中的主要分析 notebook
│   ├── 1_VTA.ipynb                 # VTA 基础分析版本
│   ├── 1_VTA_new.ipynb             # VTA QC、去双细胞、整合和初步注释
│   ├── 2_VTA_DA_cluster.ipynb      # DA 细胞重聚类和跨物种注释比较
│   ├── 2_VTA_nonneuron_cluster.ipynb # 非神经元细胞重聚类
│   ├── 3_VTA_merge_dataset.ipynb       # 合并 DA、非神经元和其他神经元结果，待迁移
│   └── soupX.ipynb                 # VTA 文库 SoupX 环境 RNA 校正
├── pyproject.toml                   # Python 环境与依赖
└── uv.lock                          # 锁定的 Python 依赖版本
```

## 分析流程

推荐按以下顺序运行；每个 notebook 中的数据路径和关键参数均以代码为准。

1. `Script/soupX.ipynb`：读取样本信息表，针对 `area == "VTA"` 的每个文库进行 SoupX 校正；结果写入 `soupx_vta/`，并输出汇总 CSV 和 XLSX。
2. `Script/1_VTA_new.ipynb`：从 `vta_new-1.h5ad` 建立 Seurat 对象，计算 QC 指标、使用 `scDblFinder` 去除双细胞、进行 SCTransform、Harmony 整合和初步细胞类型注释。
3. `Script/2_VTA_DA_cluster.ipynb`：提取 DA 细胞，以 Animal 为批次进行 Harmony 重聚类，并与小鼠参考注释比较；输出 DA 聚类 RDS 和图件。
4. `Script/2_VTA_nonneuron_cluster.ipynb`：对 Astro、Oligo、OPC、Micro、Endothelial 和 VLMC 等非神经元细胞进行重聚类；输出非神经元聚类 RDS 和图件。
5. `Script/3_VTA_merge_dataset.ipynb`：合并 DA、非神经元和其他神经元结果，统一细胞类别与 cluster 命名，并生成最终整合对象和概览图。


## 环境

Python 环境由 `uv` 管理，项目要求 Python 3.12 或更高版本：

```bash
cd /home/chaiqw/project/mb
uv sync
```

主要分析在 R/Jupyter notebook 中执行，需安装 Seurat、Harmony、SoupX、scDblFinder、anndata、reticulate 及其依赖。涉及 Python 的 R notebook 使用项目虚拟环境：

```r
use_virtualenv("/home/chaiqw/project/mb/.venv")
```

资源密集型 notebook 中目前设置了最多 64 个 worker；在共享服务器上执行前，请按当时可用资源调整该参数。
