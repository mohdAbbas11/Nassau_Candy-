import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Factories Data
FACTORIES = {
    "Lot's O' Nuts": {"lat": 32.881893, "lon": -111.768036},
    "Wicked Choccy's": {"lat": 32.076176, "lon": -81.088371},
    "Sugar Shack": {"lat": 48.11914, "lon": -96.18115},
    "Secret Factory": {"lat": 41.446333, "lon": -90.565487},
    "The Other Factory": {"lat": 35.1175, "lon": -89.971107}
}

PRODUCTS = [
    {"Product ID": "PROD-001", "Product Name": "Chocolate Almonds", "Division": "Nuts", "Cost": 2.50},
    {"Product ID": "PROD-002", "Product Name": "Gummy Bears", "Division": "Candy", "Cost": 1.20},
    {"Product ID": "PROD-003", "Product Name": "Sour Worms", "Division": "Candy", "Cost": 1.30},
    {"Product ID": "PROD-004", "Product Name": "Peanut Butter Cups", "Division": "Chocolate", "Cost": 3.00},
    {"Product ID": "PROD-005", "Product Name": "Jelly Beans", "Division": "Candy", "Cost": 1.50},
    {"Product ID": "PROD-006", "Product Name": "Dark Chocolate Truffles", "Division": "Chocolate", "Cost": 5.00},
    {"Product ID": "PROD-007", "Product Name": "Cashew Clusters", "Division": "Nuts", "Cost": 4.00},
    {"Product ID": "PROD-008", "Product Name": "Lollipops", "Division": "Candy", "Cost": 0.50},
    {"Product ID": "PROD-009", "Product Name": "Caramel Squares", "Division": "Chocolate", "Cost": 2.80},
    {"Product ID": "PROD-010", "Product Name": "Pistachios", "Division": "Nuts", "Cost": 4.50}
]

REGIONS = ["East", "West", "Central", "South"]
SHIP_MODES = ["Standard Class", "Second Class", "First Class", "Same Day"]

def generate_mock_data(num_records=5000):
    np.random.seed(42)
    random.seed(42)
    
    data = []
    start_date = datetime(2023, 1, 1)
    
    factory_names = list(FACTORIES.keys())
    
    for i in range(1, num_records + 1):
        product = random.choice(PRODUCTS)
        factory = random.choice(factory_names)
        region = random.choice(REGIONS)
        ship_mode = random.choice(SHIP_MODES)
        
        order_date = start_date + timedelta(days=random.randint(0, 365))
        
        # Base lead time calculation based on ship mode
        base_days = {"Standard Class": 5, "Second Class": 3, "First Class": 1, "Same Day": 0}[ship_mode]
        
        # Add noise and variance based on factory and region
        # e.g., West to East takes longer
        factory_idx = factory_names.index(factory)
        region_idx = REGIONS.index(region)
        variance = abs(factory_idx - region_idx) * 1.5 + np.random.normal(0, 1)
        
        lead_time_days = max(0, int(base_days + variance))
        ship_date = order_date + timedelta(days=lead_time_days)
        
        units = random.randint(10, 500)
        sales = units * product["Cost"] * random.uniform(1.5, 3.0) # markup
        gross_profit = sales - (units * product["Cost"])
        
        record = {
            "Row ID": i,
            "Order ID": f"ORD-2023-{10000+i}",
            "Order Date": order_date.strftime("%Y-%m-%d"),
            "Ship Date": ship_date.strftime("%Y-%m-%d"),
            "Ship Mode": ship_mode,
            "Customer ID": f"CUST-{random.randint(100, 999)}",
            "Country/Region": "United States",
            "City": f"City_{random.randint(1, 50)}",
            "State/Province": f"State_{random.randint(1, 20)}",
            "Postal Code": f"{random.randint(10000, 99999)}",
            "Division": product["Division"],
            "Region": region,
            "Product ID": product["Product ID"],
            "Product Name": product["Product Name"],
            "Origin Factory": factory,
            "Sales": round(sales, 2),
            "Units": units,
            "Gross Profit": round(gross_profit, 2),
            "Cost": round(product["Cost"] * units, 2)
        }
        data.append(record)
        
    df = pd.DataFrame(data)
    
    # Save to CSV
    output_path = os.path.join(os.path.dirname(__file__), 'nassau_candy_data.csv')
    df.to_csv(output_path, index=False)
    print(f"Generated {num_records} records and saved to {output_path}")

if __name__ == "__main__":
    generate_mock_data(5000)
