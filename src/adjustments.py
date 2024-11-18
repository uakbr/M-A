# adjustments.py

from dataclasses import dataclass
from typing import Dict, Optional
import pandas as pd
import numpy as np

@dataclass
class AcquisitionConfig:
    """Configuration for acquisition adjustments"""
    purchase_price: float
    target_book_value: float
    tax_rate: float
    asset_step_ups: Dict[str, float]
    depreciation_periods: Dict[str, int]

class AcquisitionAdjustments:
    def __init__(self, config: AcquisitionConfig):
        """
        Initialize acquisition adjustments calculator.
        
        Args:
            config (AcquisitionConfig): Configuration for adjustments
        """
        self.config = config
        
    def calculate_goodwill(self) -> float:
        """
        Calculate goodwill as the difference between purchase price and
        adjusted book value (including step-ups).
        
        Returns:
            float: Calculated goodwill amount
        """
        total_step_ups = sum(self.config.asset_step_ups.values())
        adjusted_book_value = self.config.target_book_value + total_step_ups
        goodwill = self.config.purchase_price - adjusted_book_value
        return max(goodwill, 0)  # Goodwill cannot be negative
        
    def calculate_step_up_impacts(self) -> Dict[str, float]:
        """
        Calculate tax and depreciation impacts of asset step-ups.
        
        Returns:
            Dict[str, float]: Dictionary containing annual depreciation and tax impacts
        """
        annual_depreciation = {}
        for asset, step_up in self.config.asset_step_ups.items():
            if asset in self.config.depreciation_periods:
                period = self.config.depreciation_periods[asset]
                annual_depreciation[asset] = step_up / period
            else:
                annual_depreciation[asset] = 0
                
        total_annual_depreciation = sum(annual_depreciation.values())
        tax_shield = total_annual_depreciation * self.config.tax_rate
        
        return {
            'annual_depreciation': annual_depreciation,
            'total_annual_depreciation': total_annual_depreciation,
            'tax_shield': tax_shield
        }
    
    def apply_adjustments(self, balance_sheet: pd.DataFrame) -> pd.DataFrame:
        """
        Apply all acquisition adjustments to the balance sheet.
        
        Args:
            balance_sheet (pd.DataFrame): Original balance sheet
            
        Returns:
            pd.DataFrame: Adjusted balance sheet
        """
        adjusted_bs = balance_sheet.copy()
        
        # Calculate and add goodwill
        goodwill = self.calculate_goodwill()
        goodwill_idx = adjusted_bs['Account'] == 'Goodwill'
        adjusted_bs.loc[goodwill_idx, 'Amount'] += goodwill
        
        # Apply asset step-ups
        for asset, step_up in self.config.asset_step_ups.items():
            asset_idx = adjusted_bs['Account'] == asset
            if any(asset_idx):
                adjusted_bs.loc[asset_idx, 'Amount'] += step_up
        
        # Calculate deferred tax liability from step-ups
        total_step_ups = sum(self.config.asset_step_ups.values())
        deferred_tax = total_step_ups * self.config.tax_rate
        
        # Add deferred tax liability (create new row if doesn't exist)
        if 'Deferred Tax Liability' not in adjusted_bs['Account'].values:
            adjusted_bs = pd.concat([
                adjusted_bs,
                pd.DataFrame({
                    'Account': ['Deferred Tax Liability'],
                    'Amount': [deferred_tax]
                })
            ], ignore_index=True)
        else:
            dtl_idx = adjusted_bs['Account'] == 'Deferred Tax Liability'
            adjusted_bs.loc[dtl_idx, 'Amount'] += deferred_tax
            
        return adjusted_bs
    
    def calculate_financing_impacts(
        self,
        balance_sheet: pd.DataFrame,
        debt_ratio: float,
        interest_rate: float
    ) -> Dict[str, float]:
        """
        Calculate the impact of acquisition financing.
        
        Args:
            balance_sheet (pd.DataFrame): Balance sheet
            debt_ratio (float): Portion of purchase price funded by debt
            interest_rate (float): Annual interest rate on debt
            
        Returns:
            Dict[str, float]: Financing impacts including interest expense and tax effects
        """
        debt_financing = self.config.purchase_price * debt_ratio
        annual_interest = debt_financing * interest_rate
        tax_shield = annual_interest * self.config.tax_rate
        
        return {
            'debt_financing': debt_financing,
            'annual_interest': annual_interest,
            'interest_tax_shield': tax_shield,
            'net_interest_cost': annual_interest - tax_shield
        }

def create_acquisition_config(
    purchase_price: float,
    target_book_value: float,
    tax_rate: float,
    asset_step_ups: Optional[Dict[str, float]] = None,
    depreciation_periods: Optional[Dict[str, int]] = None
) -> AcquisitionConfig:
    """Helper function to create AcquisitionConfig with default values.
    
    Args:
        purchase_price (float): Total purchase price
        target_book_value (float): Book value of target company
        tax_rate (float): Applicable tax rate
        asset_step_ups (Dict[str, float], optional): Asset step-up values
        depreciation_periods (Dict[str, int], optional): Depreciation periods for stepped-up assets
        
    Returns:
        AcquisitionConfig: Configuration object for acquisition adjustments
    """
    return AcquisitionConfig(
        purchase_price=purchase_price,
        target_book_value=target_book_value,
        tax_rate=tax_rate,
        asset_step_ups=asset_step_ups or {},
        depreciation_periods=depreciation_periods or {}
    )
