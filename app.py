import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from simulation_engine import SimulationEngine

# Configure Streamlit page
st.set_page_config(
    page_title="Nassau Candy - Intelligent Reallocation",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern glassmorphism and typography
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    /* Modern metrics cards */
    div[data-testid="metric-container"] {
        background-color: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 5% 5% 5% 10%;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Headers styling */
    h1, h2, h3 {
        color: #f8fafc;
        font-weight: 700;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        color: #f8fafc;
    }
    
    .stAlert {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.title("🏭 Nassau Candy Factory Reallocation Engine")
st.markdown("Intelligent decision-making dashboard for optimizing factory-product assignments.")

# Load Data and Model
@st.cache_resource
def load_engine():
    data_path = os.path.join(os.path.dirname(__file__), 'nassau_candy_data.csv')
    model_path = os.path.join(os.path.dirname(__file__), 'best_model.pkl')
    
    if not os.path.exists(data_path) or not os.path.exists(model_path):
        return None
    return SimulationEngine(model_path, data_path)

engine = load_engine()

if engine is None:
    st.error("Model or data not found. Please run the training pipeline first.")
    st.stop()

df = engine.df

# --- SIDEBAR CONTROLS ---
st.sidebar.header("⚙️ Simulation Controls")

products = df['Product Name'].unique().tolist()
regions = df['Region'].unique().tolist()
ship_modes = df['Ship Mode'].unique().tolist()
factories = df['Origin Factory'].unique().tolist()

selected_product = st.sidebar.selectbox("Select Product", products)
selected_region = st.sidebar.selectbox("Destination Region", regions)
selected_ship_mode = st.sidebar.selectbox("Ship Mode", ship_modes)
current_factory = st.sidebar.selectbox("Current Origin Factory", factories)

st.sidebar.markdown("---")
priority = st.sidebar.select_slider(
    "Optimization Priority",
    options=["Speed (Lead Time)", "Balanced", "Profit (Margin)"],
    value="Balanced"
)

# --- SIMULATION EXECUTION ---
with st.spinner("Running intelligent simulations..."):
    sim_results = engine.simulate_reassignment(
        selected_product, selected_region, selected_ship_mode, current_factory
    )

current_stats = sim_results[sim_results['Factory'] == current_factory].iloc[0]
recommended_factory_row = sim_results.iloc[0]

# --- TOP METRICS PANEL ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Current Lead Time", 
        value=f"{current_stats['Predicted Lead Time (Days)']} Days"
    )
with col2:
    st.metric(
        label="Best Lead Time", 
        value=f"{recommended_factory_row['Predicted Lead Time (Days)']} Days",
        delta=f"-{current_stats['Predicted Lead Time (Days)'] - recommended_factory_row['Predicted Lead Time (Days)']:.1f} Days" if recommended_factory_row['Predicted Lead Time (Days)'] < current_stats['Predicted Lead Time (Days)'] else "0 Days",
        delta_color="inverse"
    )
with col3:
    st.metric(
        label="Est. Profit Impact", 
        value=f"+{recommended_factory_row['Profit Impact (%)']}%" if recommended_factory_row['Profit Impact (%)'] > 0 else f"{recommended_factory_row['Profit Impact (%)']}%"
    )
with col4:
    st.metric(
        label="Scenario Confidence", 
        value=f"{recommended_factory_row['Confidence Score (%)']}%"
    )


st.markdown("---")

# --- MAIN DASHBOARD LAYOUT ---
row1_col1, row1_col2 = st.columns([2, 1])

with row1_col1:
    st.subheader("📊 What-If Scenario Analysis")
    st.markdown("Compare the predicted lead time across all available manufacturing locations.")
    
    # Bar chart comparing lead times
    fig = px.bar(
        sim_results, 
        x='Factory', 
        y='Predicted Lead Time (Days)',
        color='Predicted Lead Time (Days)',
        color_continuous_scale='blues_r',
        text='Predicted Lead Time (Days)'
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis_title="Manufacturing Facility",
        yaxis_title="Predicted Lead Time (Days)"
    )
    # Highlight current factory
    fig.add_shape(
        type="rect",
        x0=-0.5 + sim_results['Factory'].tolist().index(current_factory),
        x1=0.5 + sim_results['Factory'].tolist().index(current_factory),
        y0=0,
        y1=current_stats['Predicted Lead Time (Days)'],
        line=dict(color="red", width=2, dash="dash"),
        fillcolor="rgba(255,0,0,0.1)",
    )
    st.plotly_chart(fig, use_container_width=True)

with row1_col2:
    st.subheader("💡 Recommendation Dashboard")
    
    if recommended_factory_row['Factory'] != current_factory:
        st.success(f"**Action Recommended:** Reassign to {recommended_factory_row['Factory']}")
        st.write(f"Moving production of **{selected_product}** for the **{selected_region}** region from **{current_factory}** to **{recommended_factory_row['Factory']}** is expected to yield:")
        st.write(f"- **{recommended_factory_row['Lead Time Reduction (%)']}%** Lead Time Reduction")
        st.write(f"- **{recommended_factory_row['Profit Impact (%)']}%** Positive Margin Impact")
    else:
        st.info(f"**Current Assignment Optimal:** {current_factory}")
        st.write("The current origin factory provides the best balance of speed and efficiency for this region.")

    st.subheader("⚠️ Risk & Impact Panel")
    if recommended_factory_row['Confidence Score (%)'] < 50:
        st.warning("Low confidence score. Reassignment relies on limited historical data for this route.")
    if recommended_factory_row['Profit Impact (%)'] < 0:
        st.error("Warning: Expected negative profit impact. Proceed with caution.")
    if recommended_factory_row['Profit Impact (%)'] >= 0 and recommended_factory_row['Confidence Score (%)'] >= 50:
        st.success("Safe execution parameters. High confidence and positive/neutral profit impact.")


st.markdown("---")

# --- GEOSPATIAL VISUALIZATION ---
st.subheader("🗺️ Factory Geographic Distribution")

FACTORIES_COORDS = {
    "Lot's O' Nuts": {"lat": 32.881893, "lon": -111.768036},
    "Wicked Choccy's": {"lat": 32.076176, "lon": -81.088371},
    "Sugar Shack": {"lat": 48.11914, "lon": -96.18115},
    "Secret Factory": {"lat": 41.446333, "lon": -90.565487},
    "The Other Factory": {"lat": 35.1175, "lon": -89.971107}
}

map_data = []
for fac in sim_results['Factory']:
    row = sim_results[sim_results['Factory'] == fac].iloc[0]
    map_data.append({
        'Factory': fac,
        'Latitude': FACTORIES_COORDS[fac]['lat'],
        'Longitude': FACTORIES_COORDS[fac]['lon'],
        'Lead Time': row['Predicted Lead Time (Days)'],
        'Recommended': "Best Option" if fac == recommended_factory_row['Factory'] else "Alternate"
    })

map_df = pd.DataFrame(map_data)

fig_map = px.scatter_mapbox(
    map_df, 
    lat="Latitude", 
    lon="Longitude", 
    hover_name="Factory",
    hover_data=["Lead Time"],
    color="Recommended",
    size_max=15,
    zoom=3, 
    mapbox_style="carto-darkmatter"
)
fig_map.update_traces(marker=dict(size=12))
fig_map.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig_map, use_container_width=True)
