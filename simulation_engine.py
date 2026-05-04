import pandas as pd
import numpy as np
import joblib
import os

class SimulationEngine:
    def __init__(self, model_path=None, data_path=None):
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), 'best_model.pkl')
        if data_path is None:
            data_path = os.path.join(os.path.dirname(__file__), 'nassau_candy_data.csv')
            
        try:
            self.model = joblib.load(model_path)
        except Exception as e:
            print(f"Model load failed (likely version mismatch). Retraining... Error: {e}")
            from train_pipeline import train_and_evaluate
            train_and_evaluate()
            self.model = joblib.load(model_path)
            
        self.df = pd.read_csv(data_path)
        
        self.factories = [
            "Lot's O' Nuts", "Wicked Choccy's", "Sugar Shack", 
            "Secret Factory", "The Other Factory"
        ]
        
    def simulate_reassignment(self, product_name, region, ship_mode, current_factory):
        """Simulate reassignment to all other factories and calculate KPIs."""
        results = []
        
        # Current baseline prediction
        baseline_input = pd.DataFrame([{
            'Product Name': product_name,
            'Origin Factory': current_factory,
            'Region': region,
            'Ship Mode': ship_mode
        }])
        baseline_lead_time = self.model.predict(baseline_input)[0]
        
        # Product cost info
        prod_data = self.df[self.df['Product Name'] == product_name]
        if not prod_data.empty:
            avg_cost = prod_data['Cost'].mean() / prod_data['Units'].mean() if prod_data['Units'].mean() > 0 else 2.0
            avg_price = prod_data['Sales'].mean() / prod_data['Units'].mean() if prod_data['Units'].mean() > 0 else 5.0
        else:
            avg_cost = 2.0
            avg_price = 5.0
            
        for factory in self.factories:
            sim_input = pd.DataFrame([{
                'Product Name': product_name,
                'Origin Factory': factory,
                'Region': region,
                'Ship Mode': ship_mode
            }])
            new_lead_time = self.model.predict(sim_input)[0]
            
            # KPI calculations
            lead_time_diff = baseline_lead_time - new_lead_time
            if baseline_lead_time > 0:
                lead_time_reduction_pct = (lead_time_diff / baseline_lead_time) * 100
            else:
                lead_time_reduction_pct = 0.0
                
            # Heuristic for profit impact based on lead time (faster shipping = better margin/less penalty)
            # Assuming every day saved improves margin by 0.5%
            profit_impact_pct = lead_time_diff * 0.5
            
            # Confidence score based on historical data volume for this factory-region route
            route_data_volume = len(self.df[(self.df['Origin Factory'] == factory) & (self.df['Region'] == region)])
            confidence_score = min(100, route_data_volume / 20)  # Max 100%
            
            results.append({
                'Factory': factory,
                'Predicted Lead Time (Days)': max(0, round(new_lead_time, 2)),
                'Lead Time Reduction (%)': round(lead_time_reduction_pct, 2),
                'Profit Impact (%)': round(profit_impact_pct, 2),
                'Confidence Score (%)': round(confidence_score, 2),
                'Is Recommended': new_lead_time < baseline_lead_time
            })
            
        return pd.DataFrame(results).sort_values(by='Predicted Lead Time (Days)')
