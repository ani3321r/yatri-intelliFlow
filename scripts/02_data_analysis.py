import sqlite3
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def load_data(csv_path: str = "data/namma_yatri_rides.csv") -> pd.DataFrame:
    return pd.read_csv(csv_path, parse_dates=["ride_datetime"])


def create_sqlite_db(df: pd.DataFrame, db_path: str = "data/namma_yatri.db"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    df.to_sql("rides", conn, index=False, if_exists="replace")
    conn.close()
    print(f"SQLite database created at {db_path}")


def run_key_queries(df: pd.DataFrame):
    print("=== Key Metrics ===")
    print(f"Total rides: {len(df)}")
    print(f"Completion rate: {df['is_completed'].mean() * 100:.1f}%")
    print(f"Total revenue (₹): {df[df['is_completed'] == 1]['fare_amount'].sum():,.2f}")

    print("\nTop 5 hours by demand:")
    print(
        df.groupby("hour_of_day")["ride_id"]
        .count()
        .sort_values(ascending=False)
        .head()
    )

    print("\nTop 5 zones by revenue:")
    print(
        df[df["is_completed"] == 1]
        .groupby("pickup_zone")["fare_amount"]
        .sum()
        .sort_values(ascending=False)
        .head()
    )


def generate_visualizations(df: pd.DataFrame, out_dir: str = "visualizations"):
    os.makedirs(out_dir, exist_ok=True)

    # Figure 1: Demand heatmap, duration distribution, driver revenue
    plt.figure(figsize=(14, 4))

    # Demand heatmap (day vs hour)
    plt.subplot(1, 3, 1)
    pivot = (
        df.pivot_table(
            index="day_of_week",
            columns="hour_of_day",
            values="ride_id",
            aggfunc="count",
        )
        .reindex(
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
        )
    )
    sns.heatmap(pivot, cmap="YlOrRd")
    plt.title("Demand Heatmap\n(Day vs Hour)")
    plt.xlabel("Hour of Day")
    plt.ylabel("Day of Week")

    # Trip duration distribution
    plt.subplot(1, 3, 2)
    sns.histplot(df["ride_time_min"], bins=20, kde=True)
    plt.title("Ride Duration Distribution")
    plt.xlabel("Ride Time (min)")

    # Driver revenue distribution
    plt.subplot(1, 3, 3)
    driver_rev = (
        df[df["is_completed"] == 1]
        .groupby("driver_id")["fare_amount"]
        .sum()
        .reset_index()
    )
    sns.boxplot(y=driver_rev["fare_amount"])
    plt.title("Driver Revenue Distribution")
    plt.ylabel("Total Revenue per Driver (₹)")

    fig1_path = os.path.join(out_dir, "namma_yatri_analytics_1.png")
    plt.tight_layout()
    plt.savefig(fig1_path, dpi=300)
    plt.close()

    # Figure 2: Zone performance, rating vs wait, hourly trend
    plt.figure(figsize=(14, 4))

    plt.subplot(1, 3, 1)
    zone_perf = (
        df[df["is_completed"] == 1]
        .groupby("pickup_zone")["fare_amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    sns.barplot(x=zone_perf.values, y=zone_perf.index)
    plt.title("Top Zones by Revenue")
    plt.xlabel("Revenue (₹)")
    plt.ylabel("Pickup Zone")

    plt.subplot(1, 3, 2)
    completed = df[df["is_completed"] == 1].copy()
    sns.scatterplot(
        data=completed,
        x="wait_time_min",
        y="rating",
        alpha=0.5,
    )
    sns.regplot(
        data=completed,
        x="wait_time_min",
        y="rating",
        scatter=False,
        color="red",
    )
    plt.title("Rating vs Wait Time")
    plt.xlabel("Wait Time (min)")
    plt.ylabel("Rating")

    plt.subplot(1, 3, 3)
    hourly = (
        df.groupby("hour_of_day")["ride_id"]
        .count()
        .reset_index()
        .rename(columns={"ride_id": "total_rides"})
    )
    sns.lineplot(data=hourly, x="hour_of_day", y="total_rides", marker="o")
    plt.title("Hourly Demand Trend")
    plt.xlabel("Hour of Day")
    plt.ylabel("Total Rides")

    fig2_path = os.path.join(out_dir, "namma_yatri_analytics_2.png")
    plt.tight_layout()
    plt.savefig(fig2_path, dpi=300)
    plt.close()

    print(f"Saved visualizations:\n- {fig1_path}\n- {fig2_path}")


def main():
    df = load_data()
    create_sqlite_db(df)
    run_key_queries(df)
    generate_visualizations(df)


if __name__ == "__main__":
    main()


