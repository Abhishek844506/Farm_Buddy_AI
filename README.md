# 🌱 Farm-Buddy AI — AI-Powered Farming Companion

Farm-Buddy AI is an **AI-powered smart agriculture assistant** designed to help farmers with **plant disease detection, multilingual voice guidance, and real-time mandi (market) prices** — all through a simple mobile-friendly web application.

The goal of this project is to make advanced agricultural assistance accessible to farmers using **Artificial Intelligence, Multimodal AI, and Voice Technology**.

---

## 🚀 Features

### 🌿 Plant Disease Detection
- Upload or capture a plant leaf image
- AI-powered disease identification
- Get:
  - Disease Name
  - Severity Level
  - Recommended Cure/Treatment

### 🎙️ Multilingual Voice Guide
- Ask farming-related questions using voice
- Supports multilingual interaction
- Receives spoken responses in the **same language**

### 📈 Live Mandi Market Prices
- View commodity prices in real time
- District & state-wise market updates
- Helps farmers get fair pricing information

### 📱 Mobile-Friendly Web App
- Works directly in the browser
- No installation required
- Accessible on smartphones and desktops

---

## 🛠️ Tech Stack

### Frontend
- **Streamlit**

### Backend / AI
- **Python**
- **Google Gemini 2.5 Flash API**

### Voice Processing
- **gTTS (Google Text-to-Speech)**
- **audio_recorder**

### Data Processing
- **Pandas**

### Deployment
- **Streamlit Community Cloud**

---

## 🧠 How It Works

### 1️⃣ Plant Disease Detection Pipeline
```text
Leaf Image Upload
        ↓
Google Gemini API
(acts as an agronomist)
        ↓
Disease Detection
        ↓
Severity + Cure Recommendation
```

### 2️⃣ Voice Assistant Pipeline
```text
Voice Input (.wav)
        ↓
Gemini API Processing
        ↓
Text Response
        ↓
gTTS Conversion
        ↓
Voice Reply (Same Language)
```

---

## 📸 Project Screenshots

### Home Page
_Add screenshots here_

### Plant Disease Detection
_Add screenshots here_

### Live Market Dashboard
_Add screenshots here_

---

## 🎯 Problem Statement

Agriculture is one of the most important sectors in India, but many farmers still face challenges such as:

- Difficulty identifying plant diseases quickly
- Limited access to agricultural experts
- Language barriers in digital farming resources
- Lack of real-time mandi pricing information

Farm-Buddy AI aims to solve these problems by acting as a **24×7 Pocket Agricultural Specialist**.

---

## 🔮 Future Scope

- 🌦️ **Weather-Based Spray Alerts**
- 📍 **Geo-Localized Pest Alerts**
- 🤖 **ML-Based Crop Recommendation System**
- 📡 **Real-Time Government Market APIs Integration**

---

## ⚙️ Installation & Setup

### Clone the Repository

```bash
git clone https://github.com/your-username/Farm_Buddy_AI.git
```

### Navigate to Project Folder

```bash
cd Farm_Buddy_AI
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app.py
```

---

## 🌐 Live Demo

🔗 https://farmbuddyai.streamlit.app/

---

## 📂 Project Structure

```text
Farm_Buddy_AI/
│── app.py
│── requirements.txt
│── assets/
│── data/
│── utils/
│── README.md
```

---

## 👨‍💻 Author

**Abhishek Kumar Nirankari**  

