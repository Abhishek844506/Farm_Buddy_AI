import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
from audio_recorder_streamlit import audio_recorder
import tempfile
from gtts import gTTS

# 1. Load API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("API Key not found! Please check your .env file.")
else:
    genai.configure(api_key=api_key)

# 2. Page Configuration
st.set_page_config(
    page_title="Farm-Buddy AI",
    page_icon="🌱",
    layout="centered"
)

# 3. Custom CSS for Dynamic Active/Inactive Tabs
st.markdown("""
    <style>
    /* Base styling for BOTH buttons in the navigation row */
    div[data-testid="stHorizontalBlock"]:nth-of-type(1) button {
        width: 325px !important;
        font-size: 40px !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
    }
    
    /* INACTIVE STATE (Natural Green) -> Streamlit 'secondary' button */
    div[data-testid="stHorizontalBlock"]:nth-of-type(1) button[kind="secondary"] {
        background-color: #48A111 !important; /* Natural green */
        color: white !important;
        border: 2px solid transparent !important; 
        box-shadow: none !important;
    }
    
    /* Hover effect for inactive button */
    div[data-testid="stHorizontalBlock"]:nth-of-type(1) button[kind="secondary"]:hover {
        background-color: #3d8c0f !important;
    }
    
    /* ACTIVE STATE (Dark Green + Border + Shadow) -> Streamlit 'primary' button */
    div[data-testid="stHorizontalBlock"]:nth-of-type(1) button[kind="primary"] {
        background-color: #1a3d06 !important; /* Dark Green */
        color: white !important;
        border: 3px solid #051401 !important; /* Even darker green border */
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4) !important; /* Prominent shadow */
    }
            
    /* General Action Buttons (Ask Assistant, Analyze Image, etc.) */
    div.stButton > button {
        background-color: #48A111 !important; /* Natural Green */
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
    }
    
    /* Hover effect for action buttons */
    div.stButton > button:hover {
        background-color: #3d8c0f !important; /* Slightly darker green on hover */
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Main Header & Intro
st.title("🌾 Welcome To Farm-Buddy AI")

st.divider() 
st.subheader("**Your AI-Powered Farming Companion**")
st.markdown("""
This application uses Artificial Intelligence to help you:
    
1. **Identify Plant Diseases:** Upload a photo of a leaf, and our AI will diagnose the issue.
2. **Get Farming Advice:** Ask questions using your voice.
""")

# --- SESSION STATE INITIALIZATION ---
if "current_page" not in st.session_state:
    st.session_state.current_page = "Plant Doctor"

# 5. Button Navigation Layout (In Columns)
col1, col2 = st.columns(2)

with col1:
    # Set to 'primary' if active, 'secondary' if inactive
    pd_type = "primary" if st.session_state.current_page == "Plant Doctor" else "secondary"
    
    if st.button("🍂 Plant Doctor", type=pd_type):
        st.session_state.current_page = "Plant Doctor"
        st.rerun()

with col2:
    # Set to 'primary' if active, 'secondary' if inactive
    vg_type = "primary" if st.session_state.current_page == "Voice Guide" else "secondary"
    
    if st.button("🎙️ Voice Guide", type=vg_type):
        st.session_state.current_page = "Voice Guide"
        st.rerun()
    

# 6. Tab Content Logic using Session State
if st.session_state.current_page == "Plant Doctor":
    st.subheader("🍂 Plant Disease Detector")
    
    if "uploader_key" not in st.session_state:
        st.session_state.uploader_key = 0

    st.warning("🛑 Please ensure the image is a clear photo of a plant or leaf.")
    
    input_method = st.radio("Choose Input Method:", ["📁 Upload Image", "📷 Take Picture"], horizontal=True)
    image_data = None
    
    if input_method == "📁 Upload Image":
        image_data = st.file_uploader("Choose a leaf image...", type=["jpg", "jpeg", "png"], key=f"upload_{st.session_state.uploader_key}")
    else:
        image_data = st.camera_input("Take a picture of the leaf", key=f"camera_{st.session_state.uploader_key}")
    
    if image_data is not None:
        image = Image.open(image_data)
        st.image(image, caption="Selected Image", use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            analyze_clicked = st.button("🔍 Analyze Image", key="analyze_btn")
        with col2:
            if st.button("🔄 Reupload / Retake", key="retake_btn"):
                st.session_state.uploader_key += 1
                st.rerun()
                
        if analyze_clicked: 
            with st.spinner("Analyzing with Gemini AI..."):
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    prompt = """
                    You are an expert agronomist. First, analyze the image to determine if it contains a plant, leaf, tree, or crop.
                    If the image DOES NOT contain a plant or crop, ONLY reply with: "WARNING_NOT_A_PLANT"
                    If the image DOES contain a plant, identify the crop and the disease. Provide the answer in three sections:
                    1. Disease Name 
                    2. Severity 
                    3. Recommended Treatment (Organic and Chemical)
                    """
                    response = model.generate_content([prompt, image])
                    
                    if "WARNING_NOT_A_PLANT" in response.text:
                        st.error("❌ Invalid Image Detected: Please upload a valid agricultural image.")
                    else:
                        st.success("Analysis Complete!")
                        st.write(response.text)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

elif st.session_state.current_page == "Voice Guide":
    st.subheader("🎙️ Voice Guide")
    st.write("Tap the microphone icon to ask your farming question. The AI will reply in your language!")
    
    # --- AUDIO RECORDING WIDGET ---
    audio_bytes = audio_recorder(text="Click to Record", recording_color="#e81c1c", neutral_color="#48A111")
    
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        
        if st.button("Ask Assistant", key="ask_voice_btn"):
            with st.spinner("Listening and thinking..."):
                try:
                    # 1. Save farmer's voice to temp file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                        temp_audio.write(audio_bytes)
                        temp_audio_path = temp_audio.name

                    audio_file = genai.upload_file(path=temp_audio_path)

                    # 2. Get Answer from Gemini with Dynamic Language Prompt
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    prompt = """
                    You are an expert agricultural assistant. Listen to the farmer's question.
                    Respond directly with practical, easy-to-understand advice (under 3-4 sentences).
                    
                    CRITICAL INSTRUCTION:
                    1. Detect the exact language the farmer is speaking.
                    2. You MUST reply in that exact same language.
                    3. You MUST format your final output strictly as: language_code|Your text response.
                    
                    Use standard 2-letter Google TTS language codes (e.g., 'hi' for Hindi/Bhojpuri, 'en' for English, 'bn' for Bengali, 'mr' for Marathi).
                    
                    Example Output:
                    hi|गेहूं की फसल में यूरिया का प्रयोग करें।
                    """
                    
                    response = model.generate_content([prompt, audio_file])
                    
                    # 3. Split the AI's response to get the code and the text
                    try:
                        # Splits the text into exactly two parts at the first '|'
                        lang_code, actual_response = response.text.split('|', 1)
                        lang_code = lang_code.strip().lower()
                        actual_response = actual_response.strip()
                    except ValueError:
                        # Fallback just in case the AI forgets to add the '|'
                        lang_code = 'hi' 
                        actual_response = response.text
                    
                    st.success("Here is your answer:")
                    st.write(actual_response)
                    
                    # 4. TEXT-TO-SPEECH LOGIC (Now Dynamic!)
                    with st.spinner(f"Generating voice response in '{lang_code}'..."):
                        # Pass the dynamically detected language code to gTTS
                        tts = gTTS(text=actual_response, lang=lang_code) 
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_tts:
                            tts.save(temp_tts.name)
                            tts_audio_path = temp_tts.name
                            
                        st.audio(tts_audio_path, format="audio/mp3", autoplay=True)

                    # Clean up the audio file you uploaded to Gemini
                    os.remove(temp_audio_path)
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")

# 7. PERSISTENT SECTION: Live Market Prices
st.divider()

st.header("🌾 Crop Market Price Live")
st.write("Check the latest agricultural commodity prices in your local market.")

# User Inputs for filtering data
col1, col2 = st.columns(2)
with col1:
    selected_state = st.selectbox("Select State", ["Bihar", "Uttar Pradesh", "Punjab", "Haryana"])
with col2:
    # Dynamic district selection based on state
    if selected_state == "Bihar":
        districts = ["Patna", "Gaya", "Muzaffarpur", "Bhagalpur", "Purnia"]
    else:
        districts = ["District 1", "District 2"] 
    selected_district = st.selectbox("Select District", districts)

selected_crop = st.selectbox("Select Crop", ["Wheat", "Rice (Paddy)", "Maize", "Mustard", "Potato", "Onion"])

# Mock API Function (Simulating data.gov.in)
def fetch_mandi_prices(state, district, crop):
    import random
    import pandas as pd
    from datetime import date
    
    base_prices = {
        "Wheat": 2275, "Rice (Paddy)": 2183, "Maize": 2090, 
        "Mustard": 5650, "Potato": 1200, "Onion": 1800
    }
    
    base = base_prices.get(crop, 2000)
    
    data = {
        "Market (Mandi)": [f"{district} Main Market", f"{district} APMC", f"{district} Rural"],
        "Commodity": [crop, crop, crop],
        "Variety": ["Common", "Grade A", "Common"],
        "Min Price (₹/Quintal)": [base - random.randint(50, 150) for _ in range(3)],
        "Max Price (₹/Quintal)": [base + random.randint(50, 200) for _ in range(3)],
        "Arrival Date": [date.today().strftime("%d-%b-%Y")] * 3
    }
    return pd.DataFrame(data)

# Display the Data
if st.button("Get Latest Prices", key="get_prices_btn"):
    with st.spinner("Fetching data from mandis..."):
        df = fetch_mandi_prices(selected_state, selected_district, selected_crop)
        
        # Highlight the average Max price
        avg_max_price = int(df["Max Price (₹/Quintal)"].mean())
        st.metric(label=f"Average Max Price for {selected_crop} in {selected_district}", 
                  value=f"₹ {avg_max_price} / Quintal", 
                  delta="Updated Today", delta_color="normal")
        
        # Display the full table
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption("Data source: Simulated Agmarknet Data (For Internship Demo Purposes)")
