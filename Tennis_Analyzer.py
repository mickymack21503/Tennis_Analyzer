import streamlit as st
import tempfile
import os
import time

# Custom CSS for modern styling and enhancements
st.markdown("""
    <style>
        /* Global Background and Font */
        .main {
            background-color: #212121;
            font-family: 'Roboto', sans-serif;
            color: #e0e0e0;
        }
        /* Title Styling */
        .title {
            text-align: center;
            color: #81c784;
            font-weight: bold;
            font-size: 2.5em;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        /* Sidebar Styling */
        .sidebar .sidebar-content {
            background-color: #263238;
            color: #e0f7fa;
            padding: 1.5rem;
            border-radius: 8px;
        }
        .sidebar .sidebar-header {
            color: #ffffff;
            font-size: 1.3em;
            font-weight: bold;
        }
        /* Button Styling */
        .stButton > button {
            width: 100%;
            margin: 1rem 0;
            background-color: #4caf50;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px;
            font-size: 1.1rem;
            transition: background-color 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #388e3c;
        }
        .stButton > button:active {
            transform: scale(0.98);
        }
        /* Progress Bar Styling */
        .stProgress > div > div {
            background-color: #81c784;
            border-radius: 8px;
        }
        /* Video Styling */
        .stVideo {
            border-radius: 15px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            margin-top: 1rem;
            max-width: 100%;
        }
        /* Information Text */
        .info-text {
            font-size: 1.1rem;
            color: #b2dfdb;
            text-align: center;
            margin-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h2 class='title'>🎾 Tennis Game Tracking 🎾</h2>", unsafe_allow_html=True)

# Sidebar for input and actions
st.sidebar.title("🎬 Controls")

# File uploader with enhanced description
uploaded_file = st.sidebar.file_uploader("📂 Select Input Video File", type=["mp4", "avi", "mov"])

# Initialize temp_file_path as None
temp_file_path = None

# Check if a file is uploaded
if uploaded_file:
    # Save the uploaded file temporarily
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_file.read())
    temp_file_path = temp_file.name

    # Button to preview the video with smooth transition
    if st.sidebar.button("▶️ Preview Video"):
        st.video(temp_file_path, start_time=0)
    
    # Processing video with a dynamic progress indicator
    progress_bar = st.sidebar.progress(0)
    if st.sidebar.button("⚙️ Process Video"):
        st.sidebar.text("🔄 Processing Video...")

        # Simulate processing time and update progress
        for percent in range(1, 101):
            progress_bar.progress(percent)
            time.sleep(0.05)  # Simulated delay for faster response
        
        st.sidebar.text("✅ Video processed successfully!")

    # Show processed output after processing
    if st.sidebar.button("👀 Show Output"):
        st.video(temp_file_path)  # Placeholder for processed video (replace after actual processing)
    
    # Download processed output with smoother UI
    st.sidebar.download_button(
        label="⬇️ Download Processed Video",
        data=temp_file_path,
        file_name="processed_video.mp4",
        mime="video/mp4"
    )

    # Closing the temporary file after use
    temp_file.close()
    os.remove(temp_file.name)

else:
    st.markdown("<p class='info-text'>Please upload a video file to start processing.</p>", unsafe_allow_html=True)