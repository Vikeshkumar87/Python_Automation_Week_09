"""
Task 4: API Caller
==================
Retrieves customer data from the JSONPlaceholder public API, flattens
the nested JSON using pandas, and exports the result to CSV and Excel.

Dependencies:
    pip install requests pandas openpyxl

Usage:
    python api_caller.py
"""

import os
import sys
from datetime import datetime

import requests
import pandas as pd

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
API_URL    = "https://jsonplaceholder.typicode.com/users"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


# ---------------------------------------------------------------------------
# Step 1: Fetch Data
# ---------------------------------------------------------------------------
def fetch_customers(url: str) -> list:
    """Call the API and return the parsed JSON list."""
    print(f"Calling API: {url}")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("[ERROR] Network error — check your internet connection.")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out after 15 seconds.")
        sys.exit(1)
    except requests.exceptions.HTTPError as exc:
        print(f"[ERROR] HTTP error: {exc}")
        sys.exit(1)

    data = response.json()
    print(f"Received {len(data)} customer record(s).")
    return data


# ---------------------------------------------------------------------------
# Step 2: Flatten Nested JSON
# ---------------------------------------------------------------------------
def flatten_record(user: dict) -> dict:
    """Convert a single nested user record into a flat dictionary."""
    addr = user.get("address", {})
    geo  = addr.get("geo", {})
    comp = user.get("company", {})

    return {
        "id":                  user.get("id"),
        "name":                user.get("name"),
        "username":            user.get("username"),
        "email":               user.get("email"),
        "phone":               user.get("phone"),
        "website":             user.get("website"),
        "address_street":      addr.get("street"),
        "address_suite":       addr.get("suite"),
        "address_city":        addr.get("city"),
        "address_zipcode":     addr.get("zipcode"),
        "geo_lat":             geo.get("lat"),
        "geo_lng":             geo.get("lng"),
        "company_name":        comp.get("name"),
        "company_catchphrase": comp.get("catchPhrase"),
        "company_bs":          comp.get("bs"),
    }


def build_dataframe(raw_data: list) -> pd.DataFrame:
    """Flatten all records and return a pandas DataFrame."""
    records = [flatten_record(user) for user in raw_data]
    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# Step 3: Display Summary
# ---------------------------------------------------------------------------
def display_summary(df: pd.DataFrame) -> None:
    """Print a quick summary of the flattened DataFrame."""
    print("\n" + "=" * 60)
    print(f"  DataFrame Shape : {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"  Columns         : {', '.join(df.columns.tolist())}")
    print("=" * 60)
    print("\nFirst 3 rows:\n")
    # Print in a readable transposed format
    print(df.head(3).T.to_string())
    print()


# ---------------------------------------------------------------------------
# Step 4: Export to CSV and Excel
# ---------------------------------------------------------------------------
def export_files(df: pd.DataFrame, output_dir: str) -> tuple:
    """Save the DataFrame to timestamped CSV and Excel files."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp  = datetime.now().strftime("%Y%m%d_%H%M%S")

    csv_path   = os.path.join(output_dir, f"customers_{timestamp}.csv")
    excel_path = os.path.join(output_dir, f"customers_{timestamp}.xlsx")

    df.to_csv(csv_path,   index=False, encoding="utf-8")
    df.to_excel(excel_path, index=False, engine="openpyxl")

    print(f"Exported CSV   → {csv_path}")
    print(f"Exported Excel → {excel_path}")
    return csv_path, excel_path


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    raw_data = fetch_customers(API_URL)
    df       = build_dataframe(raw_data)
    display_summary(df)
    export_files(df, OUTPUT_DIR)
    print("\nDone!")
