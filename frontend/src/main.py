# frontend/src/main.py  – v2 + helpers (drop-in)
import asyncio, os, json, logging
from datetime import datetime
import streamlit as st
import requests, pandas as pd, plotly.express as px, plotly.graph_objects as go
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table
from dotenv import load_dotenv  # ← make sure this is imported

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="CÆSER Dashboard v2", layout="wide")

# ---------- THEMING & DARK MODE ----------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
st.sidebar.button(
    "🌗 Toggle Dark",
    on_click=lambda: st.session_state.__setitem__(
        "dark_mode", not st.session_state.dark_mode
    ),
)
st.markdown(
    f"""<style> :root {{ --p:{os.getenv("PRIMARY_COLOR","#667eea")};}}
.dark body{{background:#0f172a;color:#e2e8f0}}</style>""",
    unsafe_allow_html=True,
)

# ---------- ASYNC / VALID ----------
async def async_post(endpoint, payload):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        lambda: requests.post(
            f"{API_BASE_URL}{endpoint}",
            json=payload,
            timeout=60,
        ).json(),
    )

def validate_inputs(n, d):
    return bool(n.strip() and d.strip())

# ---------- SIDEBAR ----------
with st.sidebar.expander("🛠 Manage"):
    for t, lbl in (("categories", "Category"), ("competitors", "Competitor")):
        st.subheader(f"{lbl}")
        name = st.text_input(f"{lbl} Name", key=f"{t}_name")
        extra = (
            st.number_input("Hype Score", 0.0, 100.0, 50.0, key=f"{t}_score")
            if t == "competitors"
            else st.text_area("Keywords (comma)", key=f"{t}_kw")
        )
        if st.button("Save", key=f"{t}_save"):
            payload = (
                {"name": name, "hype_score": extra}
                if t == "competitors"
                else {"category_name": name, "keywords": extra}
            )
            st.success(
                requests.post(
                    f"{API_BASE_URL}/{t}",
                    json=payload,
                    timeout=5,
                )
                .json()
                .get("message", "Saved")
            )

# ---------- HELPERS ----------
@st.cache_data(ttl=300)
def _get_insights(location, tags, insight_type):
    """Cached wrapper for /insights endpoint."""
    url = f"{API_BASE_URL}/insights/{location or 'global'}"
    params = {"tags": tags or "", "insight_type": insight_type}
    return requests.get(url, params=params, timeout=30).json()

@st.cache_data(ttl=300)
def _get_trend_prediction(location, tags):
    url = f"{API_BASE_URL}/trend_prediction"
    payload = {"location": location or "global", "tags": tags or ""}
    return requests.post(url, json=payload, timeout=30).json()

def insight_chart(data, itype):
    if not data or not data.get("success"):
        return None
    ents = data["data"].get("entities", [])
    if itype == "brand":
        df = pd.DataFrame(
            [
                {"trait": e["name"], "score": e["properties"].get("popularity", 0.5)}
                for e in ents
            ]
        )
        fig = px.bar(df, x="trait", y="score", title="Cultural Affinity")
    elif itype == "demographics":
        df = pd.DataFrame(
            [
                {"age": e.get("age_group", "?"), "affinity": e.get("affinity_score", 0.5)}
                for e in ents
            ]
        )
        fig = px.bar(df, x="age", y="affinity", title="Demographic Affinity")
    elif itype == "heatmap":
        h = data["data"].get("heatmap", {})
        fig = go.Figure(
            go.Heatmap(
                z=h.get("z", []),
                x=h.get("x", []),
                y=h.get("y", []),
                colorscale="Viridis",
            )
        )
        fig.update_layout(title="Regional Heatmap")
    else:
        return None
    st.plotly_chart(fig, use_container_width=True)
    return df

def pred_chart(p, hype, t):
    if not p or not p.get("success"):
        return None
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Uplift %", f"{p['data'].get('uplift', '-')}")
        st.metric("Confidence", f"{p['data'].get('confidence', '-')}")
        st.metric("Hype", f"{hype}")
        if t and t.get("success"):
            st.metric("Peak in", f"{t['predicted_peak_days']} days")
    with c2:
        st.write("**Strategy**", p["data"].get("strategy", "-"))
    trend = p["data"].get("trend", [])
    if trend:
        st.plotly_chart(
            px.line(
                pd.DataFrame(trend),
                x="time",
                y="demand",
                title="Demand Trend",
            ),
            use_container_width=True,
        )
    return pd.DataFrame([{"Metric": "Uplift", "Value": p["data"].get("uplift")}])

def export_report(df1, df2, fmt):
    if df1 is None or df2 is None:
        return None, None, None
    report = pd.concat([df1, df2], axis=1)
    buf = BytesIO()
    if fmt == "PDF":
        SimpleDocTemplate(buf, pagesize=letter).build(
            [Table([report.columns.tolist()] + report.values.tolist())]
        )
    elif fmt == "Excel":
        report.to_excel(buf, index=False)
    else:
        report.to_csv(buf, index=False)
    buf.seek(0)
    return (
        buf,
        f"report.{fmt.lower()}",
        (
            "application/pdf"
            if fmt == "PDF"
            else (
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                if fmt == "Excel"
                else "text/csv"
            )
        ),
    )

def dq_widget():
    try:
        m = requests.get(f"{API_BASE_URL}/data_quality", timeout=5).json()
        if m.get("success"):
            st.subheader("Data Quality")
            for k, v in m["data"].items():
                st.write(f"**{k}**: {v.get('value', '-')}")
    except Exception:
        pass

# ---------- MAIN ----------
tab1, tab2, tab3 = st.tabs(["Dashboard", "Store Data", "Google Trends"])
with tab1:
    st.subheader("Product Details")
    pn = st.text_input("Product Name*")
    desc = st.text_area("Description*")
    tags = st.text_input("Tags")
    loc = st.text_input("Location")
    age = st.text_input("Age")
    gender = st.selectbox("Gender", ["All", "Male", "Female"])
    itype = st.selectbox("Insight", ["brand", "demographics", "heatmap"])
    if st.button("Analyze", use_container_width=True) and validate_inputs(pn, desc):
        with st.spinner("Analyzing…"):
            res = asyncio.run(
                async_post(
                    "/analyze",
                    {
                        "product_name": pn,
                        "description": desc,
                        "tags": tags,
                        "locations": loc,
                        "gender": gender,
                    },
                )
            )
            hype = res.get("hype_score", 0)
            with st.spinner("Fetching trend prediction…"):
                trend = asyncio.run(
                    async_post(
                        "/predict/trend",
                        {"product_name": pn, "tags": tags},
                    )
                )
            with st.spinner("Fetching insights…"):
                ins = _get_insights(loc, tags, itype)
            with st.spinner("Predicting demand…"):
                pred = asyncio.run(
                    async_post(
                        "/predict/demand",
                        {
                            "product": {"name": pn, "tags": tags},
                            "insights": ins,
                            "hype_score": hype,
                        },
                    )
                )
            df_ins = insight_chart(ins, itype)
            df_pred = pred_chart(pred, hype, trend)
            dq_widget()
            buf, fn, mime = export_report(
                df_ins,
                df_pred,
                st.selectbox("Export", ["CSV", "Excel", "PDF"]),
            )
            if buf:
                st.download_button("Download Report", data=buf, file_name=fn, mime=mime)

with tab2:
    st.subheader("Store Data")
    up = st.file_uploader("CSV (product,sales,date)", type="csv")
    if up:
        df = pd.read_csv(up)
        st.dataframe(df.head())
        if st.button("Upload"):
            with st.spinner("Uploading…"):
                for _, row in df.iterrows():
                    asyncio.run(async_post("/store_data", dict(row)))
            st.success("Uploaded!")
        st.download_button(
            "Download existing store data",
            data=requests.get(f"{API_BASE_URL}/store_data").content,
            file_name="store.csv",
        )

with tab3:
    kw = st.text_input("Google Trends Keywords")
    if st.button("Fetch"):
        with st.spinner("Fetching Google Trends…"):
            r = requests.post(
                f"{API_BASE_URL}/google_trends",
                json={"keywords": kw.split(",")},
            )
        st.dataframe(pd.json_normalize(r.json()))