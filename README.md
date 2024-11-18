# M&A Model

The M&A model consolidates balance sheets for acquiring and target companies under multiple scenarios, facilitating scenario-based sensitivity analysis and decision-making. The model integrates acquisition adjustments like goodwill creation, financing impacts, and synergies, providing a comprehensive view of post-acquisition financials. Scenario management capabilities allow users to assess various acquisition structures, financing mixes, and synergy realizations dynamically. Outputs include consolidated balance sheets, key financial metrics, and visualized insights into the impact of different assumptions.

## Installation

To set up the project, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ma-model.git
   ```

2. **Navigate to the project directory:**
   ```bash
   cd ma-model
   ```

3. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
M&A-Model/
│
├── data/
│   ├── balance_sheets/
│   │   ├── acquirer_balance_sheet.xlsx
│   │   ├── target_balance_sheet.xlsx
│   │   └── sample_balance_sheets.csv
│   ├── assumptions/
│   │   ├── scenarios.json
│   │   └── financing_options.csv
│   └── synergies/
│       └── synergy_inputs.xlsx
│
├── notebooks/
│   ├── exploratory_analysis.ipynb
│   └── scenario_simulations.ipynb
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py       # Load input data
│   ├── balance_sheet_logic.py
│   ├── scenario_manager.py  # Scenario setup and switching
│   ├── adjustments.py       # Goodwill, financing, synergy adjustments
│   ├── consolidation.py     # Final consolidation logic
│   └── visualization.py     # Charts and outputs
│
├── output/
│   ├── consolidated_balance_sheets/
│   │   ├── base_case.xlsx
│   │   ├── optimistic_case.xlsx
│   │   └── pessimistic_case.xlsx
│   └── charts/
│       ├── leverage_ratios.png
│       └── eps_accretion_dilution.png
│
├── requirements.txt
├── main.py
└── README.md
```

---

### Description of Files and Folders

#### 1. **data/**
   - Stores all input data required for the model.
   - Subfolders organize data by type:
     - **balance_sheets/**: Balance sheets of acquirer and target.
     - **assumptions/**: M&A transaction assumptions, financing mix, etc.
     - **synergies/**: Inputs for synergy calculations.

#### 2. **notebooks/**
   - Jupyter notebooks for testing and prototyping.
   - Includes:
     - `exploratory_analysis.ipynb`: Analyze balance sheets, validate data.
     - `scenario_simulations.ipynb`: Run and visualize multiple scenarios.

#### 3. **src/**
   - Core Python modules for the project:
     - **`data_loader.py`**: Functions to read input data from Excel, CSV, or JSON.
     - **`balance_sheet_logic.py`**: Logic for combining and adjusting balance sheets.
     - **`scenario_manager.py`**: Handles scenario switching and sensitivity analysis.
     - **`adjustments.py`**: Functions for Goodwill, financing impacts, and synergies.
     - **`consolidation.py`**: Consolidates balance sheets into a single output.
     - **`visualization.py`**: Generates charts for scenario comparisons.

#### 4. **output/**
   - Stores the results and outputs of the model:
     - Consolidated financials for different scenarios.
     - Visualizations for key metrics like leverage ratios and EPS accretion/dilution.

#### 5. **requirements.txt**
   - Lists all Python dependencies (e.g., Pandas, NumPy, Matplotlib, Plotly, OpenPyXL).

#### 6. **main.py**
   - The main execution script to run the M&A model. Orchestrates data loading, scenario management, and output generation.

#### 7. **README.md**
   - Detailed project documentation:
     - Project overview.
     - Step-by-step instructions for setting up and running the model.
     - Explanation of each input and output.

---
