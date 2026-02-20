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
    page_title="Krishi-Darpan AI",
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
st.title("🌾 Welcome To Krishi-Darpan AI")

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
    ka_type = "primary" if st.session_state.current_page == "Kisan Assistant" else "secondary"
    
    if st.button("🎙️ Kisan Assistant", type=ka_type):
        st.session_state.current_page = "Kisan Assistant"
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

elif st.session_state.current_page == "Kisan Assistant":
    st.subheader("🎙️ Voice Assistant")
    st.write("Tap the microphone icon to ask your farming question.")
    
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

                    # 2. Get Answer from Gemini
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    prompt = """
                    You are an expert agricultural assistant in Bihar. Listen to the farmer's question.
                    Respond directly with practical, easy-to-understand advice.
                    Keep the answer concise (under 3-4 sentences).
                    You must reply in Hindi, written in Devanagari script, so it can be spoken out loud clearly.
                    """
                    
                    response = model.generate_content([prompt, audio_file])
                    
                    st.success("Here is your answer:")
                    st.write(response.text)
                    
                    # --- NEW: TEXT-TO-SPEECH LOGIC ---
                    with st.spinner("Generating voice response..."):
                        # Convert the Hindi text to spoken audio
                        tts = gTTS(text=response.text, lang='hi') 
                        
                        # Save the spoken audio to a new temporary file
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_tts:
                            tts.save(temp_tts.name)
                            tts_audio_path = temp_tts.name
                            
                        # Play the audio back to the user automatically
                        st.audio(tts_audio_path, format="audio/mp3", autoplay=True)

                    # Clean up temporary files
                    os.remove(temp_audio_path)
                    # Note: We leave the tts_audio_path alone so Streamlit can finish playing it
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")