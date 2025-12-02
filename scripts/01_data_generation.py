import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random


def generate_namma_yatri_data(
    n_rides: int = 500,
    days: int = 7,
    random_seed: int = 42,
    output_path: str = "data/namma_yatri_rides.csv",
):
    random.seed(random_seed)
    np.random.seed(random_seed)

    zones = [
        "Whitefield",
        "Koramangala",
        "Indiranagar",
        "BTM Layout",
        "Electronic City",
        "Marathahalli",
        "MG Road",
        "Jayanagar",
        "Hebbal",
        "Yelahanka",
        "Rajajinagar",
        "Malleshwaram",
        "Banashankari",
        "HSR Layout",
        "KR Puram",
    ]

    base_datetime = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days)

    records = []
    ride_id = 1

    for _ in range(n_rides):
        day_offset = random.randint(0, days - 1)
        hour_of_day = random.randint(0, 23)
        minute = random.randint(0, 59)

        ts = base_datetime + timedelta(days=day_offset, hours=hour_of_day, minutes=minute)

        # Peak hour demand boost
        is_peak = (7 <= hour_of_day <= 10) or (17 <= hour_of_day <= 20)

        pickup_zone = random.choice(zones)
        drop_zone = random.choice([z for z in zones if z != pickup_zone])

        distance_km = max(1, np.random.normal(8 if is_peak else 6, 3))
        base_fare_per_km = 18
        surge_multiplier = 1.4 if is_peak else 1.0

        wait_time_min = max(1, np.random.normal(6 if is_peak else 4, 2))
        ride_time_min = max(5, distance_km * np.random.uniform(2.5, 3.5))

        completed_prob = 0.9 - 0.03 * (wait_time_min > 8) - 0.02 * (ride_time_min > 40)
        is_completed = np.random.rand() < completed_prob

        base_fare = distance_km * base_fare_per_km * surge_multiplier
        time_component = ride_time_min * 1.2
        fare_amount = round(base_fare + time_component + np.random.normal(0, 10), 2)
        fare_amount = max(40, fare_amount)

        if is_completed:
            rating = np.clip(np.random.normal(4.5 - 0.02 * wait_time_min, 0.4), 2.5, 5.0)
            cancellation_reason = ""
        else:
            rating = np.nan
            cancellation_reason = random.choices(
                ["Driver no-show", "Rider cancelled", "Payment issue"],
                weights=[0.5, 0.4, 0.1],
            )[0]

        driver_id = random.randint(1, 80)
        rider_id = random.randint(1, 300)

        records.append(
            {
                "ride_id": ride_id,
                "ride_datetime": ts,
                "day_of_week": ts.strftime("%A"),
                "hour_of_day": hour_of_day,
                "pickup_zone": pickup_zone,
                "drop_zone": drop_zone,
                "distance_km": round(distance_km, 2),
                "wait_time_min": round(wait_time_min, 1),
                "ride_time_min": round(ride_time_min, 1),
                "fare_amount": fare_amount,
                "is_completed": int(is_completed),
                "driver_id": driver_id,
                "rider_id": rider_id,
                "rating": round(rating, 1) if not np.isnan(rating) else "",
                "cancellation_reason": cancellation_reason,
            }
        )

        ride_id += 1

    df = pd.DataFrame(records)
    df["ride_datetime"] = df["ride_datetime"].dt.strftime("%Y-%m-%d %H:%M:%S")

    # Ensure output directory exists
    import os

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    print("=== Namma Yatri Dataset Generated ===")
    print(f"Output file: {output_path}")
    print(f"Total rides: {len(df)}")
    print(f"Completion rate: {df['is_completed'].mean() * 100:.1f}%")
    print(f"Total revenue (₹): {df[df['is_completed'] == 1]['fare_amount'].sum():,.2f}")

    return df


if __name__ == "__main__":
    generate_namma_yatri_data()


