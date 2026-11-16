from babel.numbers import format_currency
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

sns.set(style="dark")


def create_daily_orders_df(df):
  daily_orders_df = df.resample(rule="D", on="order_purchase_timestamp").agg(
      {"order_id": "nunique", "price": "sum"}
  )
  daily_orders_df = daily_orders_df.reset_index()
  daily_orders_df.rename(
      columns={"order_id": "order_count", "price": "revenue"}, inplace=True
  )

  return daily_orders_df


def create_bystate_df(df):
  bystate_df = (
      df.groupby(by="customer_state")
      .agg({"order_id": "nunique", "price": "sum"})
      .reset_index()
  )
  bystate_df.rename(
      columns={"order_id": "order_count", "price": "revenue"}, inplace=True
  )
  bystate_df["order_pct"] = round(
      bystate_df.order_count / bystate_df.order_count.sum() * 100, 2
  )
  bystate_df["revenue_pct"] = round(
      bystate_df.revenue / bystate_df.revenue.sum() * 100, 2
  )

  return bystate_df


def create_delivery_review_df(df):
  unique_orders_df = (
      df.drop_duplicates(subset=["order_id"])
      .dropna(subset=["review_score", "delivery_status"])
      .copy()
  )

  avg_review_df = (
      unique_orders_df.groupby(by="delivery_status")
      .agg({"order_id": "nunique", "review_score": "mean"})
      .reindex(["On Time", "Late"])
      .reset_index()
  )

  unique_orders_df["review_group"] = unique_orders_df.review_score.apply(
      lambda x: "Negative (<=2)"
      if x <= 2
      else ("Neutral (3)" if x < 4 else "Positive (>=4)")
  )
  comp_review_df = (
      pd.crosstab(
          unique_orders_df["delivery_status"],
          unique_orders_df["review_group"],
          normalize="index",
      )
      * 100
  )
  comp_review_df = comp_review_df.reindex(
      index=["On Time", "Late"],
      columns=["Negative (<=2)", "Neutral (3)", "Positive (>=4)"],
  )

  return avg_review_df, comp_review_df


def create_delay_cluster_df(df):
  unique_orders_df = (
      df.drop_duplicates(subset=["order_id"])
      .dropna(
          subset=[
              "review_score",
              "order_delivered_customer_date",
              "order_estimated_delivery_date",
          ]
      )
      .copy()
  )
  unique_orders_df["delay_days"] = (
      pd.to_datetime(unique_orders_df["order_delivered_customer_date"])
      - pd.to_datetime(unique_orders_df["order_estimated_delivery_date"])
  ).dt.total_seconds() / 86400

  def categorize_delay(days):
    if days <= 0:
      return "1. Tepat Waktu (<= 0 hari)"
    elif days <= 3:
      return "2. Terlambat Ringan (1-3 hari)"
    elif days <= 7:
      return "3. Terlambat Sedang (4-7 hari)"
    else:
      return "4. Terlambat Berat (> 7 hari)"

  unique_orders_df["delay_category"] = unique_orders_df["delay_days"].apply(
      categorize_delay
  )

  delay_cluster_df = (
      unique_orders_df.groupby("delay_category")
      .agg({"order_id": "nunique", "review_score": "mean"})
      .reset_index()
  )
  delay_cluster_df.rename(
      columns={"order_id": "total_orders", "review_score": "avg_review_score"},
      inplace=True,
  )

  return delay_cluster_df


all_df = pd.read_csv("dashboard/main_data.csv")

datetime_columns = [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
  all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
  st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

  start_date, end_date = st.date_input(
      label="Rentang Waktu",
      min_value=min_date,
      max_value=max_date,
      value=[min_date, max_date],
  )

main_df = all_df[
    (all_df["order_purchase_timestamp"] >= str(start_date))
    & (all_df["order_purchase_timestamp"] <= str(end_date))
]

daily_orders_df = create_daily_orders_df(main_df)
bystate_df = create_bystate_df(main_df)
avg_review_df, comp_review_df = create_delivery_review_df(main_df)
delay_cluster_df = create_delay_cluster_df(main_df)

st.header("E-Commerce Public Dataset Dashboard :sparkles:")

st.subheader("Daily Orders")

col1, col2 = st.columns(2)

with col1:
  total_orders = daily_orders_df.order_count.sum()
  st.metric("Total Orders", value=total_orders)

with col2:
  total_revenue = format_currency(
      daily_orders_df.revenue.sum(), "BRL", locale="pt_BR"
  )
  st.metric("Total Revenue", value=total_revenue)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_purchase_timestamp"],
    daily_orders_df["order_count"],
    marker="o",
    linewidth=2,
    color="#90CAF9",
)
ax.tick_params(axis="y", labelsize=20)
ax.tick_params(axis="x", labelsize=15)

st.pyplot(fig)

st.subheader("Top 5 States by Order & Revenue")

top5_df = bystate_df.sort_values(by="revenue", ascending=False).head(5)
colors = (
    ["#1F4E79"] + ["#9DB7D5"] * (len(top5_df) - 1) if len(top5_df) > 0 else []
)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

ax[0].barh(top5_df["customer_state"], top5_df["order_count"], color=colors)
ax[0].set_title("Jumlah Order", fontsize=14)
ax[0].set_xlabel("Jumlah order")
ax[0].invert_yaxis()
for i, (v, p) in enumerate(zip(top5_df["order_count"], top5_df["order_pct"])):
  ax[0].text(v, i, f" {v:,} ({p:.1f}%)", va="center")
ax[0].set_xlim(0, top5_df["order_count"].max() * 1.25)

ax[1].barh(top5_df["customer_state"], top5_df["revenue"] / 1e6, color=colors)
ax[1].set_title("Total Revenue", fontsize=14)
ax[1].set_xlabel("Revenue (juta)")
ax[1].invert_yaxis()
for i, (v, p) in enumerate(zip(top5_df["revenue"], top5_df["revenue_pct"])):
  ax[1].text(v / 1e6, i, f" {v/1e6:.2f} jt ({p:.1f}%)", va="center")
ax[1].set_xlim(0, top5_df["revenue"].max() / 1e6 * 1.25)

plt.tight_layout()
st.pyplot(fig)

st.subheader("Delivery Delay Impact on Review Score")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

bars = ax[0].bar(
    avg_review_df["delivery_status"],
    avg_review_df["review_score"],
    color="#1F4E79",
)
ax[0].set_title("Rata-rata Review Score", fontsize=14)
ax[0].set_ylabel("Rata-rata review score (skala 1-5)")
ax[0].set_ylim(0, 5)
for bar in bars:
  yval = bar.get_height()
  if pd.notna(yval):
    ax[0].text(
        bar.get_x() + bar.get_width() / 2,
        yval + 0.1,
        f"{yval:.2f}",
        ha="center",
        fontsize=11,
    )

comp_colors = ["#C84B59", "#B5B5B5", "#2B7A9B"]
comp_review_df.plot(kind="barh", stacked=True, color=comp_colors, ax=ax[1])
ax[1].set_title("Komposisi Review", fontsize=14)
ax[1].set_xlabel("Persentase order (%)")
ax[1].set_ylabel("")
ax[1].invert_yaxis()
ax[1].legend(
    title="Kelompok review",
    loc="lower center",
    bbox_to_anchor=(0.5, -0.25),
    ncol=3,
)

for c in ax[1].containers:
  labels = [f"{w:.1f}%" if w > 5 else "" for w in c.datavalues]
  ax[1].bar_label(
      c, labels=labels, label_type="center", color="white", fontweight="bold"
  )

plt.tight_layout()
st.pyplot(fig)

st.subheader("Delivery Delay Clustering Analysis")

fig, ax = plt.subplots(figsize=(12, 5))
bars = ax.bar(
    delay_cluster_df["delay_category"],
    delay_cluster_df["avg_review_score"],
    color="#1F4E79",
)
ax.set_title(
    "Rata-rata Review Score Berdasarkan Kategori Keterlambatan", fontsize=14
)
ax.set_ylabel("Rata-rata Review Score (Skala 1-5)")
ax.set_ylim(0, 5)

for bar in bars:
  yval = bar.get_height()
  ax.text(
      bar.get_x() + bar.get_width() / 2,
      yval + 0.1,
      f"{yval:.2f}",
      ha="center",
      fontsize=11,
  )

plt.tight_layout()
st.pyplot(fig)

st.caption("Copyright (c) Axel Antonia 2026")