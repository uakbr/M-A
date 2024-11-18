# data_loader.py

import pandas as pd
import json
import os
from typing import Dict, Any

def validate_balance_sheet_structure(df: pd.DataFrame) -> None:
    """
    Validate the structure of a balance sheet DataFrame.
    
    Args:
        df: Balance sheet DataFrame to validate
        
    Raises:
        ValueError: If required columns or accounts are missing
    """
    required_columns = {'Account', 'Amount'} if len(df.columns) == 2 else {'Account', 'Acquirer', 'Target'}
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"Balance sheet must contain columns: {required_columns}")
    
    required_accounts = {
        'Cash and Cash Equivalents',
        'Accounts Receivable',
        'Inventory',
        'Property Plant & Equipment',
        'Goodwill',
        'Accounts Payable',
        'Short-Term Debt',
        'Long-Term Debt',
        'Shareholders\' Equity'
    }
    
    missing_accounts = required_accounts - set(df['Account'])
    if missing_accounts:
        raise ValueError(f"Missing required accounts: {missing_accounts}")

def validate_scenarios_structure(data: Dict[str, Any]) -> None:
    """
    Validate the structure of scenarios data.
    
    Args:
        data: Scenarios dictionary to validate
        
    Raises:
        ValueError: If required fields or structure is missing
    """
    required_fields = {
        'purchase_price',
        'financing_mix',
        'synergies',
        'transaction_costs',
        'tax_rate'
    }
    
    financing_fields = {'debt', 'equity'}
    synergy_fields = {'cost_savings', 'revenue_growth'}
    
    for scenario, config in data.items():
        missing_fields = required_fields - set(config.keys())
        if missing_fields:
            raise ValueError(f"Scenario '{scenario}' missing required fields: {missing_fields}")
        
        # Validate financing mix
        if not all(field in config['financing_mix'] for field in financing_fields):
            raise ValueError(f"Scenario '{scenario}' missing required financing mix fields")
        
        # Validate financing mix sums to 1
        if not abs(sum(config['financing_mix'].values()) - 1.0) < 1e-6:
            raise ValueError(f"Financing mix in scenario '{scenario}' must sum to 1.0")
        
        # Validate synergies
        if not all(field in config['synergies'] for field in synergy_fields):
            raise ValueError(f"Scenario '{scenario}' missing required synergy fields")
        
        # Validate numeric fields
        if not isinstance(config['purchase_price'], (int, float)):
            raise ValueError(f"Purchase price in scenario '{scenario}' must be numeric")
        if not isinstance(config['tax_rate'], (int, float)):
            raise ValueError(f"Tax rate in scenario '{scenario}' must be numeric")
        if not 0 <= config['tax_rate'] <= 1:
            raise ValueError(f"Tax rate in scenario '{scenario}' must be between 0 and 1")

def load_balance_sheet_excel(file_path: str) -> pd.DataFrame:
    """
    Load and validate balance sheet data from an Excel file.
    
    Args:
        file_path: Path to Excel file
        
    Returns:
        Validated balance sheet DataFrame
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If data structure is invalid
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    df = pd.read_excel(file_path)
    validate_balance_sheet_structure(df)
    return df

def load_balance_sheet_csv(file_path: str) -> pd.DataFrame:
    """
    Load and validate balance sheet data from a CSV file.
    
    Args:
        file_path: Path to CSV file
        
    Returns:
        Validated balance sheet DataFrame
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If data structure is invalid
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    df = pd.read_csv(file_path)
    validate_balance_sheet_structure(df)
    return df

def parse_scenarios_json(file_path: str) -> Dict[str, Any]:
    """
    Parse and validate scenario assumptions from a JSON file.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Validated scenarios dictionary
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If data structure is invalid
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    validate_scenarios_structure(data)
    return data
