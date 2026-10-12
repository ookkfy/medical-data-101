# -*- coding: utf-8 -*-
"""
数据清洗：将以 0 编码的缺失值替换为 NaN，按各列中位数填补，
并派生年龄段分组用于后续统计。

用法：
    python step2_clean.py
"""

import numpy as np
import pandas as pd

pd.set_option("display.width", 120)

df = pd.read_csv("data/diabetes.csv")

zero_as_missing = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]

# ---------------------------------------------------------------
# 1. 将 0 替换为 NaN，使 pandas 能正确识别为缺失
# ---------------------------------------------------------------
print("=" * 56)
print("1) 把 0 替换成 NaN（真正的缺失）")
print("=" * 56)

before = (df[zero_as_missing] == 0).sum()
df[zero_as_missing] = df[zero_as_missing].replace(0, np.nan)

after = df[zero_as_missing].isnull().sum()

summary = pd.DataFrame({"替换前 0 的个数": before, "替换后 NaN 个数": after})
print(summary)
print()
print("现在再用 df.isnull().sum() 就能查出来了：")
print(df.isnull().sum()[lambda s: s > 0])

# ---------------------------------------------------------------
# 2. 填补缺失
#    这里用「中位数」而不是「平均数」：
#    医疗数据常有极端值（比如胰岛素能到 800），平均数会被拉偏，中位数更稳
# ---------------------------------------------------------------
print()
print("=" * 56)
print("2) 用各列中位数填补缺失")
print("=" * 56)

for col in zero_as_missing:
    median_value = df[col].median()
    df[col] = df[col].fillna(median_value)
    print(f"  {col:<16} 中位数 = {median_value:<8.2f} 已填补")

print()
print("填补后缺失值总数：")
print(df.isnull().sum().sum())

# ---------------------------------------------------------------
# 3. 新增一个字段：年龄段
# 按年龄段分箱，便于后续分组统计
# ---------------------------------------------------------------
print()
print("=" * 56)
print("3) 新增 AgeGroup 年龄段字段")
print("=" * 56)

df["AgeGroup"] = pd.cut(
    df["Age"],
    bins=[20, 30, 40, 50, 60, 100],
    labels=["21-30", "31-40", "41-50", "51-60", "60+"],
)
print(df["AgeGroup"].value_counts().sort_index())

# ---------------------------------------------------------------
# 4. 看一眼分组统计：各年龄段的患病率
# 按年龄段聚合：Outcome 为 0/1，其均值即患病率
# ---------------------------------------------------------------
print()
print("=" * 56)
print("4) 各年龄段患病率")
print("=" * 56)

rate_by_age = (
    df.groupby("AgeGroup", observed=True)["Outcome"]
    .agg(人数="count", 患病人数="sum", 患病率="mean")
    .assign(患病率=lambda d: (d["患病率"] * 100).round(1))
)
print(rate_by_age)

# ---------------------------------------------------------------
# 5. 存盘供 step3_charts.py 使用
# ---------------------------------------------------------------
df.to_csv("data/diabetes_cleaned.csv", index=False, encoding="utf-8-sig")
print()
print("=" * 56)
print("清洗后的数据已保存到 data/diabetes_cleaned.csv")
print("=" * 56)
