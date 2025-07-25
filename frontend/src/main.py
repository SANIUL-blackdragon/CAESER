```python
import streamlit as st
import requests
import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
API_BASE_URL = "http://localhost:8000"  # Update to Heroku URL after deployment
st.set_page_config(page_title="CÆSER Dashboard", layout="wide")

# Custom CSS
st.markdown("""
    <style>
        .market-selector__dropdown { margin-bottom: 1rem; }
        .insight-visualizer__chart { max-width: 100%; }
        .prediction-dashboard__container { padding: 1rem; background-color: #f9f9f9; border-radius: 8px; }
        .product-keywords__input { width: 100%; }
        .product-description__textarea { width: 100%; min-height: 100px; }
        @media (max-width: 768px) {
            .market-selector__dropdown { font-size: 14px; }
            .insight-visualizer__chart { height: 300px; }
        }
        :root {
            --primary-color: #667eea;
            --text-color: #333;
        }
        .stButton>button { background-color: var(--primary-color); color: white; }
    </style>
""", unsafe_allow_html=True)

# MarketSelector Component
def market_selector():
    st.subheader("Select Market and Category")
    col1, col2 = st.columns(2)
    with col1:
        location = st.selectbox("Location", ["New York, NY", "London", "Tokyo"], key="location")
    with col2:
        category = st.selectbox("Category", ["sneakers", "electronics", "fashion"], key="category")
    insight_type = st.selectbox("Insight Type", ["brand", "demographics", "heatmap"], key="insight_type")
    return location, category, insight_type

# ProductKeywords Component
def product_keywords():
    st.subheader("Product Keywords")
    keywords = st.text_input("Enter keywords (comma-separated)", help="e.g., sneakers, streetwear")
    return [k.strip() for k in keywords.split(",") if k.strip()] if keywords else []

# ProductDescription Component
def product_description():
    st.subheader("Product Description")
    description = st.text_area("Enter product description")
    return description.strip() if description else ""

# InsightVisualizer Component
def insight_visualizer(insights, insight_type):
    st.subheader("Cultural Insights")
    if not insights or not insights.get("success"):
        st.error("Failed to fetch cultural insights. Please try again.")
        return
    
    try:
        entities = insights["data"].get("entities", [])
        if insight_type == "brand":
            df = pd.DataFrame([
                {"trait": entity["name"], "score": entity["properties"].get("popularity", 0.5)}
                for entity in entities
            ])
            fig = px.bar(df, x="trait", y="score", title="Cultural Affinity Scores",
                         color_discrete_sequence=["#667eea"])
            st.plotly_chart(fig, use_container_width=True)
        
        elif insight_type == "demographics":
            df = pd.DataFrame([
                {"age_group": entity.get("age_group", "Unknown"), "affinity": entity.get("affinity_score", 0.5)}
                for entity in entities
            ])
            fig = px.bar(df, x="age_group", y="affinity", title="Demographic Affinity",
                         color_discrete_sequence=["#764ba2"])
            st.plotly_chart(fig, use_container_width=True)
        
        elif insight_type == "heatmap":
            # Mock heatmap data (replace with real Qloo heatmap data if available)
            z = [[0.8, 0.6, 0.9], [0.7, 0.85, 0.75], [0.9, 0.8, 0.95]]
            fig = go.Figure(data=go.Heatmap(
                z=z,
                x=["North America", "Europe", "Asia"],
                y=["Fashion", "Electronics", "Home"],
                colorscale="Viridis"
            ))
            fig.update_layout(title="Regional Affinity Heatmap")
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        logger.error(f"Error rendering insights: {str(e)}")
        st.error(f"Error rendering insights: {str(e)}")

# PredictionDashboard Component
def prediction_dashboard(predictions, hype_score):
    st.subheader("Demand Predictions and Strategies")
    if not predictions or not predictions.get("success"):
        st.error("Failed to generate predictions. Please try again.")
        return
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Demand Uplift", f"{predictions['data'].get('uplift', 'Unknown')}%")
        st.metric("Hype Score", f"{hype_score.get('averageScore', 'Unknown')}")
    with col2:
        st.write("**Recommended Strategy**")
        st.write(predictions["data"].get("strategy", "Unknown"))
    
    # Demand Line Chart
    df = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Demand": [120, 190, 300, 500, 200, 300]
    })
    fig = px.line(df, x="Month", y="Demand", title="Demand Trends",
                  color_discrete_sequence=["#667eea"])
    st.plotly_chart(fig, use_container_width=True)

# Main App Logic
def main():
    st.title("CÆSER: Cultural Affinity Simulation Engine for Retail")
    
    # Collect inputs
    location, category, insight_type = market_selector()
    keywords = product_keywords()
    description = product_description()
    
    # Submit button
    if st.button("Generate Insights and Predictions", key="submit"):
        with st.spinner("Fetching insights and predictions..."):
            try:
                # Fetch cultural insights
                insights_response = requests.get(
                    f"{API_BASE_URL}/insights/{location}/{category}?insight_type={insight_type}",
                    timeout=10
                )
                insights = insights_response.json() if insights_response.status_code == 200 else {}
                
                # Fetch predictions
                product = {
                    "name": ", ".join(keywords) or category,
                    "category": category,
                    "description": description or f"{category} product"
                }
                prediction_payload = {"product": product, "insights": insights}
                prediction_response = requests.post(
                    f"{API_BASE_URL}/predict/demand",
                    json=prediction_payload,
                    timeout=10
                )
                predictions = prediction_response.json() if prediction_response.status_code == 200 else {}
                
                # Calculate hype score
                hype_score = requests.post(
                    f"{API_BASE_URL}/hype/score",
                    json={"insights": insights},
                    timeout=10
                ).json()
                
                # Display results
                insight_visualizer(insights, insight_type)
                prediction_dashboard(predictions, hype_score)
                
                # Send Discord alert
                discord_payload = {"prediction": {"product": product, **predictions.get("data", {})}, "hype_data": hype_score}
                requests.post(f"{API_BASE_URL}/discord/alert", json=discord_payload, timeout=5)
                
            except requests.RequestException as e:
                logger.error(f"API request failed: {str(e)}")
                st.error(f"API request failed: {str(e)}")
            except Exception as e:
                logger.error(f"An error occurred: {str(e)}")
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
```