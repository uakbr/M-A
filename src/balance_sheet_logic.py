# balance_sheet_logic.py

import pandas as pd
import numpy as np
from typing import Dict, Tuple

class BalanceSheetCombiner:
    def __init__(self, acquirer_bs: pd.DataFrame, target_bs: pd.DataFrame):
        """
        Initialize the balance sheet combiner with acquirer and target balance sheets.
        
        Args:
            acquirer_bs (pd.DataFrame): Acquirer's balance sheet
            target_bs (pd.DataFrame): Target's balance sheet
        """
        self.acquirer_bs = acquirer_bs
        self.target_bs = target_bs
        self.validate_balance_sheets()

    def validate_balance_sheets(self) -> None:
        """
        Validate that both balance sheets are balanced 
        (Assets = Liabilities + Equity).
        
        Raises:
            ValueError: If balance sheets don't balance
        """
        def calculate_totals(df: pd.DataFrame) -> Tuple[float, float]:
            assets = df[df['Account'].isin([
                'Cash and Cash Equivalents',
                'Accounts Receivable',
                'Inventory',
                'Property Plant & Equipment',
                'Goodwill'
            ])]['Amount'].sum()
            
            liab_equity = df[df['Account'].isin([
                'Accounts Payable',
                'Short-Term Debt',
                'Long-Term Debt',
                'Shareholders\' Equity'
            ])]['Amount'].sum()
            
            return assets, liab_equity

        # Check Acquirer's balance sheet
        acq_assets, acq_liab_equity = calculate_totals(self.acquirer_bs)
        if not np.isclose(acq_assets, acq_liab_equity, rtol=1e-5):
            raise ValueError("Acquirer's balance sheet is not balanced")

        # Check Target's balance sheet
        target_assets, target_liab_equity = calculate_totals(self.target_bs)
        if not np.isclose(target_assets, target_liab_equity, rtol=1e-5):
            raise ValueError("Target's balance sheet is not balanced")

    def combine_balance_sheets(self, intercompany_balances: Dict = None) -> pd.DataFrame:
        """
        Combine acquirer and target balance sheets, eliminating intercompany balances.
        
        Args:
            intercompany_balances (Dict): Dictionary of intercompany balances to eliminate
                Example: {'Accounts Receivable': 1000, 'Accounts Payable': 1000}
        
        Returns:
            pd.DataFrame: Combined balance sheet
        """
        # Create a copy of balance sheets
        combined_bs = pd.DataFrame(columns=['Account', 'Amount'])
        
        # Combine all accounts
        for account in self.acquirer_bs['Account'].unique():
            acquirer_amount = self.acquirer_bs[
                self.acquirer_bs['Account'] == account
            ]['Amount'].iloc[0]
            
            target_amount = self.target_bs[
                self.target_bs['Account'] == account
            ]['Amount'].iloc[0]
            
            # Eliminate intercompany balances if provided
            if intercompany_balances and account in intercompany_balances:
                combined_amount = acquirer_amount + target_amount - intercompany_balances[account]
            else:
                combined_amount = acquirer_amount + target_amount
            
            combined_bs = pd.concat([
                combined_bs,
                pd.DataFrame({
                    'Account': [account],
                    'Amount': [combined_amount]
                })
            ], ignore_index=True)
        
        return combined_bs

    def verify_combined_balance_sheet(self, combined_bs: pd.DataFrame) -> bool:
        """
        Verify that the combined balance sheet maintains the accounting equation:
        Assets = Liabilities + Equity
        
        Args:
            combined_bs (pd.DataFrame): Combined balance sheet to verify
            
        Returns:
            bool: True if balanced, False otherwise
        """
        # Calculate total assets
        total_assets = combined_bs[
            combined_bs['Account'].isin([
                'Cash and Cash Equivalents',
                'Accounts Receivable',
                'Inventory',
                'Property Plant & Equipment',
                'Goodwill'
            ])
        ]['Amount'].sum()
        
        # Calculate total liabilities and equity
        total_liab_equity = combined_bs[
            combined_bs['Account'].isin([
                'Accounts Payable',
                'Short-Term Debt',
                'Long-Term Debt',
                'Shareholders\' Equity'
            ])
        ]['Amount'].sum()
        
        return np.isclose(total_assets, total_liab_equity, rtol=1e-5)

def format_balance_sheet(df: pd.DataFrame) -> pd.DataFrame:
    """
    Format the balance sheet for display or export.
    
    Args:
        df (pd.DataFrame): Balance sheet to format
        
    Returns:
        pd.DataFrame: Formatted balance sheet
    """
    # Define the order of accounts
    account_order = [
        'Cash and Cash Equivalents',
        'Accounts Receivable',
        'Inventory',
        'Property Plant & Equipment',
        'Goodwill',
        'Accounts Payable',
        'Short-Term Debt',
        'Long-Term Debt',
        'Shareholders\' Equity'
    ]
    
    # Sort the balance sheet according to the defined order
    df['Account'] = pd.Categorical(df['Account'], categories=account_order, ordered=True)
    formatted_df = df.sort_values('Account').reset_index(drop=True)
    
    return formatted_df
