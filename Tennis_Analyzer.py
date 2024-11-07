import streamlit as st
import tempfile
import os
import cv2
import numpy as np
import time
from ultralytics import YOLO

# Load YOLOv8 model
@st.cache_resource
def load_model():
    model = YOLO("C:/Users/nevyp/Desktop/Project/netGenius/models/yolov8x.pt")  # Make sure this path points to your YOLOv8x model
    return model

# Process video function
def process_video(input_path, output_path):
    model = load_model()
    video = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(video.get(cv2.CAP_PROP_FPS))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    progress_bar = st.sidebar.progress(0)

    for i in range(frame_count):
        ret, frame = video.read()
        if not ret:
            break

        # Run YOLOv8 inference
        results = model(frame)
        annotated_frame = results[0].plot()  # Get the annotated frame

        # Write the annotated frame to output video
        out.write(annotated_frame)

        # Update progress
        progress_bar.progress((i + 1) / frame_count)

    video.release()
    out.release()
    progress_bar.empty()

    # Check if output video was created
    return os.path.exists(output_path)

# Streamlit UI code
st.title("🎾 Tennis Game Tracking 🎾")

# Sidebar controls
st.sidebar.title("Controls")
uploaded_file = st.sidebar.file_uploader("📂 Select Input Video File", type=["mp4", "avi", "mov"])

if uploaded_file:
    # Save the uploaded file temporarily
    temp_input = tempfile.NamedTemporaryFile(delete=False)
    temp_input.write(uploaded_file.read())
    temp_input_path = temp_input.name
    
    # Prepare temporary file for processed output
    temp_output_path = tempfile.mktemp(suffix=".mp4")

    if st.sidebar.button("Process Video"):
        # Run processing
        st.sidebar.text("Processing Video...")
        success = process_video(temp_input_path, temp_output_path)
        
        if success:
            st.sidebar.text("Processing complete!")
            st.video(temp_output_path)
            
            with open(temp_output_path, "rb") as file:
                st.sidebar.download_button(
                    label="⬇️ Download Processed Video",
                    data=file,
                    file_name="processed_video.mp4",
                    mime="video/mp4"
                )
        else:
            st.sidebar.error("Processing failed. Could not generate output video.")

    # Cleanup input file
    temp_input.close()
    os.remove(temp_input_path)

    # Check and remove output file if it exists
    if os.path.exists(temp_output_path):
        os.remove(temp_output_path)
else:
    st.info("Please upload a video file to start processing.")

