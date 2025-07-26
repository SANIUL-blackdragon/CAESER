import streamlit as st
import requests
import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table
import openpyxl
from io import BytesIO
import logging
from api.utils.logging import setup_logging
import sqlite3
import os
import sys
import pandas as pd
from datetime import datetime

# Add scrapers directory to path for Google Trends import
sys.path.append('../scrapers')
from google_trends import get_google_trends, store_trend

logger = setup_logging()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_BASE_URL = "http://localhost:8000"  # Update to Heroku URL after deployment
DB_PATH = os.getenv("DB_PATH", "./data/caeser.db")
st.set_page_config(page_title="CÆSER Dashboard", layout="wide")

st.markdown("""
    <style>
        .market-selector__dropdown { margin-bottom: 1rem; }
        .insight-visualizer__chart { max-width: 100%; }
        .prediction-dashboard__container { padding: 1rem; background-color: #f9f9f9; border-radius: 8px; }
        .product-keywords__input { width: 100%; }
        .product-description__textarea { width: 100%; min-height: 100px; }
        .data-quality__widget { background-color: #f0f0f0; padding: 1rem; border-radius: 8px; }
        .tabs-container { margin-top: 2rem; }
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

def init_store_table():
    """Initialize the store_data table if it doesn't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS store_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT,
            sales REAL,
            date TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def user_provided_store_data():
    """Widget for uploading store data via CSV"""
    st.subheader("Upload Store Data")
    uploaded_file = st.file_uploader("Choose a CSV file (product, sales, date)", type="csv")
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            if not all(col in df.columns for col in ['product', 'sales', 'date']):
                st.error("CSV must contain columns: product, sales, date")
                return
                
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            for _, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO store_data (product, sales, date, timestamp)
                    VALUES (?, ?, ?, ?)
                """, (row['product'], row['sales'], row['date'], datetime.now().isoformat()))
                
            conn.commit()
            conn.close()
            st.success(f"Successfully uploaded {len(df)} store records")
            
            # Display uploaded data
            st.dataframe(df.head())
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

def fetch_and_display_trends():
    """Widget for Google Trends search"""
    st.subheader("Google Trends Search")
    keywords_input = st.text_input("Enter keywords (comma-separated, e.g., sneakers, boots):")
    
    if st.button("Fetch Trends"):
        if not keywords_input:
            st.error("Please enter at least one keyword")
            return
            
        keywords = [kw.strip() for kw in keywords_input.split(",")]
        with st.spinner("Fetching Google Trends data..."):
            try:
                trends = get_google_trends(keywords)
                if not trends:
                    st.warning("No trends data found")
                    return
                    
                # Store trends in database
                for keyword, interest in trends.items():
                    store_trend(keyword, interest)
                
                st.success("Trends fetched and stored successfully")
                
                # Display trends data
                trends_df = pd.DataFrame({
                    "Keyword": list(trends.keys()),
                    "Interest": list(trends.values()),
                    "Source": "google_trends",
                    "Timestamp": datetime.now().isoformat()
                })
                st.dataframe(trends_df)
                
            except Exception as e:
                st.error(f"Error fetching trends: {str(e)}")

def market_selector():
    st.subheader("Select Market and Category")
    col1, col2, col3 = st.columns(3)
    with col1:
        location = st.selectbox("Location", ["New York, NY", "London", "Tokyo"], key="location")
    with col2:
        category = st.selectbox("Category", ["sneakers", "electronics", "fashion"], key="category")
    with col3:
        threshold = st.number_input("Hype Change Threshold (%)", min_value=0.0, max_value=100.0, value=20.0, step=1.0)
    insight_type = st.selectbox("Insight Type", ["brand", "demographics", "heatmap"], key="insight_type")
    return location, category, insight_type, threshold

def product_keywords():
    st.subheader("Product Keywords")
    keywords = st.text_input("Enter keywords (comma-separated)", help="e.g., sneakers, streetwear")
    return [k.strip() for k in keywords.split(",") if k.strip()] if keywords else []

def product_description():
    st.subheader("Product Description")
    description = st.text_area("Enter product description")
    return description.strip() if description else ""

def insight_visualizer(insights, insight_type, location, category):
    st.subheader("Cultural Insights")
    if not insights or not insights.get("success"):
        st.error("Failed to fetch cultural insights. Please try again.")
        return None
    
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
            return df
        
        elif insight_type == "demographics":
            df = pd.DataFrame([
                {"age_group": entity.get("age_group", "Unknown"), "affinity": entity.get("affinity_score", 0.5)}
                for entity in entities
            ])
            fig = px.bar(df, x="age_group", y="affinity", title="Demographic Affinity",
                         color_discrete_sequence=["#764ba2"])
            st.plotly_chart(fig, use_container_width=True)
            return df
        
        elif insight_type == "heatmap":
            heatmap_data = insights["data"].get("heatmap", {})
            if not heatmap_data:
                st.warning("No heatmap data available.")
                return None
            z = heatmap_data.get("z", [])
            x = heatmap_data.get("x", [])
            y = heatmap_data.get("y", [])
            fig = go.Figure(data=go.Heatmap(z=z, x=x, y=y, colorscale="Viridis"))
            fig.update_layout(title="Regional Affinity Heatmap")
            st.plotly_chart(fig, use_container_width=True)
            return pd.DataFrame(z, columns=x, index=y)
        
        history_response = requests.get(f"{API_BASE_URL}/hype/history/{location}/{category}", timeout=10)
        history = history_response.json() if history_response.status_code == 200 else {"data": []}
        if history["data"]:
            df_history = pd.DataFrame(history["data"])
            fig_history = px.line(df_history, x="timestamp", y="score", title="Hype Score Trends",
                                  color_discrete_sequence=["#667eea"])
            st.plotly_chart(fig_history, use_container_width=True)
            return df_history
    except Exception as e:
        logger.error(f"Error rendering insights: {str(e)}")
        st.error(f"Error rendering insights: {str(e)}")
        return None

def prediction_dashboard(predictions, hype_score):
    st.subheader("Demand Predictions and Strategies")
    if not predictions or not predictions.get("success"):
        st.error("Failed to generate predictions. Please try again.")
        return None
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Demand Uplift", f"{predictions['data'].get('uplift', 'Unknown')}%")
        st.metric("Confidence Score", f"{predictions['data'].get('confidence', 'Unknown')}")
        st.metric("Hype Score", f"{hype_score.get('averageScore', 'Unknown')}")
        if hype_score.get("change_detected", False):
            st.warning(f"Significant change detected: {hype_score['change_percent']}%")
    with col2:
        st.write("**Recommended Strategy**")
        st.write(predictions["data"].get("strategy", "Unknown"))
    
    trend_data = predictions["data"].get("trend", [])
    if trend_data:
        df = pd.DataFrame(trend_data)
        fig = px.line(df, x="time", y="demand", title="Demand Trends",
                      color_discrete_sequence=["#667eea"])
        st.plotly_chart(fig, use_container_width=True)
        return df
    else:
        st.warning("No trend data available.")
    
    return pd.DataFrame({
        "Metric": ["Demand Uplift", "Confidence Score", "Hype Score", "Strategy"],
        "Value": [f"{predictions['data'].get('uplift', 'Unknown')}%",
                  f"{predictions['data'].get('confidence', 'Unknown')}",
                  f"{hype_score.get('averageScore', 'Unknown')}",
                  predictions["data"].get("strategy", "Unknown")]
    })

def export_report(insights_df, predictions_df, format_type):
    if insights_df is not None and predictions_df is not None:
        report_df = pd.concat([insights_df, predictions_df], axis=1, keys=["Insights", "Predictions"])
        if format_type == "PDF":
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            data = [report_df.columns.tolist()] + report_df.values.tolist()
            table = Table(data)
            doc.build([table])
            buffer.seek(0)
            return buffer, "caeser_report.pdf", "application/pdf"
        elif format_type == "Excel":
            buffer = BytesIO()
            report_df.to_excel(buffer, index=False, engine="openpyxl")
            buffer.seek(0)
            return buffer, "caeser_report.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        elif format_type == "CSV":
            buffer = BytesIO()
            report_df.to_csv(buffer, index=False, encoding='utf-8')
            buffer.seek(0)
            return buffer, "caeser_report.csv", "text/csv"
    return None, None, None

def data_quality_widget():
    st.subheader("Data Quality Report")
    try:
        response = requests.get(f"{API_BASE_URL}/data_quality", timeout=5)
        metrics = response.json() if response.status_code == 200 else {}
        if metrics.get("success"):
            st.markdown('<div class="data-quality__widget">', unsafe_allow_html=True)
            st.write(f"**Missing Values**: {metrics['data'].get('missing_values', {}).get('value', 0)}")
            st.write(f"**API Errors**: {metrics['data'].get('api_errors', {}).get('value', 0)}")
            st.write(f"**Freshness**: {metrics['data'].get('freshness', {}).get('value', 'Unknown'):.2f} hours")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No data quality metrics available.")
    except Exception as e:
        logger.error(f"Error fetching data quality: {str(e)}")
        st.error(f"Error fetching data quality: {str(e)}")

def llm_data_quality_widget():
    st.subheader("LLM Data Quality Report")
    try:
        response = requests.get(f"{API_BASE_URL}/llm_data_quality", timeout=5)
        metrics = response.json() if response.status_code == 200 else {}
        if metrics.get("success"):
            st.markdown('<div class="data-quality__widget">', unsafe_allow_html=True)
            confidence = metrics['data'].get('confidence', {})
            st.write(f"**Average Confidence**: {confidence.get('avg_value', 'N/A'):.2f}")
            errors = metrics['data'].get('errors', {})
            st.write(f"**Error Count**: {errors.get('count', 0)}")
            response_time = metrics['data'].get('response_time', {})
            st.write(f"**Average Response Time**: {response_time.get('avg_value', 'N/A'):.2f} seconds")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No LLM data quality metrics available.")
    except Exception as e:
        logger.error(f"Error fetching LLM data quality: {str(e)}")
        st.error(f"Error fetching LLM data quality: {str(e)}")

def mark_product(user_id, product_name, category):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO marked_products (user_id, product_name, category)
        VALUES (?, ?, ?)
    """, (user_id, product_name, category))
    conn.commit()
    conn.close()

def get_marked_products(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT product_name, category FROM marked_products WHERE user_id = ?
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"product_name": row[0], "category": row[1]} for row in rows]

def main():
    st.title("CÆSER: Cultural Affinity Simulation Engine for Retail")
    
    # Initialize store data table
    init_store_table()
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Main Dashboard", "Store Data", "Google Trends"])
    
    with tab1:
        user_id = st.text_input("User ID", help="Enter your user ID", key="user_id")
        location, category, insight_type, threshold = market_selector()
        keywords = product_keywords()
        description = product_description()
        export_format = st.selectbox("Export Format", ["PDF", "Excel", "CSV"], key="export_format")
        
        if user_id:
            marked_products = get_marked_products(user_id)
            if marked_products:
                st.subheader("Marked Products")
                for product in marked_products:
                    st.write(f"{product['product_name']} ({product['category']})")
        
        if st.button("Generate Insights and Predictions", key="submit"):
            with st.spinner("Fetching insights and predictions..."):
                try:
                    insights_response = requests.get(
                        f"{API_BASE_URL}/insights/{location}/{category}?insight_type={insight_type}",
                        timeout=10
                    )
                    insights = insights_response.json() if insights_response.status_code == 200 else {}
                    
                    product = {
                        "name": ", ".join(keywords) or category,
                        "category": category,
                        "description": description or f"{category} product"
                    }
                    
                    if st.checkbox("Mark this product for sentiment tracking", key="mark_product"):
                        mark_product(user_id, product["name"], category)
                    
                    prediction_payload = {"product": product, "insights": insights}
                    prediction_response = requests.post(
                        f"{API_BASE_URL}/predict/demand",
                        json=prediction_payload,
                        timeout=10
                    )
                    predictions = prediction_response.json() if prediction_response.status_code == 200 else {}
                    
                    hype_payload = {"insights": insights, "category": category, "location": location, "threshold": threshold, "product_name": product["name"]}
                    hype_response = requests.post(
                        f"{API_BASE_URL}/hype/score",
                        json=hype_payload,
                        timeout=10
                    )
                    hype_score = hype_response.json()
                    
                    insights_df = insight_visualizer(insights, insight_type, location, category)
                    predictions_df = prediction_dashboard(predictions, hype_score)
                    
                    if hype_score.get("hourly_sentiment_change"):
                        st.metric("Hourly Sentiment Change", f"{hype_score['hourly_sentiment_change']}%")
                    
                    data_quality_widget()
                    llm_data_quality_widget()
                    
                    buffer, filename, mime = export_report(insights_df, predictions_df, export_format)
                    if buffer:
                        st.download_button(
                            label=f"Download Report as {export_format}",
                            data=buffer,
                            file_name=filename,
                            mime=mime
                        )
                    
                    discord_payload = {"prediction": {"product": product, **predictions.get("data", {})}, "hype_data": hype_score}
                    requests.post(f"{API_BASE_URL}/discord/alert", json=discord_payload, timeout=5)
                    
                    integrations_payload = {"prediction": {"product": product, **predictions.get("data", {})}, "hype_data": hype_score}
                    requests.post(f"{API_BASE_URL}/integrations/send", json=integrations_payload, timeout=5)
                    
                except requests.RequestException as e:
                    logger.error(f"API request failed: {str(e)}")
                    st.error(f"API request failed: {str(e)}")
                except Exception as e:
                    logger.error(f"An error occurred: {str(e)}")
                    st.error(f"An error occurred: {str(e)}")
    
    with tab2:
        st.header("Store Data Management")
        user_provided_store_data()
        
        # Show existing store data
        st.subheader("Existing Store Data")
        conn = sqlite3.connect(DB_PATH)
        store_df = pd.read_sql_query("SELECT product, sales, date FROM store_data", conn)
        conn.close()
        
        if not store_df.empty:
            st.dataframe(store_df)
            st.download_button(
                label="Download Store Data as CSV",
                data=store_df.to_csv(index=False).encode('utf-8'),
                file_name="store_data.csv",
                mime="text/csv"
            )
        else:
            st.info("No store data available")
    
    with tab3:
        st.header("Google Trends Integration")
        fetch_and_display_trends()
        
        # Show existing trends data
        st.subheader("Existing Trends Data")
        conn = sqlite3.connect(DB_PATH)
        trends_df = pd.read_sql_query(
            "SELECT text AS keyword, likes AS interest, timestamp FROM social_data WHERE source='google_trends'", 
            conn
        )
        conn.close()
        
        if not trends_df.empty:
            st.dataframe(trends_df)
            st.download_button(
                label="Download Trends Data as CSV",
                data=trends_df.to_csv(index=False).encode('utf-8'),
                file_name="trends_data.csv",
                mime="text/csv"
            )
        else:
            st.info("No trends data available")

if __name__ == "__main__":
    main()
logger.info('Streamlit app initialized successfully')