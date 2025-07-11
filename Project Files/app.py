import streamlit as st
from utils.watson_api import get_ai_response
import json
import plotly.graph_objects as go

st.set_page_config(page_title="HealthAI - Intelligent Healthcare Assistant", layout="wide")

# Load custom styles
with open("assets/custom_styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown("""
<div style="text-align: center; margin-top: -40px;">
    <h1 style="font-size: 38px; font-weight: bold;">
        🩺 <span style="color:#2c3e50;">HealthAI</span> - <span style="color:#2c3e50;">Intelligent Healthcare Assistant</span>
    </h1>
</div>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
st.sidebar.header("Patient Profile")
with st.sidebar.form("patient_form"):
    name = st.text_input("Name", "")
    age = st.number_input("Age", min_value=0, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    medical_history = st.text_area("Medical History", "")
    current_meds = st.text_area("Current Medications", "")
    allergies = st.text_input("Allergies", "")

    submitted = st.form_submit_button("Submit Profile")
    if submitted:
        st.session_state["profile"] = {
            "name": name,
            "age": age,
            "gender": gender,
            "medical_history": medical_history,
            "current_meds": current_meds,
            "allergies": allergies
        }
        st.sidebar.success("✅ Profile submitted.")

# ------------------ FEATURE SELECTOR ------------------
st.markdown("### 24/7 Patient Support")
st.markdown("Ask any health-related question for immediate assistance.")
selected_tab = st.radio("Select Feature", ["Patient Chat", "Disease Prediction", "Treatment Plan Generator", "Health Analytics Dashboard"], horizontal=True)

# Retrieve latest profile info
profile = st.session_state.get("profile", {
    "name": name,
    "age": age,
    "gender": gender,
    "medical_history": medical_history,
    "current_meds": current_meds,
    "allergies": allergies
})

# ------------------ PATIENT CHAT ------------------
if selected_tab == "Patient Chat":
    st.subheader("💬 HealthAI Chat Assistant")
    query = st.text_input("Ask a health-related question:")

    if st.button("Submit", key="chat_query") and query:
        with st.spinner("Consulting AI Doctor..."):
            prompt = f"""
You are a responsible AI healthcare assistant.

The patient has submitted a health-related query. Use the following context to provide a clear, medically accurate, helpful response. Be specific and professional, and include actionable suggestions when possible. If necessary, mention that they should consult a licensed physician.

Patient Profile:
- Name: {profile['name']}
- Age: {profile['age']}
- Gender: {profile['gender']}
- Medical History: {profile['medical_history']}
- Current Medications: {profile['current_meds']}
- Allergies: {profile['allergies']}

Patient Question:
\"{query}\"

Your response should:
- Be direct and empathetic
- Include specific suggestions or first-aid steps if possible
- Avoid vague phrases like “just consult a doctor” unless absolutely required
- Avoid hallucinations or repetition

Format your answer in natural paragraph form.
"""
            response = get_ai_response(prompt)

            if not response.strip() or "Response" in response.strip():
                st.error("❌ The AI did not generate a proper response. Try asking again with more detail.")
            else:
                st.subheader("🩺 AI Medical Advice")
                st.markdown(response)
# ------------------ DISEASE PREDICTION ------------------
elif selected_tab == "Disease Prediction":
    st.subheader("🧪 Disease Prediction System")
    symptoms = st.text_area("Enter symptoms in detail (e.g., fatigue, sore throat for 3 days):")
    if st.button("Generate Prediction"):
        with st.spinner("Analyzing symptoms..."):
            prompt = (
                f"Based on the following symptoms: {symptoms}, and patient profile:\n"
                f"Age: {profile['age']}, Gender: {profile['gender']}\n"
                f"Medical History: {profile['medical_history']}\n"
                f"Current Medications: {profile['current_meds']}\n"
                f"Allergies: {profile['allergies']}\n"
                f"Predict possible medical conditions with likelihood and what steps should be taken next."
            )
            prediction = get_ai_response(prompt)
            st.subheader("🔍 Potential Conditions")
            st.markdown(prediction)

# ------------------ TREATMENT PLAN ------------------
elif selected_tab == "Treatment Plan Generator":
    st.subheader("💊 Personalized Treatment Plan Generator")
    condition = st.text_input("Enter medical condition (e.g., Diabetes, Mouth Ulcer):")

    if st.button("Generate Treatment Plan"):
        with st.spinner("Creating personalized plan..."):
            profile = st.session_state.get("profile", {
                "name": name,
                "age": age,
                "gender": gender,
                "medical_history": medical_history,
                "current_meds": current_meds,
                "allergies": allergies,
            })

            prompt = f"""
You are a licensed virtual healthcare assistant. Generate a complete treatment plan for:

🩺 Condition: {condition}

Patient Profile:
- Age: {profile['age']}
- Gender: {profile['gender']}
- Medical History: {profile['medical_history']}
- Current Medications: {profile['current_meds']}
- Allergies: {profile['allergies']}

The treatment plan should include ALL of the following 5 sections — do NOT skip or leave any section blank:

1. **Condition Overview** – Brief explanation of the condition  
2. **Recommended Medications** – List up to 5 meds (name, dosage, frequency)  
3. **Lifestyle Changes** – Diet, activity, hygiene, habits  
4. **Monitoring Advice** – What the patient should track (vitals, tests, symptoms)  
5. **Follow-Up Recommendations** – When to return, what exams to repeat, specialist referrals if needed

Please respond using bullet points where appropriate. Make sure the final response is clear, medically appropriate, and tailored to the patient.
"""
            response = get_ai_response(prompt)

            if not response.strip():
                st.error("⚠️ AI returned no useful information. Please try again.")
            else:
                st.subheader("📝 Treatment Plan")
                st.markdown(response)


# ------------------ HEALTH ANALYTICS ------------------
elif selected_tab == "Health Analytics Dashboard":
    st.subheader("📊 Health Analytics Dashboard")
    with open("data/health_metrics.json") as f:
        data = json.load(f)

    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=data["heart_rate"], mode='lines', name='Heart Rate'))
        fig.update_layout(title="Heart Rate Trend (90-Day)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=data["systolic"], mode='lines', name='Systolic'))
        fig.add_trace(go.Scatter(y=data["diastolic"], mode='lines', name='Diastolic'))
        fig.update_layout(title="Blood Pressure Trend (90-Day)")
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=data["glucose"], mode='lines', name='Glucose'))
        fig.update_layout(title="Blood Glucose Trend (90-Day)")
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        fig = go.Figure(data=[
            go.Pie(labels=list(data["symptoms"].keys()), values=list(data["symptoms"].values()))
        ])
        fig.update_layout(title="Symptom Frequency (90-Day)")
        st.plotly_chart(fig, use_container_width=True)
