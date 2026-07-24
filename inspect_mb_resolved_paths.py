from pathlib import Path

import pandas as pd

p = Path("/mnt/90-connectome/Personal/CQW/midbrain/mb_sample_info_resolved_paths.xlsx")
df = pd.read_excel(p)
print(df.shape)
print(list(df.columns))
print(df.head(50).to_string())
