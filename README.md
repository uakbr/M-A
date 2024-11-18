<p align="center">
  <img src="logo.png" alt="SynerMerge Logo" width="500"/>
</p>

## Overview
**SynerMerge** is a powerful tool designed for consolidating balance sheets during mergers and acquisitions (M&A). The model is built to handle complex acquisition adjustments, including goodwill creation, financing impacts, and synergy calculations. It supports multiple scenario simulations, enabling users to evaluate the financial impact of varying assumptions dynamically. This solution provides detailed insights into post-acquisition financials, empowering decision-makers with actionable data.

---

## Features

### Core Functionality
- **Balance Sheet Consolidation**:
  - Seamless integration of acquirer and target balance sheets.
  - Handles intercompany eliminations and ensures balancing of assets, liabilities, and equity.
- **Acquisition Adjustments**:
  - Calculation of goodwill and purchase price allocation (PPA).
  - Incorporation of transaction costs, financing impacts, and tax adjustments.
  - Synergy realization: Revenue and cost synergies dynamically applied to outputs.
- **Scenario Management**:
  - Simulate and compare base, optimistic, and pessimistic cases.
  - Adjust key variables like purchase price, financing mix, and synergy realization rates.
- **Visualization**:
  - Generate visual summaries of key metrics such as EPS accretion/dilution, leverage ratios, and consolidated financial statements.

### Outputs
- Consolidated balance sheets for multiple scenarios.
- Sensitivity analysis results for key drivers.
- Visual representations of key metrics to aid decision-making.

---

## Repository Architecture

The project is modular and designed for scalability and clarity, with the following structure:

```plaintext
M&A-Scenario-Model/
├── data/                     # Stores input data files
│   ├── balance_sheets/       # Input balance sheets for acquirer and target
│   ├── assumptions/          # Scenario and financing assumption files
│   └── synergies/            # Cost and revenue synergy inputs
├── notebooks/                # Jupyter notebooks for prototyping and validation
├── src/                      # Core Python modules for logic and data processing
│   ├── __init__.py           # Module initializer
│   ├── data_loader.py        # Functions for loading and validating input data
│   ├── balance_sheet_logic.py # Combines and adjusts balance sheets
│   ├── scenario_manager.py   # Logic for managing scenarios and sensitivity
│   ├── adjustments.py        # Goodwill, financing, and synergy adjustments
│   ├── consolidation.py      # Orchestrates balance sheet consolidation
│   └── visualization.py      # Generates charts and graphical outputs
├── output/                   # Generated outputs for scenarios
│   ├── consolidated_balance_sheets/  # Final consolidated financials
│   └── charts/               # Visualizations of key metrics
├── requirements.txt          # Dependencies required for the project
├── main.py                   # Main script to execute the full model
└── README.md                 # Project documentation
```

---

## Workflow and Architecture

### 1. **Data Loading**
- **Module**: `data_loader.py`
- **Description**: Reads input data from Excel, CSV, or JSON files. Validates balance sheet structures to ensure consistency. Key functions:
  - `load_balance_sheet(filepath)`: Loads and preprocesses balance sheets.
  - `load_scenarios(filepath)`: Parses scenario assumptions into a usable format.

### 2. **Balance Sheet Consolidation**
- **Module**: `balance_sheet_logic.py`
- **Description**: Combines acquirer and target balance sheets while eliminating intercompany accounts. Ensures the fundamental equation (`Assets = Liabilities + Equity`) holds post-consolidation. Key logic includes:
  - Adjustments for pre-acquisition liabilities.
  - Intercompany eliminations.

### 3. **Scenario Management**
- **Module**: `scenario_manager.py`
- **Description**: Dynamically adjusts inputs based on user-defined scenarios (e.g., Base Case, Optimistic, Pessimistic). Scenarios are stored in JSON format for modularity. Key functionality:
  - `apply_scenario_adjustments(data, scenario)`: Applies scenario-specific adjustments to balance sheets and assumptions.

### 4. **Acquisition Adjustments**
- **Module**: `adjustments.py`
- **Description**: Applies acquisition-specific changes, including:
  - **Goodwill Calculation**: Determines goodwill based on purchase price and net asset value.
  - **Financing Impacts**: Adjusts liabilities for debt and equity financing.
  - **Tax Adjustments**: Incorporates deferred tax liabilities and step-up amortization.
  - **Synergies**: Calculates and applies cost/revenue synergies.

### 5. **Consolidation**
- **Module**: `consolidation.py`
- **Description**: Orchestrates the balance sheet consolidation process. Combines raw inputs with scenario-specific adjustments and outputs the final consolidated financial statements.

### 6. **Visualization**
- **Module**: `visualization.py`
- **Description**: Produces visual outputs for quick insights into key metrics. Chart types include:
  - Stacked bar charts for consolidated balance sheets.
  - Line graphs for EPS accretion/dilution and leverage ratios.

### 7. **Execution**
- **Script**: `main.py`
- **Description**: The main driver script to execute the workflow. Processes inputs, applies scenarios, consolidates financials, and generates outputs.

---

## Input/Output Details

### Input Data
- **Balance Sheets**: Detailed balance sheets for acquirer and target in Excel/CSV format.
- **Scenario Assumptions**: JSON file specifying parameters for different cases.
- **Synergy Inputs**: Excel/CSV inputs detailing revenue and cost synergy assumptions.

### Outputs
- **Consolidated Financials**: Excel files for each scenario saved in `output/consolidated_balance_sheets/`.
- **Charts**: PNG files summarizing key metrics saved in `output/charts/`.

---

## Example Workflow
1. **Prepare Input Files**:
   - Place balance sheets, synergy inputs, and scenario assumptions in the `data/` directory.
2. **Run the Model**:
   - Execute the main script:
     ```bash
     python main.py
     ```
3. **Review Outputs**:
   - Consolidated financial statements: `output/consolidated_balance_sheets/`
   - Key metric visualizations: `output/charts/`

---

## Technical Highlights
- Built with Python using robust data processing libraries like `Pandas` and `NumPy`.
- Modular design ensures maintainability and extensibility for future features.
- Comprehensive handling of M&A-specific complexities such as intercompany eliminations, goodwill, and synergies.

---

For questions or enhancements, please reach out to the repository maintainer.
