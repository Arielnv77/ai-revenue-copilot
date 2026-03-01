"""
Generates a realistic sample dataset matching the Online Retail II schema.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

def generate_sample_data(num_rows=5000, output_path="data/sample/online_retail_sample.csv"):
    print(f"Generating {num_rows} rows of sample data...")
    np.random.seed(42)

    # 1. Generate base columns
    invoice_numbers = [f"{np.random.randint(500000, 599999)}" for _ in range(num_rows)]
    
    # Simulate ~5% cancellations (starts with 'c' or 'C')
    cancel_indices = np.random.choice(range(num_rows), size=int(num_rows * 0.05), replace=False)
    for idx in cancel_indices:
        invoice_numbers[idx] = f"C{invoice_numbers[idx]}"

    # Product Catalog
    products = {
        "85123A": ("WHITE HANGING HEART T-LIGHT HOLDER", 2.55),
        "71053": ("WHITE METAL LANTERN", 3.39),
        "84406B": ("CREAM CUPID HEARTS COAT HANGER", 2.75),
        "84029G": ("KNITTED UNION FLAG HOT WATER BOTTLE", 3.39),
        "84029E": ("RED WOOLLY HOTTIE WHITE HEART.", 3.39),
        "22752": ("SET 7 BABUSHKA NESTING BOXES", 7.65),
        "21730": ("GLASS STAR FROSTED T-LIGHT HOLDER", 4.25),
        "22632": ("HAND WARMER RED RETROSPOT", 2.10),
        "22633": ("HAND WARMER UNION JACK", 2.10),
        "21078": ("SET/20 STRAWBERRY PAPER NAPKINS", 0.85),
        "21080": ("SET/20 RED RETROSPOT PAPER NAPKINS", 0.85),
    }

    stock_codes = list(products.keys())
    chosen_stock_codes = np.random.choice(stock_codes, size=num_rows)
    
    descriptions = [products[code][0] for code in chosen_stock_codes]
    unit_prices = [products[code][1] for code in chosen_stock_codes]

    # Add some noise to unit prices to simulate discounts or price changes over time
    unit_prices = [max(0.1, price + np.random.normal(0, 0.2)) for price in unit_prices]

    # Quantities: Cancellations have negative quantities, others positive
    quantities = []
    for idx in range(num_rows):
        if invoice_numbers[idx].startswith('C'):
            quantities.append(np.random.randint(-10, -1))
        else:
            # Most orders are small, some are bulk
            if np.random.random() < 0.9:
                quantities.append(np.random.randint(1, 25))
            else:
                quantities.append(np.random.randint(50, 500))

    # Dates: Spread over 2023 - 2024
    start_date = pd.Timestamp("2023-01-01").timestamp()
    end_date = pd.Timestamp("2024-12-31").timestamp()
    
    # Use exponential distribution to simulate clustered buying (holidays/weekends)
    timestamps = np.random.uniform(start_date, end_date, size=num_rows)
    timestamps.sort() # chronological order
    invoice_dates = [datetime.fromtimestamp(ts) for ts in timestamps]

    # Customers (~1000 unique customers)
    customer_ids = np.random.choice(range(12000, 18000), size=num_rows)
    
    # Introduce ~10% missing CustomerIDs to simulate guest checkouts
    missing_indices = np.random.choice(range(num_rows), size=int(num_rows * 0.1), replace=False)
    customer_ids = customer_ids.astype(float) # allow NaNs
    customer_ids[missing_indices] = np.nan

    # Countries (Heavy bias to UK)
    countries = ["United Kingdom", "Germany", "France", "EIRE", "Spain", "Netherlands", "Belgium", "Switzerland", "Portugal", "Australia"]
    probs = [0.85, 0.03, 0.03, 0.02, 0.02, 0.01, 0.01, 0.01, 0.01, 0.01]
    chosen_countries = np.random.choice(countries, size=num_rows, p=probs)

    # 2. Build DataFrame
    df = pd.DataFrame({
        "InvoiceNo": invoice_numbers,
        "StockCode": chosen_stock_codes,
        "Description": descriptions,
        "Quantity": quantities,
        "InvoiceDate": invoice_dates,
        "UnitPrice": np.round(unit_prices, 2),
        "CustomerID": customer_ids,
        "Country": chosen_countries
    })

    # Format customer IDs (no decimals)
    df["CustomerID"] = df["CustomerID"].astype("Int64")
    
    # 3. Save
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"✅ Success! Sample dataset saved to: {out_path.absolute()}")
    print("Columns generated:", df.columns.tolist())

if __name__ == "__main__":
    generate_sample_data()
