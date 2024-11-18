# consolidation.py

from typing import Dict, Optional
import pandas as pd
from pathlib import Path
import os

from .balance_sheet_logic import BalanceSheetCombiner, format_balance_sheet
from .adjustments import AcquisitionAdjustments
from .scenario_manager import ScenarioManager

class ConsolidationWorkflow:
    def __init__(
        self,
        bs_combiner: BalanceSheetCombiner,
        adjustments: AcquisitionAdjustments,
        scenario_manager: ScenarioManager,
        output_dir: str = 'output/consolidated_balance_sheets'
    ):
        """
        Initialize the consolidation workflow.
        
        Args:
            bs_combiner: Balance sheet combiner instance
            adjustments: Acquisition adjustments instance
            scenario_manager: Scenario manager instance
            output_dir: Directory for output files
        """
        self.bs_combiner = bs_combiner
        self.adjustments = adjustments
        self.scenario_manager = scenario_manager
        self.output_dir = output_dir
        self._ensure_output_directory()
    
    def _ensure_output_directory(self) -> None:
        """Create output directory if it doesn't exist."""
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
    
    def process_scenario(
        self,
        scenario_name: str,
        intercompany_balances: Optional[Dict] = None,
        interest_rate: float = 0.05
    ) -> Dict:
        """
        Process a single scenario and generate outputs.
        
        Args:
            scenario_name: Name of the scenario to process
            intercompany_balances: Dictionary of intercompany balances to eliminate
            interest_rate: Interest rate for debt financing
            
        Returns:
            Dict containing processed balance sheet and metrics
        """
        # Set current scenario
        self.scenario_manager.set_scenario(scenario_name)
        scenario = self.scenario_manager.get_current_scenario()
        
        # Combine balance sheets
        combined_bs = self.bs_combiner.combine_balance_sheets(intercompany_balances)
        formatted_bs = format_balance_sheet(combined_bs)
        
        # Apply acquisition adjustments
        adjusted_bs = self.adjustments.apply_adjustments(formatted_bs)
        
        # Calculate financing impacts
        financing_impacts = self.adjustments.calculate_financing_impacts(
            adjusted_bs,
            debt_ratio=scenario.financing_mix['debt'],
            interest_rate=interest_rate
        )
        
        # Apply scenario-specific adjustments
        final_bs = self.scenario_manager.apply_scenario_adjustments(adjusted_bs)
        
        # Calculate metrics
        metrics = self.scenario_manager.calculate_metrics(final_bs)
        
        return {
            'balance_sheet': final_bs,
            'metrics': metrics,
            'financing_impacts': financing_impacts
        }
    
    def save_outputs(self, scenario_name: str, results: Dict) -> None:
        """
        Save scenario results to Excel file.
        
        Args:
            scenario_name: Name of the scenario
            results: Dictionary containing results to save
        """
        output_file = os.path.join(self.output_dir, f"{scenario_name}.xlsx")
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Save balance sheet
            results['balance_sheet'].to_excel(
                writer,
                sheet_name='Balance Sheet',
                index=False
            )
            
            # Save metrics
            pd.DataFrame([results['metrics']]).to_excel(
                writer,
                sheet_name='Metrics',
                index=False
            )
            
            # Save financing impacts
            pd.DataFrame([results['financing_impacts']]).to_excel(
                writer,
                sheet_name='Financing Impacts',
                index=False
            )
    
    def run_all_scenarios(
        self,
        intercompany_balances: Optional[Dict] = None,
        interest_rate: float = 0.05,
        save_output: bool = True
    ) -> Dict[str, Dict]:
        """
        Process all scenarios and optionally save results.
        
        Args:
            intercompany_balances: Dictionary of intercompany balances to eliminate
            interest_rate: Interest rate for debt financing
            save_output: Whether to save results to Excel files
            
        Returns:
            Dictionary containing results for all scenarios
        """
        results = {}
        
        for scenario_name in self.scenario_manager.scenarios.keys():
            print(f"Processing scenario: {scenario_name}")
            
            # Process scenario
            scenario_results = self.process_scenario(
                scenario_name,
                intercompany_balances,
                interest_rate
            )
            
            # Save results if requested
            if save_output:
                self.save_outputs(scenario_name, scenario_results)
            
            results[scenario_name] = scenario_results
        
        return results

def create_consolidation_workflow(
    acquirer_bs: pd.DataFrame,
    target_bs: pd.DataFrame,
    scenarios_data: Dict,
    acquisition_config: Dict,
    output_dir: str = 'output/consolidated_balance_sheets'
) -> ConsolidationWorkflow:
    """
    Helper function to create ConsolidationWorkflow instance.
    
    Args:
        acquirer_bs: Acquirer's balance sheet
        target_bs: Target's balance sheet
        scenarios_data: Dictionary of scenario configurations
        acquisition_config: Configuration for acquisition adjustments
        output_dir: Directory for output files
        
    Returns:
        Configured ConsolidationWorkflow instance
    """
    bs_combiner = BalanceSheetCombiner(acquirer_bs, target_bs)
    adjustments = AcquisitionAdjustments(acquisition_config)
    scenario_manager = ScenarioManager(scenarios_data)
    
    return ConsolidationWorkflow(
        bs_combiner,
        adjustments,
        scenario_manager,
        output_dir
    )
