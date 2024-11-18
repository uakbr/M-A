# main.py

from src.data_loader.py import (
    load_balance_sheet_excel,
    load_balance_sheet_csv,
    parse_scenarios_json
)

def main():
    # Load sample balance sheets from CSV
    bs_csv_path = 'data/sample_balance_sheets.csv'
    balance_sheet_df = load_balance_sheet_csv(bs_csv_path)
    print("Balance Sheet Data:")
    print(balance_sheet_df)

    # Assuming we have Excel files available
    # acquirer_bs_excel = 'data/balance_sheets/acquirer_balance_sheet.xlsx'
    # target_bs_excel = 'data/balance_sheets/target_balance_sheet.xlsx'
    # acquirer_df = load_balance_sheet_excel(acquirer_bs_excel)
    # target_df = load_balance_sheet_excel(target_bs_excel)

    # Load scenario assumptions
    scenarios_json_path = 'data/assumptions/scenarios.json'
    scenarios = parse_scenarios_json(scenarios_json_path)
    print("\nScenarios Data:")
    print(scenarios)

if __name__ == "__main__":
    main()
