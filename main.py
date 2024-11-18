# main.py

from src.data_loader import load_balance_sheet_csv, parse_scenarios_json
from src.balance_sheet_logic import BalanceSheetCombiner, format_balance_sheet
import pandas as pd

def main():
    # Load sample balance sheets
    sample_bs = load_balance_sheet_csv('data/sample_balance_sheets.csv')
    
    # Split into acquirer and target balance sheets
    acquirer_bs = pd.DataFrame({
        'Account': sample_bs['Account'],
        'Amount': sample_bs['Acquirer']
    })
    
    target_bs = pd.DataFrame({
        'Account': sample_bs['Account'],
        'Amount': sample_bs['Target']
    })
    
    # Create balance sheet combiner instance
    bs_combiner = BalanceSheetCombiner(acquirer_bs, target_bs)
    
    # Example intercompany balances (if any exist)
    intercompany_balances = {
        'Accounts Receivable': 5000,
        'Accounts Payable': 5000
    }
    
    # Combine balance sheets
    combined_bs = bs_combiner.combine_balance_sheets(intercompany_balances)
    
    # Format the combined balance sheet
    formatted_bs = format_balance_sheet(combined_bs)
    
    # Verify the combined balance sheet
    is_balanced = bs_combiner.verify_combined_balance_sheet(formatted_bs)
    
    # Print results
    print("\nCombined Balance Sheet:")
    print(formatted_bs)
    print(f"\nBalance Sheet is balanced: {is_balanced}")
    
    # Calculate and print totals
    total_assets = formatted_bs[formatted_bs['Account'].isin([
        'Cash and Cash Equivalents',
        'Accounts Receivable',
        'Inventory',
        'Property Plant & Equipment',
        'Goodwill'
    ])]['Amount'].sum()
    
    total_liab_equity = formatted_bs[formatted_bs['Account'].isin([
        'Accounts Payable',
        'Short-Term Debt',
        'Long-Term Debt',
        'Shareholders\' Equity'
    ])]['Amount'].sum()
    
    print(f"\nTotal Assets: {total_assets:,.2f}")
    print(f"Total Liabilities + Equity: {total_liab_equity:,.2f}")

if __name__ == "__main__":
    main()
