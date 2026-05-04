# 🏭 Nassau Candy - Intelligent Logistics Optimization

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4+-F7931E.svg)](https://scikit-learn.org/)
[![Status](https://img.shields.io/badge/Status-Production_Ready-success.svg)]()

## 📌 Overview
The **Nassau Candy Factory Reallocation Engine** is a data-driven intelligence platform designed to optimize supply chain logistics. By transitioning from static assignment rules to predictive machine learning models, this system dynamically recommends optimal factory-product assignments. This reduces shipping lead times, maximizes operational efficiency, and preserves profit margins.

---

## 🚀 Key Features
- **Predictive Inference Engine:** Leverages Gradient Boosting and Random Forest algorithms to accurately predict shipping lead times based on product, origin factory, destination region, and shipping mode.
- **Scenario Simulation Dashboard:** An interactive, glassmorphism-styled Streamlit web application that visualizes current performance versus alternative factory assignments.
- **Intelligent Recommendations:** Automatically ranks factory assignments based on expected Lead Time Reduction (%) and Est. Profit Impact (%).
- **Risk Mitigation:** Alerts operators to scenarios with low historical data confidence or negative profit outlooks.
- **Geospatial Analytics:** Interactive 3D map views of optimal routing from factory origins to destinations.

---

## 🛠️ Technology Stack
- **Core Logistics:** Python, Pandas, Numpy
- **Machine Learning:** Scikit-Learn, Joblib
- **Web Application & UI:** Streamlit, Vanilla CSS
- **Data Visualization:** Plotly (Express & Graph Objects)

---

## 📂 Project Structure
```text
📦 project1
 ┣ 📜 app.py                  # Main Streamlit web application dashboard
 ┣ 📜 simulation_engine.py    # Core logic calculating KPIs & predicting impact
 ┣ 📜 train_pipeline.py       # Data preprocessing & ML training pipeline
 ┣ 📜 generate_mock_data.py   # Synthesizes 5,000+ realistic operational records
 ┣ 📜 run_project.bat         # 1-click batch script to run the entire project
 ┣ 📜 requirements.txt        # Python dependency manifest
 ┣ 📜 research_paper.md       # Methodological approach & EDA analysis
 ┣ 📜 executive_summary.md    # High-level business impact overview
 ┗ 📜 README.md               # Project documentation (this file)
```

---

## ⚡ Installation & Execution

We have provided an automated batch script to seamlessly generate data, train the models, and launch the application.

### 1. Install Dependencies
Ensure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 2. Run the Full Pipeline
Simply execute the `run_project.bat` script from your command prompt or double-click it in your file explorer:
```cmd
.\run_project.bat
```

**What the script does automatically:**
1. Generates the initial mock datasets (`generate_mock_data.py`).
2. Trains the ML models and exports `best_model.pkl` (`train_pipeline.py`).
3. Launches the web application dashboard at `http://localhost:8501`.

*(Alternatively, you can run these steps sequentially in your terminal.)*

---

## 📊 Analytics & Documentation
This project contains detailed analytics reports targeted for both technical and executive audiences.
- Review **[research_paper.md](research_paper.md)** for a deep dive into data encoding, RMSE/R² evaluation metrics, and route clustering methodologies.
- Review **[executive_summary.md](executive_summary.md)** for a strategic overview of KPIs, operational gains, and government/stakeholder reporting.

---

## 👥 Authors & Acknowledgments
Developed by **Antigravity AI**.
Designed for Nassau Candy Distributor Logistics Optimization Initiative.
