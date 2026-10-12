# -*- coding: utf-8 -*-
"""
生成四张统计图到 output/：结局分布、血糖分布对比、
各年龄段患病率、指标相关系数热力图。

依赖 step2_clean.py 产出的 data/diabetes_cleaned.csv

用法：
    python step3_charts.py
"""

import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# matplotlib 默认字体不含中文，需显式指定
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

sns.set_theme(style="whitegrid", font=plt.rcParams["font.sans-serif"][0])

COLOR_NEG = "#185FA5"   # 未患病
COLOR_POS = "#D85A30"   # 患病
PALETTE = [COLOR_NEG, COLOR_POS]

os.makedirs("output", exist_ok=True)

df = pd.read_csv("data/diabetes_cleaned.csv")
df["OutcomeLabel"] = df["Outcome"].map({0: "未患病", 1: "患病"})

# ---------------------------------------------------------------
# 图 1：结局变量分布
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6, 4.2))
counts = df["OutcomeLabel"].value_counts().reindex(["未患病", "患病"])
bars = ax.bar(counts.index, counts.values, color=PALETTE, width=0.55)

for bar, value in zip(bars, counts.values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        value + 8,
        f"{value} ({value / len(df) * 100:.1f}%)",
        ha="center",
        fontsize=11,
    )

ax.set_title("糖尿病结局分布", fontsize=14)
ax.set_ylabel("人数")
ax.set_ylim(0, max(counts.values) * 1.18)
fig.tight_layout()
fig.savefig("output/01_outcome_dist.png", dpi=150)
plt.close(fig)
print("[已生成] output/01_outcome_dist.png")

# ---------------------------------------------------------------
# 图 2：血糖分布 —— 患病组 vs 未患病组
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.6, 4.2))
sns.histplot(
    data=df,
    x="Glucose",
    hue="OutcomeLabel",
    hue_order=["未患病", "患病"],
    palette=PALETTE,
    bins=30,
    alpha=0.6,
    edgecolor="white",
    linewidth=0.5,
    ax=ax,
)
ax.set_title("血糖分布：患病组 vs 未患病组", fontsize=14)
ax.set_xlabel("血糖 (Glucose)")
ax.set_ylabel("人数")
ax.get_legend().set_title("结局")
fig.tight_layout()
fig.savefig("output/02_glucose_hist.png", dpi=150)
plt.close(fig)
print("[已生成] output/02_glucose_hist.png")

# ---------------------------------------------------------------
# 图 3：各年龄段患病率
# ---------------------------------------------------------------
rate = (
    df.groupby("AgeGroup", observed=True)["Outcome"]
    .mean()
    .mul(100)
    .round(1)
    .reset_index(name="患病率")
)

fig, ax = plt.subplots(figsize=(6.8, 4.2))
bars = ax.bar(rate["AgeGroup"].astype(str), rate["患病率"], color=COLOR_POS, width=0.58)
for bar, value in zip(bars, rate["患病率"]):
    ax.text(bar.get_x() + bar.get_width() / 2, value + 1.2, f"{value}%", ha="center", fontsize=11)

ax.set_title("各年龄段糖尿病患病率", fontsize=14)
ax.set_xlabel("年龄段")
ax.set_ylabel("患病率 (%)")
ax.set_ylim(0, max(rate["患病率"]) * 1.2)
fig.tight_layout()
fig.savefig("output/03_age_group_rate.png", dpi=150)
plt.close(fig)
print("[已生成] output/03_age_group_rate.png")

# ---------------------------------------------------------------
# 图 4：相关系数热力图
# ---------------------------------------------------------------
numeric_df = df.drop(columns=["AgeGroup", "OutcomeLabel"])
corr = numeric_df.corr(numeric_only=True)

fig, ax = plt.subplots(figsize=(7.6, 6))
sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    cmap="RdBu_r",
    center=0,
    vmin=-1,
    vmax=1,
    square=True,
    linewidths=0.5,
    cbar_kws={"shrink": 0.75},
    ax=ax,
)
ax.set_title("各指标相关系数热力图", fontsize=14)
fig.tight_layout()
fig.savefig("output/04_corr_heatmap.png", dpi=150)
plt.close(fig)
print("[已生成] output/04_corr_heatmap.png")

# ---------------------------------------------------------------
# 输出各指标与结局变量的相关系数排序
# ---------------------------------------------------------------
print()
print("=" * 56)
print("各指标与结局变量的相关系数（降序）")
print("=" * 56)
top = corr["Outcome"].drop("Outcome").sort_values(ascending=False)
for name, value in top.items():
    print(f"  {name:<24} r = {value:+.3f}")

overall_rate = df["Outcome"].mean() * 100
glucose_pos = df.loc[df["Outcome"] == 1, "Glucose"].mean()
glucose_neg = df.loc[df["Outcome"] == 0, "Glucose"].mean()
print()
print(f"总体患病率: {overall_rate:.1f}%")
print(f"患病组平均血糖: {glucose_pos:.1f}   未患病组平均血糖: {glucose_neg:.1f}")
print()
