# frontend/src/main.py
import streamlit as st
import requests
import json
import plotly.express as px
import pandas as pd

# Configuration
API_BASE_URL = "http://localhost:8000"  # Update to Heroku URL after deployment
st.set_page_config(page_title="CÆSER Dashboard", layout="wide")

# Custom CSS for responsiveness and theme
st.markdown("""
    <style>
        /* BEM naming convention */
        .market-selector__dropdown { margin-bottom: 1rem; }
        .insight-visualizer__chart { max-width: 100%; }
        .prediction-dashboard__container { padding: 1rem; background-color: #f9f9f9; border-radius: 8px; }
        .product-keywords__input { width: 100%; }
        .product-description__textarea { width: 100%; min-height: 100px; }
        /* Mobile responsiveness */
        @media (max-width: 768px) {
            .market-selector__dropdown { font-size: 14px; }
            .insight-visualizer__chart { height: 300px; }
        }
        /* Theme variables */
        :root {
            --primary-color: #1a73e8;
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
        location = st.selectbox("Location", ["New York, NY", "London", "Tokyo"], key="location", help="Choose a target market")
    with col2:
        category = st.selectbox("Category", ["sneakers", "electronics", "fashion"], key="category", help="Choose a product category")
    return location, category

# ProductKeywords Component
def product_keywords():
    st.subheader("Product Keywords")
    keywords = st.text_input("Enter keywords (comma-separated)", help="e.g., sneakers, streetwear, limited edition")
    return [k.strip() for k in keywords.split(",") if k.strip()] if keywords else []

# ProductDescription Component
def product_description():
    st.subheader("Product Description")
    description = st.text_area("Enter product description", help="Provide a detailed description of the product")
    return description.strip() if description else ""

# InsightVisualizer Component
def insight_visualizer(insights):
    st.subheader("Cultural Insights")
    if not insights or not insights.get("success"):
        st.error("Failed to fetch cultural insights. Please try again.")
        return
    try:
        # Example: Plot affinity scores
        data = insights["data"]["results"]["entities"]
        df = pd.DataFrame([
            {"trait": entity["name"], "score": entity["properties"]["popularity"]}
            for entity in data
        ])
        fig = px.bar(df, x="trait", y="score", title="Cultural Affinity Scores")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error rendering insights: {str(e)}")

# PredictionDashboard Component
def prediction_dashboard(predictions):
    st.subheader("Demand Predictions and Strategies")
    if not predictions or predictions.get("uplift") == "Unknown":
        st.error("Failed to generate predictions. Please try again.")
        return
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Demand Uplift", predictions.get("uplift", "Unknown"))
    with col2:
        st.write("**Recommended Strategy**")
        st.write(predictions.get("strategy", "Unknown"))

# Main App Logic
def main():
    st.title("CÆSER: Cultural Affinity Simulation Engine for Retail")
    
    # Collect inputs
    location, category = market_selector()
    keywords = product_keywords()
    description = product_description()
    
    # Submit button
    if st.button("Generate Insights and Predictions", key="submit"):
        with st.spinner("Fetching insights and predictions..."):
            try:
                # Fetch cultural insights
                insights_response = requests.get(
                    f"{API_BASE_URL}/insights/{location}/{category}",
                    timeout=10
                )
                insights = insights_response.json() if insights_response.status_code == 200 else {}
                
                # Fetch predictions
                prediction_payload = {
                    "product": f"{category} ({', '.join(keywords)}): {description}",
                    "insights": insights.get("data", {})
                }
                prediction_response = requests.post(
                    f"{API_BASE_URL}/predict/demand",
                    json=prediction_payload,
                    timeout=10
                )
                predictions = prediction_response.json() if prediction_response.status_code == 200 else {}
                
                # Display results
                insight_visualizer(insights)
                prediction_dashboard(predictions)
                
                # Send Discord alert
                discord_payload = {"prediction": predictions, "insights": insights}
                requests.post(f"{API_BASE_URL}/discord/alert", json=discord_payload)
                
            except requests.RequestException as e:
                st.error(f"API request failed: {str(e)}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()