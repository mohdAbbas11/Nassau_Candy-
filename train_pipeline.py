import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import os

def load_data(filepath):
    df = pd.read_csv(filepath)
    # Calculate Lead Time in days
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days
    
    # Target variable: Lead Time
    # Features specified: Product ID (or Name), Origin Factory, Region, Ship Mode
    # I'll use Product Name, Origin Factory, Region, Ship Mode
    features = ['Product Name', 'Origin Factory', 'Region', 'Ship Mode']
    target = 'Lead Time'
    
    X = df[features]
    y = df[target]
    return X, y, df

def build_pipeline(model):
    categorical_features = ['Product Name', 'Origin Factory', 'Region', 'Ship Mode']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('model', model)])
    return pipeline

def train_and_evaluate():
    data_path = os.path.join(os.path.dirname(__file__), 'nassau_candy_data.csv')
    X, y, df = load_data(data_path)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest Regressor': RandomForestRegressor(n_estimators=100, random_state=42),
        'Gradient Boosting Regressor': GradientBoostingRegressor(n_estimators=100, random_state=42)
    }
    
    best_model_name = None
    best_model_pipeline = None
    best_score = float('inf') # lower RMSE is better
    
    results = []
    
    for name, model in models.items():
        print(f"Training {name}...")
        pipeline = build_pipeline(model)
        pipeline.fit(X_train, y_train)
        
        y_pred = pipeline.predict(X_test)
        
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        results.append({
            'Model': name,
            'RMSE': rmse,
            'MAE': mae,
            'R2': r2
        })
        print(f"{name} - RMSE: {rmse:.4f}, MAE: {mae:.4f}, R2: {r2:.4f}")
        
        if rmse < best_score:
            best_score = rmse
            best_model_name = name
            best_model_pipeline = pipeline
            
    print(f"Best Model Selected: {best_model_name} with RMSE {best_score:.4f}")
    
    # Save the best model
    model_path = os.path.join(os.path.dirname(__file__), 'best_model.pkl')
    joblib.dump(best_model_pipeline, model_path)
    print(f"Model saved to {model_path}")
    
    # Route & Product Clustering
    # We will identify congested routes by grouping and finding average lead time
    route_stats = df.groupby(['Origin Factory', 'Region', 'Product Name'])['Lead Time'].mean().reset_index()
    route_stats = route_stats.sort_values(by='Lead Time', ascending=False)
    route_stats.to_csv(os.path.join(os.path.dirname(__file__), 'route_clusters.csv'), index=False)
    print("Route clustering stats saved.")
    
    return results

if __name__ == "__main__":
    train_and_evaluate()
