# scenario_manager.py

import pandas as pd
from typing import Dict, Optional, Any
from dataclasses import dataclass

@dataclass
class ScenarioConfig:
    """Data class to hold scenario configuration"""
    purchase_price: float
    financing_mix: Dict[str, float]
    synergies: Dict[str, float]
    transaction_costs: float
    tax_rate: float

class ScenarioManager:
    def __init__(self, scenarios_data: Dict[str, Dict[str, Any]]):
        """
        Initialize the scenario manager with scenario data.
        
        Args:
            scenarios_data (Dict): Dictionary containing scenario configurations
        """
        self.scenarios = {}
        self.current_scenario = None
        self._load_scenarios(scenarios_data)

    def _load_scenarios(self, scenarios_data: Dict[str, Dict[str, Any]]) -> None:
        """
        Load scenarios from input data into ScenarioConfig objects.
        
        Args:
            scenarios_data (Dict): Dictionary containing scenario configurations
        """
        for scenario_name, config in scenarios_data.items():
            self.scenarios[scenario_name] = ScenarioConfig(
                purchase_price=config['purchase_price'],
                financing_mix=config['financing_mix'],
                synergies=config['synergies'],
                transaction_costs=config['transaction_costs'],
                tax_rate=config['tax_rate']
            )

    def set_scenario(self, scenario_name: str) -> None:
        """
        Set the current active scenario.
        
        Args:
            scenario_name (str): Name of the scenario to activate
            
        Raises:
            ValueError: If scenario_name doesn't exist
        """
        if scenario_name not in self.scenarios:
            raise ValueError(f"Scenario '{scenario_name}' not found")
        self.current_scenario = scenario_name

    def get_current_scenario(self) -> Optional[ScenarioConfig]:
        """
        Get the current scenario configuration.
        
        Returns:
            ScenarioConfig: Current scenario configuration or None if no scenario is set
        """
        if self.current_scenario is None:
            return None
        return self.scenarios[self.current_scenario]

    def apply_scenario_adjustments(self, combined_bs: pd.DataFrame) -> pd.DataFrame:
        """
        Apply scenario-specific adjustments to the combined balance sheet.
        
        Args:
            combined_bs (pd.DataFrame): Combined balance sheet before adjustments
            
        Returns:
            pd.DataFrame: Adjusted balance sheet based on current scenario
            
        Raises:
            ValueError: If no scenario is currently set
        """
        if self.current_scenario is None:
            raise ValueError("No scenario currently set")

        scenario = self.get_current_scenario()
        adjusted_bs = combined_bs.copy()

        # Apply financing mix adjustments
        debt_financing = scenario.purchase_price * scenario.financing_mix['debt']
        equity_financing = scenario.purchase_price * scenario.financing_mix['equity']

        # Update debt and equity accounts
        debt_idx = adjusted_bs['Account'] == 'Long-Term Debt'
        equity_idx = adjusted_bs['Account'] == 'Shareholders\' Equity'

        adjusted_bs.loc[debt_idx, 'Amount'] += debt_financing
        adjusted_bs.loc[equity_idx, 'Amount'] += equity_financing

        # Apply transaction costs (typically reduces cash)
        cash_idx = adjusted_bs['Account'] == 'Cash and Cash Equivalents'
        adjusted_bs.loc[cash_idx, 'Amount'] -= scenario.transaction_costs

        # Apply synergies impact (simplified - adds to cash)
        total_synergies = scenario.synergies['cost_savings'] + scenario.synergies['revenue_growth']
        adjusted_bs.loc[cash_idx, 'Amount'] += total_synergies

        return adjusted_bs

    def calculate_metrics(self, adjusted_bs: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate key financial metrics for the current scenario.
        
        Args:
            adjusted_bs (pd.DataFrame): Adjusted balance sheet
            
        Returns:
            Dict[str, float]: Dictionary of calculated metrics
        """
        total_assets = adjusted_bs[
            adjusted_bs['Account'].isin([
                'Cash and Cash Equivalents',
                'Accounts Receivable',
                'Inventory',
                'Property Plant & Equipment',
                'Goodwill'
            ])
        ]['Amount'].sum()

        total_debt = adjusted_bs[
            adjusted_bs['Account'].isin([
                'Short-Term Debt',
                'Long-Term Debt'
            ])
        ]['Amount'].sum()

        equity = adjusted_bs[
            adjusted_bs['Account'] == 'Shareholders\' Equity'
        ]['Amount'].sum()

        return {
            'leverage_ratio': total_debt / equity,
            'debt_to_assets': total_debt / total_assets,
            'equity_to_assets': equity / total_assets
        }
