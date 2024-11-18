### Detailed Project Objective

The M&A model consolidates balance sheets for acquiring and target companies under multiple scenarios, facilitating scenario-based sensitivity analysis and decision-making. The model integrates acquisition adjustments like goodwill creation, financing impacts, and synergies, providing a comprehensive view of post-acquisition financials. Scenario management capabilities allow users to assess various acquisition structures, financing mixes, and synergy realizations dynamically. Outputs include consolidated balance sheets, key financial metrics, and visualized insights into the impact of different assumptions.

---

## **Instructions.md**

### Phase 1: Core Setup
1. **File:** `requirements.txt`
   - Add dependencies: `pandas`, `numpy`, `openpyxl`, `xlwings`, `matplotlib`, `plotly`.
2. **File:** `README.md`
   - Document installation instructions, project overview, and structure.
3. Initialize the repository structure and placeholders for all files.

---

### Phase 2: Data Input Handling
1. **File:** `src/data_loader.py`
   - Write functions to load balance sheets from `Excel` and `CSV`.
   - Parse scenario assumptions from a `JSON` file.
2. **File:** `data/sample_balance_sheets.csv`
   - Create a sample dataset for testing purposes.

---

### Phase 3: Balance Sheet Combination Logic
1. **File:** `src/balance_sheet_logic.py`
   - Combine acquirer and target financials.
   - Eliminate intercompany balances.
   - Ensure `assets = liabilities + equity`.

---

### Phase 4: Scenario Management
1. **File:** `src/scenario_manager.py`
   - Develop methods to switch between scenarios dynamically.
   - Integrate logic to handle adjustments for each scenario.

---

### Phase 5: Acquisition Adjustments
1. **File:** `src/adjustments.py`
   - Implement:
     - Goodwill calculation (purchase price allocation).
     - Financing adjustments (debt and equity impacts).
     - Tax and depreciation changes due to step-ups.

---

### Phase 6: Consolidation Workflow
1. **File:** `src/consolidation.py`
   - Orchestrate the steps to consolidate balance sheets.
   - Apply adjustments, scenarios, and synergies.
   - Output final financials to `Excel`.

---

### Phase 7: Visualization and Outputs
1. **File:** `src/visualization.py`
   - Create visualizations for:
     - Consolidated balance sheets (stacked bar charts).
     - Key financial metrics (EPS accretion/dilution, leverage ratios).
2. **File:** `output/consolidated_balance_sheets/`
   - Save outputs for each scenario.

---

### Phase 8: Prototype and Testing
1. **File:** `notebooks/exploratory_analysis.ipynb`
   - Validate input data, test logic for small datasets.
2. **File:** `notebooks/scenario_simulations.ipynb`
   - Simulate and debug outputs.

---

### Phase 9: Documentation and Validation
1. **File:** `README.md`
   - Expand documentation for usage instructions and assumptions.
2. Integrate checks in each script to ensure inputs balance.

---

### Phase 10: Final Integration and Execution
1. **File:** `main.py`
   - Combine all modules.
   - Create a command-line interface for executing the full workflow.
   - Produce final outputs and charts.

---