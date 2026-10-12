# -*- coding: utf-8 -*-
"""
数据探查：输出数据集规模、字段类型、统计摘要与结局变量分布，
并检测以 0 编码的缺失值。

用法：
    python step1_load.py
"""

import pandas as pd

# 加宽输出，避免字段过多时自动折行
pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 50)

# DataFrame 即 pandas 的二维表结构
df = pd.read_csv("data/diabetes.csv")

print("=" * 56)
print("1) 前 5 行")
print("=" * 56)
print(df.head())

print()
print("=" * 56)
print("2) 数据规模")
print("=" * 56)
rows, cols = df.shape
print(f"行数（病人）: {rows}")
print(f"列数（字段）: {cols}")

print()
print("=" * 56)
print("3) 字段类型与缺失情况")
print("=" * 56)
df.info()

print()
print("=" * 56)
print("4) 数值列统计摘要")
print("=" * 56)
print(df.describe().round(2))

print()
print("=" * 56)
print("5) 结局变量分布")
print("=" * 56)
print("计数：")
print(df["Outcome"].value_counts().sort_index())
print()
print("占比 (%)：")
print(df["Outcome"].value_counts(normalize=True).sort_index().mul(100).round(1))

print()
print("=" * 56)
print("6) df.isnull().sum()  ——  官方缺失值统计")
print("=" * 56)
print(df.isnull().sum())

# isnull() 无法识别以 0 编码的缺失值，需单独检测
print()
print("=" * 56)
print("以 0 编码的缺失值检测")
print("=" * 56)
zero_check_cols = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
print("下列字段在活体测量中不可能为 0，其中的 0 判定为缺失：")
print()
for col in zero_check_cols:
    n_zero = (df[col] == 0).sum()
    pct = n_zero / len(df) * 100
    print(f"  {col:<16} 0 值个数 = {n_zero:<4} 占比 {pct:.1f}%")

print()
print("缺失值处理见 step2_clean.py")
