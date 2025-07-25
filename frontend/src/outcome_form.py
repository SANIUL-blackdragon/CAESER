import streamlit as st, requests
st.title("Report Actual Uplift")
pid = st.number_input("Prediction ID", min_value=1)
actual = st.number_input("Actual uplift %")

# New gamified slider section
st.subheader("Marketing Simulation")
budget = st.slider("Marketing Budget ($)", 1000, 50000, 10000)
hype_score = st.slider("Estimated Hype Score", 0, 100, 70)

# Calculate ROI based on hype score and budget
roi = budget * 0.1 * (hype_score/100)
st.metric("Est. ROI", f"${roi:.0f}", 
          delta_color="inverse" if roi < budget else "normal")

if st.button("Submit"):
    r = requests.post("http://localhost:8000/submit_outcome",
                      json={"prediction_id": pid, "actual_uplift": actual})
    st.json(r.json())