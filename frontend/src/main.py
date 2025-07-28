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
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# Add scrapers directory to path for Google Trends import
sys.path.append('../scrapers')
from google_trends import get_google_trends, store_trend

logger = setup_logging()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
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
                    
                for keyword, interest in trends.items():
                    store_trend(keyword, interest)
                
                st.success("Trends fetched and stored successfully")
                trends_df = pd.DataFrame({
                    "Keyword": list(trends.keys()),
                    "Interest": list(trends.values()),
                    "Source": "google_trends",
                    "Timestamp": datetime.now().isoformat()
                })
                st.dataframe(trends_df)
            except Exception as e:
                st.error(f"Error fetching trends: {str(e)}")

def product_input_form():
    """Form for product details and optional target market"""
    st.subheader("Product Details")
    product_name = st.text_input("Product Name", help="e.g., Air Jordan 1")
    description = st.text_area("Product Description", help="Describe the product")
    tags = st.text_input("Product Tags (comma-separated)", help="e.g., sneakers, fashion, streetwear")

    st.subheader("Target Market (Optional)")
    location = st.text_input("Location", help="e.g., New York, NY or leave blank for global")
    age_range = st.text_input("Age Range", help="e.g., 18-25 or leave blank")
    gender = st.selectbox("Gender", ["All", "Male", "Female"], index=0)
    insight_type = st.selectbox("Insight Type", ["brand", "demographics", "heatmap"], key="insight_type")
    threshold = st.number_input("Hype Change Threshold (%)", min_value=0.0, max_value=100.0, value=20.0, step=1.0)

    return product_name, description, tags, location, age_range, gender, insight_type, threshold

def insight_visualizer(insights, insight_type, location, tags):
    """Visualize cultural insights"""
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
    except Exception as e:
        logger.error(f"Error rendering insights: {str(e)}")
        st.error(f"Error rendering insights: {str(e)}")
        return None

def prediction_dashboard(predictions, hype_score):
    """Display predictions and strategies"""
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
    """Export analysis report"""
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
    """Display data quality metrics"""
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
    """Display LLM data quality metrics"""
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

def main():
    """Main application function"""
    st.title("CÆSER: Cultural Affinity Simulation Engine for Retail")
    
    init_store_table()
    
    tab1, tab2, tab3 = st.tabs(["Main Dashboard", "Store Data", "Google Trends"])
    
    with tab1:
        product_name, description, tags, location, age_range, gender, insight_type, threshold = product_input_form()
        export_format = st.selectbox("Export Format", ["PDF", "Excel", "CSV"], key="export_format")
        
        if st.button("Generate Insights and Predictions", key="submit"):
            if not (product_name and description and tags):
                st.error("Please fill in all required fields: Product Name, Description, and Tags.")
                return
            
            with st.spinner("Analyzing product..."):
                try:
                    # Call analyze endpoint to collect data
                    analyze_payload = {
                        "product_name": product_name,
                        "description": description,
                        "tags": tags,
                        "target_area": location if location else None,
                        "locations": location if location else None,
                        "gender": gender if gender != "All" else None
                    }
                    analyze_response = requests.post(f"{API_BASE_URL}/analyze", json=analyze_payload, timeout=60)
                    analyze_result = analyze_response.json() if analyze_response.status_code == 200 else {}
                    if not analyze_result.get("success"):
                        st.error(f"Analysis failed: {analyze_result.get('message', 'Unknown error')}")
                        return
                    
                    hype_score = analyze_result.get("hype_score", 0.0)
                    
                    # Fetch cultural insights
                    tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
                    insights_response = requests.get(
                        f"{API_BASE_URL}/insights/{location or 'global'}?tags={','.join(tags_list)}&insight_type={insight_type}",
                        timeout=10
                    )
                    insights = insights_response.json() if insights_response.status_code == 200 else {}
                    
                    # Prepare product dictionary
                    product = {
                        "name": product_name,
                        "tags": tags_list,
                        "description": description,
                        "location": location if location else "Global",
                        "age_range": age_range if age_range else "All",
                        "gender": gender if gender != "All" else "All"
                    }
                    
                    # Generate predictions
                    prediction_payload = {
                        "product": product,
                        "insights": insights,
                        "hype_score": hype_score
                    }
                    prediction_response = requests.post(
                        f"{API_BASE_URL}/predict/demand",
                        json=prediction_payload,
                        timeout=10
                    )
                    predictions = prediction_response.json() if prediction_response.status_code == 200 else {}
                    
                    # Display results
                    insights_df = insight_visualizer(insights, insight_type, location or "Global", tags)
                    predictions_df = prediction_dashboard(predictions, {"averageScore": hype_score})
                    
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
                    
                    discord_payload = {"prediction": {"product": product, **predictions.get("data", {})}, "hype_data": {"averageScore": hype_score}}
                    requests.post(f"{API_BASE_URL}/discord/alert", json=discord_payload, timeout=5)
                    
                except requests.RequestException as e:
                    logger.error(f"API request failed: {str(e)}")
                    st.error(f"API request failed: {str(e)}")
                except Exception as e:
                    logger.error(f"An error occurred: {str(e)}")
                    st.error(f"An error occurred: {str(e)}")
    
    with tab2:
        st.header("Store Data Management")
        user_provided_store_data()
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