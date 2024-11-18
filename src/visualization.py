# visualization.py

import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from typing import Dict, List
from pathlib import Path

class VisualizationManager:
    def __init__(self, output_dir: str = 'output/charts'):
        """
        Initialize visualization manager.
        
        Args:
            output_dir: Directory to save generated charts
        """
        self.output_dir = output_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    def create_balance_sheet_chart(
        self,
        balance_sheets: Dict[str, pd.DataFrame],
        chart_type: str = 'plotly'
    ) -> None:
        """
        Create stacked bar chart comparing balance sheets across scenarios.
        
        Args:
            balance_sheets: Dictionary of balance sheets by scenario
            chart_type: Type of chart to create ('plotly' or 'matplotlib')
        """
        if chart_type == 'plotly':
            self._create_plotly_balance_sheet_chart(balance_sheets)
        else:
            self._create_mpl_balance_sheet_chart(balance_sheets)
    
    def _create_plotly_balance_sheet_chart(self, balance_sheets: Dict[str, pd.DataFrame]) -> None:
        """Create interactive balance sheet chart using Plotly."""
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Assets', 'Liabilities & Equity'),
            specs=[[{'type': 'bar'}, {'type': 'bar'}]]
        )
        
        asset_accounts = [
            'Cash and Cash Equivalents',
            'Accounts Receivable',
            'Inventory',
            'Property Plant & Equipment',
            'Goodwill'
        ]
        
        liab_equity_accounts = [
            'Accounts Payable',
            'Short-Term Debt',
            'Long-Term Debt',
            'Shareholders\' Equity'
        ]
        
        colors = plt.cm.Set3(np.linspace(0, 1, max(len(asset_accounts), len(liab_equity_accounts))))
        
        for scenario_name, bs in balance_sheets.items():
            # Assets
            asset_values = [
                bs[bs['Account'] == account]['Amount'].iloc[0]
                for account in asset_accounts
            ]
            fig.add_trace(
                go.Bar(
                    name=scenario_name,
                    x=asset_accounts,
                    y=asset_values,
                    marker_color=colors
                ),
                row=1, col=1
            )
            
            # Liabilities & Equity
            liab_equity_values = [
                bs[bs['Account'] == account]['Amount'].iloc[0]
                for account in liab_equity_accounts
            ]
            fig.add_trace(
                go.Bar(
                    name=scenario_name,
                    x=liab_equity_accounts,
                    y=liab_equity_values,
                    marker_color=colors
                ),
                row=1, col=2
            )
        
        fig.update_layout(
            title='Balance Sheet Comparison Across Scenarios',
            barmode='group',
            height=600
        )
        
        fig.write_html(os.path.join(self.output_dir, 'balance_sheet_comparison.html'))
    
    def create_metrics_chart(
        self,
        metrics: Dict[str, Dict[str, float]],
        chart_type: str = 'plotly'
    ) -> None:
        """
        Create charts for key financial metrics across scenarios.
        
        Args:
            metrics: Dictionary of metrics by scenario
            chart_type: Type of chart to create ('plotly' or 'matplotlib')
        """
        if chart_type == 'plotly':
            self._create_plotly_metrics_chart(metrics)
        else:
            self._create_mpl_metrics_chart(metrics)
    
    def _create_plotly_metrics_chart(self, metrics: Dict[str, Dict[str, float]]) -> None:
        """Create interactive metrics chart using Plotly."""
        scenarios = list(metrics.keys())
        metric_names = list(metrics[scenarios[0]].keys())
        
        fig = make_subplots(rows=len(metric_names), cols=1,
                          subplot_titles=metric_names)
        
        for i, metric in enumerate(metric_names, 1):
            values = [metrics[scenario][metric] for scenario in scenarios]
            fig.add_trace(
                go.Bar(x=scenarios, y=values, name=metric),
                row=i, col=1
            )
        
        fig.update_layout(
            height=300 * len(metric_names),
            title_text="Financial Metrics Comparison",
            showlegend=False
        )
        
        fig.write_html(os.path.join(self.output_dir, 'metrics_comparison.html'))
    
    def create_financing_impact_chart(
        self,
        financing_impacts: Dict[str, Dict[str, float]],
        chart_type: str = 'plotly'
    ) -> None:
        """
        Create charts showing financing impacts across scenarios.
        
        Args:
            financing_impacts: Dictionary of financing impacts by scenario
            chart_type: Type of chart to create ('plotly' or 'matplotlib')
        """
        if chart_type == 'plotly':
            self._create_plotly_financing_chart(financing_impacts)
        else:
            self._create_mpl_financing_chart(financing_impacts)
    
    def _create_plotly_financing_chart(
        self,
        financing_impacts: Dict[str, Dict[str, float]]
    ) -> None:
        """Create interactive financing impact chart using Plotly."""
        scenarios = list(financing_impacts.keys())
        impact_types = list(financing_impacts[scenarios[0]].keys())
        
        fig = go.Figure()
        
        for impact in impact_types:
            values = [financing_impacts[scenario][impact] for scenario in scenarios]
            fig.add_trace(go.Bar(
                name=impact,
                x=scenarios,
                y=values
            ))
        
        fig.update_layout(
            title='Financing Impacts Across Scenarios',
            barmode='group',
            height=500
        )
        
        fig.write_html(os.path.join(self.output_dir, 'financing_impacts.html'))

def create_visualization_manager(output_dir: str = 'output/charts') -> VisualizationManager:
    """
    Helper function to create VisualizationManager instance.
    
    Args:
        output_dir: Directory to save generated charts
        
    Returns:
        Configured VisualizationManager instance
    """
    return VisualizationManager(output_dir)
