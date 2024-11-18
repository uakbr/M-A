# main.py

from src.data_loader import load_balance_sheet_csv, parse_scenarios_json
from src.balance_sheet_logic import BalanceSheetCombiner, format_balance_sheet
from src.scenario_manager import ScenarioManager
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
    formatted_bs = format_balance_sheet(combined_bs)
    
    # Load scenarios
    scenarios_data = parse_scenarios_json('data/assumptions/scenarios.json')
    scenario_manager = ScenarioManager(scenarios_data)
    
    # Process each scenario
    for scenario_name in scenarios_data.keys():
        print(f"\nProcessing {scenario_name}...")
        
        # Set current scenario
        scenario_manager.set_scenario(scenario_name)
        
        # Apply scenario adjustments
        adjusted_bs = scenario_manager.apply_scenario_adjustments(formatted_bs)
        
        # Calculate metrics
        metrics = scenario_manager.calculate_metrics(adjusted_bs)
        
        # Print results
        print(f"\nAdjusted Balance Sheet ({scenario_name}):")
        print(adjusted_bs)
        print("\nKey Metrics:")
        for metric, value in metrics.items():
            print(f"{metric}: {value:.2f}")

if __name__ == "__main__":
    main()
