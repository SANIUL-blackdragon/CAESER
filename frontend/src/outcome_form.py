import streamlit as st
import requests

st.title("Report Actual Uplift")

# Input fields with validation
pid = st.number_input("Prediction ID", min_value=1, value=1, step=1)
actual = st.number_input("Actual uplift %", min_value=0.0, value=0.0, step=0.1)

# New gamified slider section
st.subheader("Marketing Simulation")
budget = st.slider("Marketing Budget ($)", 1000, 50000, 10000)
hype_score = st.slider("Estimated Hype Score", 0, 100, 70)

# Calculate ROI based on hype score and budget (capped at 50 % of budget)
roi = min(budget * 0.1 * (hype_score / 100), budget * 0.5)
st.metric("Est. ROI", f"${roi:.0f}", delta_color="inverse" if roi < budget else "normal")

if st.button("Submit"):
    if pid <= 0 or actual < 0:
        st.error("Please enter valid values for Prediction ID and Actual uplift %.")
    else:
        try:
            r = requests.post(
                f"{os.getenv('API_BASE_URL', 'http://localhost:8000')}/submit_outcome",
                json={"prediction_id": pid, "actual_uplift": actual}
            )
            st.json(r.json())
        except requests.RequestException as e:
            st.error(f"Failed to submit outcome: {str(e)}")