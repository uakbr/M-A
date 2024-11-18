# main.py

import argparse
import pandas as pd
import numpy as np
from pathlib import Path

from src.data_loader import load_balance_sheet_csv, parse_scenarios_json
from src.balance_sheet_logic import BalanceSheetCombiner, format_balance_sheet
from src.scenario_manager import ScenarioManager
from src.adjustments import AcquisitionAdjustments, create_acquisition_config
from src.consolidation import create_consolidation_workflow
from src.visualization import create_visualization_manager

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='M&A Model - Balance Sheet Consolidation')
    
    parser.add_argument(
        '--balance-sheet',
        type=str,
        default='data/sample_balance_sheets.csv',
        help='Path to balance sheet CSV file'
    )
    
    parser.add_argument(
        '--scenarios',
        type=str,
        default='data/assumptions/scenarios.json',
        help='Path to scenarios JSON file'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='output',
        help='Directory for output files'
    )
    
    parser.add_argument(
        '--interest-rate',
        type=float,
        default=0.05,
        help='Interest rate for debt financing'
    )
    
    parser.add_argument(
        '--chart-type',
        choices=['plotly', 'matplotlib'],
        default='plotly',
        help='Type of charts to generate'
    )
    
    return parser.parse_args()

def main():
    """Main execution function."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Ensure output directory exists
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    
    print("\nLoading input data...")
    # Load sample balance sheets
    sample_bs = load_balance_sheet_csv(args.balance_sheet)
    
    # Split into acquirer and target balance sheets
    acquirer_bs = pd.DataFrame({
        'Account': sample_bs['Account'],
        'Amount': sample_bs['Acquirer']
    })
    
    target_bs = pd.DataFrame({
        'Account': sample_bs['Account'],
        'Amount': sample_bs['Target']
    })
    
    print("Loading scenarios...")
    # Load scenarios
    scenarios_data = parse_scenarios_json(args.scenarios)
    
    # Example asset step-ups and depreciation periods
    asset_step_ups = {
        'Property Plant & Equipment': 20000,
        'Inventory': 5000
    }
    
    depreciation_periods = {
        'Property Plant & Equipment': 10,
        'Inventory': 1
    }
    
    print("Creating acquisition configuration...")
    # Create acquisition configuration
    target_book_value = target_bs['Amount'].sum()
    base_scenario = scenarios_data['base_case']
    
    acq_config = create_acquisition_config(
        purchase_price=base_scenario['purchase_price'],
        target_book_value=target_book_value,
        tax_rate=base_scenario['tax_rate'],
        asset_step_ups=asset_step_ups,
        depreciation_periods=depreciation_periods
    )
    
    print("Initializing consolidation workflow...")
    # Create consolidation workflow
    workflow = create_consolidation_workflow(
        acquirer_bs=acquirer_bs,
        target_bs=target_bs,
        scenarios_data=scenarios_data,
        acquisition_config=acq_config,
        output_dir=f"{args.output_dir}/consolidated_balance_sheets"
    )
    
    # Example intercompany balances
    intercompany_balances = {
        'Accounts Receivable': 5000,
        'Accounts Payable': 5000
    }
    
    print("\nProcessing scenarios...")
    # Run all scenarios
    results = workflow.run_all_scenarios(
        intercompany_balances=intercompany_balances,
        interest_rate=args.interest_rate,
        save_output=True
    )
    
    print("\nGenerating visualizations...")
    # Create visualization manager
    viz_manager = create_visualization_manager(f"{args.output_dir}/charts")
    
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
    viz_manager.create_balance_sheet_chart(balance_sheets, args.chart_type)
    viz_manager.create_metrics_chart(metrics, args.chart_type)
    viz_manager.create_financing_impact_chart(financing_impacts, args.chart_type)
    
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
    
    print(f"\nOutputs have been saved to the {args.output_dir} directory:")
    print(f"- Consolidated balance sheets: {args.output_dir}/consolidated_balance_sheets/")
    print(f"- Visualizations: {args.output_dir}/charts/")

if __name__ == "__main__":
    main()
