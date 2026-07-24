import pandas as pd

p = "/mnt/90-connectome/Personal/CQW/midbrain/mb_sample_info.xlsx"
df = pd.read_excel(p)
print(df.shape)
print(list(df.columns))
print(df.head(50).to_string())
