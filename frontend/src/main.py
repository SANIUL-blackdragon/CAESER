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
load_dotenv()

sys.path.append('../scrapers')
try:
    from scrapers.google_trends import get_google_trends, store_trend
except ImportError:
    st.error("Failed to import google_trends module. Please ensure the scrapers package is installed.")
    st.stop()

logger = setup_logging()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
DB_PATH = os.getenv("DB_PATH", "./data/caeser.db").strip('\'"')
if not isinstance(DB_PATH, str):
    st.error("Invalid DB_PATH configuration")
    st.stop()
st.set_page_config(page_title="CÆSER Dashboard", layout="wide")

primary_color = os.getenv("PRIMARY_COLOR", "#667eea")
text_color = os.getenv("TEXT_COLOR", "#333")
st.markdown(f"""
    <style>
        .market-selector__dropdown {{ margin-bottom: {os.getenv("DROPDOWN_MARGIN", "1rem")}; }}
        .insight-visualizer__chart {{ max-width: 100%; }}
        .prediction-dashboard__container {{
            padding: {os.getenv("DASHBOARD_PADDING", "1rem")};
            background-color: {os.getenv("DASHBOARD_BG", "#f9f9f9")};
            border-radius: {os.getenv("DASHBOARD_RADIUS", "8px")};
        }}
        .product-keywords__input {{ width: 100%; }}
        .product-description__textarea {{ width: 100%; min-height: 100px; }}
        .data-quality__widget {{
            background-color: {os.getenv("WIDGET_BG", "#f0f0f0")};
            padding: {os.getenv("WIDGET_PADDING", "1rem")};
            border-radius: {os.getenv("WIDGET_RADIUS", "8px")};
        }}
        .tabs-container {{ margin-top: {os.getenv("TABS_MARGIN", "2rem")}; }}
        @media (max-width: 768px) {{
            .market-selector__dropdown {{ font-size: {os.getenv("MOBILE_FONT_SIZE", "14px")}; }}
            .insight-visualizer__chart {{ height: {os.getenv("MOBILE_CHART_HEIGHT", "300px")}; }}
        }}
        :root {{
            --primary-color: {primary_color};
            --text-color: {text_color};
        }}
        .stButton>button {{ background-color: var(--primary-color); color: white; }}
    </style>
""", unsafe_allow_html=True)

with st.sidebar.expander("🛠  Manage Categories"):
    st.subheader("Add / Edit Category")
    cat_name = st.text_input("Category Name", key="cat_name")
    cat_kws = st.text_area("Keywords (comma-separated)", key="cat_kws")
    if st.button("Save", key="save_cat"):
        if cat_name and cat_kws:
            r = requests.post(
                f"{API_BASE_URL}/categories",
                json={"category_name": cat_name, "keywords": cat_kws},
                timeout=5
            )
            st.success(r.json().get("message", "Saved"))
        else:
            st.error("Both fields required")

    st.subheader("Current Categories")
    try:
        cats = requests.get(f"{API_BASE_URL}/categories", timeout=5).json().get("data", {})
        for k, v in cats.items():
            st.write(f"**{k}**: {', '.join(v)}")
    except Exception as e:
        st.error("Could not load categories")

with st.sidebar.expander("🏆 Manage Competitors"):
    st.subheader("Add / Update")
    comp_name = st.text_input("Competitor Name", key="comp_name")
    comp_score = st.number_input("Hype Score", 0.0, 100.0, 50.0, key="comp_score")
    if st.button("Save Competitor", key="save_comp"):
        if comp_name:
            r = requests.post(
                f"{API_BASE_URL}/competitors/add",
                json={"name": comp_name, "hype_score": comp_score},
                timeout=5
            )
            st.success(r.json().get("message", "Saved"))
        else:
            st.error("Name required")

    st.subheader("Current Rankings")
    try:
        comps = requests.get(f"{API_BASE_URL}/competitors", timeout=5).json()
        sorted_comps = sorted(comps.items(), key=lambda x: x[1]["hype"], reverse=True)
        for idx, (name, data) in enumerate(sorted_comps, 1):
            st.write(f"{idx}. **{name}** – {data['hype']}")
    except Exception as e:
        st.error("Could not load competitors")

def init_store_table():
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
    st.subheader("Google Trends Search")
    keywords_input = st.text_input("Enter keywords (comma-separated):",
                                 placeholder="e.g., electronics, fashion, sports")
    
    if st.button("Fetch Trends"):
        if not keywords_input:
            st.error("Please enter at least one keyword")
            return
            
        keywords = [kw.strip() for kw in keywords_input.split(",")]
        with st.spinner("Fetching Google Trends data..."):
            try:
                trends = get_google_trends(keywords)
                if not trends or not isinstance(trends, dict):
                    st.warning("No trends data found or invalid format")
                    return
                
                try:
                    for keyword, interest in trends.items():
                        store_trend(keyword, interest)
                    
                    st.success("Trends fetched and stored successfully")
                    trends_df = pd.DataFrame({
                        "Keyword": list(trends.keys()),
                        "Interest": list(trends.values()),
                        "Source": "google_trends",
                        "Timestamp": datetime.now().isoformat()
                    })
                except AttributeError as e:
                    st.error(f"Invalid trends data format: {str(e)}")
                    return
                st.dataframe(trends_df)
            except Exception as e:
                st.error(f"Error fetching trends: {str(e)}")

def product_input_form():
    default_sources = ["reddit", "tiktok", "instagram", "imdb", "ebay"]
    selected_sources = st.multiselect("Scraping Sources", default_sources, default_sources)
    sources_str = ",".join(selected_sources)
    
    st.subheader("Product Details")
    product_name = st.text_input("Product Name", help="e.g., Wireless Headphones")
    description = st.text_area("Product Description", help="Describe the product")
    tags = st.text_input("Product Tags (comma-separated)", help="e.g., electronics, audio, gadgets")

    st.subheader("Target Market (Optional)")
    location = st.text_input("Location", help="e.g., San Francisco, CA or blank for global")
    age_range = st.text_input("Age Range", help="e.g., 25-35 or blank")
    gender_options = os.getenv("GENDER_OPTIONS", "All,Male,Female").split(",")
    try:
        insight_types = requests.get(f"{API_BASE_URL}/insight_types", timeout=5).json()
    except Exception:
        insight_types = ["brand", "demographics", "heatmap"]  # fallback
    
    gender = st.selectbox("Gender", gender_options, index=0)
    insight_type = st.selectbox("Insight Type", insight_types)
    threshold = st.number_input("Hype Change Threshold (%)", min_value=0.0, max_value=100.0, value=20.0, step=1.0)

    return product_name, description, tags, location, age_range, gender, insight_type, threshold

def insight_visualizer(insights, insight_type, location, tags):
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

def prediction_dashboard(predictions, hype_score, trend_prediction):
    st.subheader("Demand Predictions and Strategies")
    if not predictions or not predictions.get("success"):
        st.error("Failed to generate predictions. Please try again.")
        return None
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Demand Uplift", f"{predictions['data'].get('uplift', 'Unknown')}%")
        st.metric("Confidence Score", f"{predictions['data'].get('confidence', 'Unknown')}")
        st.metric("Hype Score", f"{hype_score}")
        if trend_prediction and trend_prediction.get("success"):
            st.metric("Trend Peak", f"{trend_prediction['predicted_peak_days']} days")
        else:
            st.warning("Trend prediction unavailable")
    with col2:
        st.write("**Recommended Strategy**")
        st.write(predictions["data"].get("strategy", "Unknown"))
        if trend_prediction and trend_prediction.get("success"):
            st.write("**Trend Peak Date**")
            st.write(trend_prediction["predicted_peak_date"])
    
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
        "Metric": ["Demand Uplift", "Confidence Score", "Hype Score", "Strategy"] + 
                  (["Trend Peak Days", "Trend Peak Date"] if trend_prediction and trend_prediction.get("success") else []),
        "Value": [f"{predictions['data'].get('uplift', 'Unknown')}%",
                  f"{predictions['data'].get('confidence', 'Unknown')}",
                  f"{hype_score}",
                  predictions["data"].get("strategy", "Unknown")] +
                  ([str(trend_prediction["predicted_peak_days"]), trend_prediction["predicted_peak_date"]] 
                   if trend_prediction and trend_prediction.get("success") else [])
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

def main():
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
                    # Call updated analyze endpoint
                    analyze_payload = {
                        "product_name": product_name,
                        "description": description,
                        "tags": tags,
                        "target_area": location,
                        "locations": location,
                        "gender": gender,
                        "sources": sources_str   # ⬅️ NEW
                    }
                    analyze_response = requests.post(f"{API_BASE_URL}/analyze", json=analyze_payload, timeout=60)
                    analyze_result = analyze_response.json() if analyze_response.status_code == 200 else {}
                    if not analyze_result.get("success"):
                        st.error(f"Analysis failed: {analyze_result.get('message', 'Unknown error')}")
                        return
                    
                    hype_score = analyze_result.get("hype_score", 0.0)
                    trend_prediction = analyze_result.get("trend_prediction")
                    
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
                    predictions_df = prediction_dashboard(predictions, hype_score, trend_prediction)
                    
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
                    
                    discord_payload = {
                        "prediction": {"product": product, **predictions.get("data", {})},
                        "hype_data": {"averageScore": hype_score},
                        "trend_prediction": trend_prediction
                    }
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

if __name__ == "__main__":
    main()
logger.info(os.getenv("STARTUP_MESSAGE", "API initialized successfully"))