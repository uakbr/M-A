# data_loader.py

import pandas as pd
import json
import os

def load_balance_sheet_excel(file_path):
    """
    Load balance sheet data from an Excel file.
    """
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        return df
    else:
        raise FileNotFoundError(f"File not found: {file_path}")

def load_balance_sheet_csv(file_path):
    """
    Load balance sheet data from a CSV file.
    """
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df
    else:
        raise FileNotFoundError(f"File not found: {file_path}")

def parse_scenarios_json(file_path):
    """
    Parse scenario assumptions from a JSON file.
    """
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    else:
        raise FileNotFoundError(f"File not found: {file_path}")
