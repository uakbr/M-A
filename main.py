# main.py

from src.data_loader import load_balance_sheet_csv, parse_scenarios_json
from src.balance_sheet_logic import BalanceSheetCombiner, format_balance_sheet
from src.scenario_manager import ScenarioManager
from src.adjustments import AcquisitionAdjustments, create_acquisition_config
from src.consolidation import create_consolidation_workflow
from src.visualization import create_visualization_manager
import pandas as pd
import numpy as np

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
    formatted_bs = format_balance_sheet(combined_bs)
    
    # Calculate target book value from sample balance sheet
    target_book_value = sample_bs['Target'].sum()
    
    # Example asset step-ups and depreciation periods
    asset_step_ups = {
        'Property Plant & Equipment': 20000,  # Step up PP&E by 20,000
        'Inventory': 5000                     # Step up inventory by 5,000
    }
    
    depreciation_periods = {
        'Property Plant & Equipment': 10,  # 10-year depreciation for PP&E
        'Inventory': 1                     # 1-year depreciation for inventory
    }
    
    # Create acquisition configuration
    acq_config = create_acquisition_config(
        purchase_price=150000,            # From scenarios.json base case
        target_book_value=target_book_value,
        tax_rate=0.25,                    # From scenarios.json
        asset_step_ups=asset_step_ups,
        depreciation_periods=depreciation_periods
    )
    
    # Initialize acquisition adjustments
    adjustments = AcquisitionAdjustments(acq_config)
    
    # Load scenarios
    scenarios_data = parse_scenarios_json('data/assumptions/scenarios.json')
    scenario_manager = ScenarioManager(scenarios_data)
    
    # Create consolidation workflow
    workflow = create_consolidation_workflow(
        acquirer_bs=acquirer_bs,
        target_bs=target_bs,
        scenarios_data=scenarios_data,
        acquisition_config=acq_config
    )
    
    # Run all scenarios
    results = workflow.run_all_scenarios(
        intercompany_balances=intercompany_balances,
        interest_rate=0.05,
        save_output=True
    )
    
    # Create visualization manager
    viz_manager = create_visualization_manager()
    
    # Prepare data for visualization
    balance_sheets = {
        scenario_name: scenario_results['balance_sheet']
        for scenario_name, scenario_results in results.items()
    }
    
    metrics = {
        scenario_name: scenario_results['metrics']
        for scenario_name, scenario_results in results.items()
    }
    
    financing_impacts = {
        scenario_name: scenario_results['financing_impacts']
        for scenario_name, scenario_results in results.items()
    }
    
    # Create visualizations
    viz_manager.create_balance_sheet_chart(balance_sheets)
    viz_manager.create_metrics_chart(metrics)
    viz_manager.create_financing_impact_chart(financing_impacts)
    
    print("\nConsolidation Complete!")
    print("\nScenario Summaries:")
    for scenario_name, scenario_results in results.items():
        print(f"\n{scenario_name}:")
        print("Key Metrics:")
        for metric, value in scenario_results['metrics'].items():
            print(f"  {metric}: {value:.2f}")
        print("Financing Impacts:")
        for impact, value in scenario_results['financing_impacts'].items():
            print(f"  {impact}: {value:,.2f}")
    
    print("\nVisualizations have been created in the output/charts directory.")

if __name__ == "__main__":
    main()
